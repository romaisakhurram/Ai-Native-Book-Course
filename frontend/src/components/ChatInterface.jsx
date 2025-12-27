import React, { useState, useEffect, useRef } from 'react';
import './ChatInterface.css'; // Import the CSS file for the chat interface

const ChatInterface = ({ sessionId: propSessionId, backendUrl }) => {
  // Use API base URL if available, otherwise construct from backend URL
  const apiBaseUrl = (typeof process !== 'undefined' && process.env && process.env.REACT_APP_API_BASE_URL)
    || (typeof window !== 'undefined' && window.__API_BASE__)
    || backendUrl
    || (typeof window !== 'undefined' && window.__BACKEND_URL__)
    || 'http://127.0.0.1:8000'; // Default to local backend

  // Ensure the apiBaseUrl ends with /api/v1
  const normalizedApiBaseUrl = apiBaseUrl.endsWith('/api/v1')
    ? apiBaseUrl
    : apiBaseUrl.replace(/\/$/, '') + '/api/v1';  // Remove trailing slash and append /api/v1

  // Use the session ID provided via props, or create a temporary one
  const [effectiveSessionId, setEffectiveSessionId] = useState(propSessionId || null);
  const [messages, setMessages] = useState([]);
  const [inputText, setInputText] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [selectedText, setSelectedText] = useState('');
  const [queryMode, setQueryMode] = useState('FULL_BOOK'); // FULL_BOOK or SELECTED_TEXT_ONLY
  const messagesEndRef = useRef(null);

  // Generate a unique ID for messages
  const genId = () => {
    return `msg_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
  };

  // Handle text selection for context
  useEffect(() => {
    const handleTextSelection = () => {
      const selection = window.getSelection ? window.getSelection().toString().trim() : '';
      setSelectedText(selection);
    };

    document.addEventListener('selectionchange', handleTextSelection);
    document.addEventListener('mouseup', handleTextSelection);
    
    return () => {
      document.removeEventListener('selectionchange', handleTextSelection);
      document.removeEventListener('mouseup', handleTextSelection);
    };
  }, []);

  // Scroll to bottom of messages
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // Function to send a message to the backend
  const sendMessage = async () => {
    if (!inputText.trim() || isLoading) return;

    // Add user message to the chat
    const userMessage = {
      id: genId(),
      text: inputText,
      sender: 'user',
      timestamp: new Date()
    };
    setMessages(prev => [...prev, userMessage]);
    setIsLoading(true);

    try {
      // If no session ID exists, create one first
      let actualSessionId = effectiveSessionId;
      if (!actualSessionId) {
        const sessionResponse = await fetch(`${normalizedApiBaseUrl}/chat/start`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({})
        });

        if (!sessionResponse.ok) {
          throw new Error(`Failed to create session: ${sessionResponse.status} ${sessionResponse.statusText}`);
        }

        const sessionData = await sessionResponse.json();
        actualSessionId = sessionData.sessionId;
        setEffectiveSessionId(actualSessionId); // Update the state with the new session ID
      }

      // Prepare the request payload
      const requestBody = {
        message: inputText,
        sessionId: actualSessionId,
        context: queryMode === 'SELECTED_TEXT_ONLY' && selectedText ? {
          selectedText: selectedText,
          sourcePage: window.location.pathname
        } : null
      };

      // Send the message to the backend
      const response = await fetch(`${normalizedApiBaseUrl}/chat/send`, {
        method: 'POST',  // Important: Use POST method
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(requestBody)
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();

      // Add the response to the chat
      const botMessage = {
        id: genId(),
        text: data.content || data.response_text || "Sorry, I couldn't process your request.",
        sender: 'bot',
        timestamp: new Date(),
        sources: data.sources || []
      };

      setMessages(prev => [...prev, botMessage]);
    } catch (error) {
      console.error('Error sending message:', error);

      // Add an error message to the chat
      const errorMessage = {
        id: genId(),
        text: 'Sorry, I encountered an error processing your request. Please try again.',
        sender: 'bot',
        timestamp: new Date(),
        isError: true
      };

      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
      setInputText('');
    }
  };

  // Handle form submission
  const handleSubmit = (e) => {
    e.preventDefault();
    sendMessage();
  };

  // Handle Enter to send (Shift+Enter for newline)
  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  // Toggle between full book and selected text mode
  const toggleQueryMode = () => {
    setQueryMode(prev => prev === 'FULL_BOOK' ? 'SELECTED_TEXT_ONLY' : 'FULL_BOOK');
  };

  const clearSelection = () => setSelectedText('');

  return (
    <div className="chat-interface" style={{ height: 'var(--chat-height, 500px)' }}>
      <div className="chat-header">
        <h3>RAG Chatbot</h3>
        <div className="query-mode-toggle">
          <label>
            <input
              aria-label="Use selected text only"
              type="checkbox"
              checked={queryMode === 'SELECTED_TEXT_ONLY'}
              onChange={toggleQueryMode}
            />
            Use Selected Text Only
          </label>
        </div>
      </div>

      {selectedText && queryMode === 'SELECTED_TEXT_ONLY' && (
        <div className="selected-text-preview" role="region" aria-label="Selected text preview">
          <strong>Selected Text:</strong> {selectedText.substring(0, 200)}{selectedText.length > 200 ? '...' : ''}
          <button className="clear-selection-btn" onClick={clearSelection} aria-label="Clear selected text">Clear</button>
        </div>
      )}

      <div className="chat-messages" role="log" aria-live="polite" aria-label="Chat messages">
        {messages.length === 0 ? (
          <div className="welcome-message">
            <p>Hello! I'm your book assistant. Ask me anything about the content you're reading.</p>
          </div>
        ) : (
          messages.map((message) => (
            <div
              key={message.id}
              role="listitem"
              className={`message ${message.sender === 'user' ? 'user-message' : 'bot-message'}`}
            >
              <div className="message-content">
                {message.text}
                {message.sources && message.sources.length > 0 && (
                  <details className="sources-details">
                    <summary>Sources</summary>
                    <ul>
                      {message.sources.map((source, index) => (
                        <li key={index} className="source-item">
                          <strong>Document:</strong> {source.document_id || source.title || 'Unknown'}<br />
                          <span className="source-content">{source.content?.substring(0, 100) || source.text?.substring(0, 100) || ''}{(source.content?.length > 100 || source.text?.length > 100) ? '...' : ''}</span>
                        </li>
                      ))}
                    </ul>
                  </details>
                )}
              </div>
              <div className="message-timestamp" aria-hidden>
                {message.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
              </div>
            </div>
          ))
        )}
        {isLoading && (
          <div className="message bot-message">
            <div className="message-content">
              <div className="typing-indicator">
                <span></span>
                <span></span>
                <span></span>
              </div>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      <form className="chat-input-form" onSubmit={handleSubmit}>
        <textarea
          aria-label={queryMode === 'SELECTED_TEXT_ONLY' ? "Ask about selected text" : "Ask about the book content"}
          value={inputText}
          onChange={(e) => setInputText(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder={queryMode === 'SELECTED_TEXT_ONLY' ? "Ask about selected text..." : "Ask about the book content..."}
          disabled={isLoading}
          rows={2}
        />
        <button type="submit" disabled={isLoading || !inputText.trim()} aria-label="Send message">
          Send
        </button>
      </form>
      <div ref={messagesEndRef} />
    </div>
  );
};

export default ChatInterface;