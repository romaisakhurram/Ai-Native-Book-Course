import React, { useState, useEffect, useRef } from 'react';
import './ChatInterface.css'; // Import the CSS file for the chat interface

const ChatInterface = ({ sessionId, backendUrl }) => {
  // Use API base URL if available, otherwise construct from backend URL
  let apiBaseUrl = (typeof process !== 'undefined' && process.env && process.env.REACT_APP_API_BASE_URL)
    || (typeof window !== 'undefined' && window.__API_BASE__)
    || backendUrl
    || (typeof window !== 'undefined' && window.__BACKEND_URL__)
    || 'https://romaisakhurram-deploy-project.hf.space';

  // If apiBaseUrl is the backend URL (like http://127.0.0.1:8000), append /api/v1
  // If it already includes /api/v1 (like http://127.0.0.1:8000/api/v1), use as is
  if (!apiBaseUrl.endsWith('/api/v1')) {
    if (apiBaseUrl.endsWith('/')) {
      apiBaseUrl += 'api/v1';
    } else {
      apiBaseUrl += '/api/v1';
    }
  }

  // We'll use the session ID provided or create one if needed
  const [effectiveSessionId, setEffectiveSessionId] = useState(sessionId || null);

  const [messages, setMessages] = useState([]);
  const [inputText, setInputText] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [selectedText, setSelectedText] = useState('');
  const [queryMode, setQueryMode] = useState('FULL_BOOK'); // FULL_BOOK or SELECTED_TEXT_ONLY
  const messagesEndRef = useRef(null);

  const genId = () => {
    try {
      if (typeof crypto !== 'undefined' && crypto.randomUUID) return crypto.randomUUID();
    } catch (e) {}
    return `${Date.now()}-${Math.random().toString(36).slice(2,9)}`;
  };

  // Function to scroll to the bottom of the chat
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  // Scroll to bottom whenever messages change
  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // Handle text selection (mouse and keyboard)
  useEffect(() => {
    const handleTextSelection = () => {
      const sel = (typeof window !== 'undefined' && window.getSelection) ? window.getSelection().toString().trim() : '';
      setSelectedText(sel || '');
    };

    document.addEventListener('selectionchange', handleTextSelection);
    document.addEventListener('mouseup', handleTextSelection);
    return () => {
      document.removeEventListener('selectionchange', handleTextSelection);
      document.removeEventListener('mouseup', handleTextSelection);
    };
  }, []);

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
      // Helper function to validate if a session ID is a proper UUID
      const isValidUUID = (id) => {
        const uuidRegex = /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i;
        return uuidRegex.test(id);
      };

      // Determine the endpoint to use and prepare appropriate request
      let endpoint, requestBody;
      if (effectiveSessionId && isValidUUID(effectiveSessionId)) {
        // If we have a valid UUID session ID, use the queries endpoint
        endpoint = `${apiBaseUrl}/sessions/${effectiveSessionId}/queries`;
        requestBody = {
          query_text: inputText,
          query_mode: queryMode,
          selected_text: queryMode === 'SELECTED_TEXT_ONLY' ? selectedText : null
        };
      } else {
        // If no session ID or invalid session ID, first create a session using chat endpoint
        let actualSessionId = effectiveSessionId;
        if (!actualSessionId || !isValidUUID(actualSessionId)) {
          const sessionResponse = await fetch(`${apiBaseUrl}/chat/start`, {
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

        endpoint = `${apiBaseUrl}/chat/send`;
        requestBody = {
          message: inputText,
          sessionId: actualSessionId,
          context: queryMode === 'SELECTED_TEXT_ONLY' && selectedText ? {
            selectedText: selectedText,
            sourcePage: window.location.pathname
          } : null
        };
      }

      // Send the query to the backend
      const response = await fetch(endpoint, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(requestBody)
      });

      if (!response.ok) {
        // If we get a 404 or 400 when using the queries endpoint, it might be because the session doesn't exist or is invalid
        if ((response.status === 404 || response.status === 400) && endpoint.includes('/sessions/') && endpoint.includes('/queries')) {
          console.log('Session not found or invalid, switching to chat endpoint...');
          // Switch to using the chat endpoint for this request
          const chatEndpoint = `${apiBaseUrl}/chat/send`;
          // Create a new session first
          const sessionResponse = await fetch(`${apiBaseUrl}/chat/start`, {
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
          const newSessionId = sessionData.sessionId;
          setEffectiveSessionId(newSessionId); // Update the state with the new session ID

          const chatRequestBody = {
            message: inputText,
            sessionId: newSessionId,
            context: queryMode === 'SELECTED_TEXT_ONLY' && selectedText ? {
              selectedText: selectedText,
              sourcePage: window.location.pathname
            } : null
          };

          const chatResponse = await fetch(chatEndpoint, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json'
            },
            body: JSON.stringify(chatRequestBody)
          });

          if (!chatResponse.ok) {
            let errText = `HTTP error! status: ${chatResponse.status}`;
            try { const j = await chatResponse.json(); if (j && j.error) errText = j.error; } catch(e){}
            throw new Error(errText);
          }

          const chatData = await chatResponse.json();

          // Chat endpoint response (ChatResponse format)
          const botMessage = {
            id: genId(),
            text: chatData.content,
            sender: 'bot',
            timestamp: new Date(),
            sources: [] // Chat endpoint doesn't return source chunks in the same format
          };

          setMessages(prev => [...prev, botMessage]);
          return; // Exit early since we've handled the request with the chat endpoint
        } else {
          // For other errors, parse and throw as before
          let errText = `HTTP error! status: ${response.status}`;
          try { const j = await response.json(); if (j && j.error) errText = j.error; } catch(e){}
          throw new Error(errText);
        }
      }

      const data = await response.json();

      // Determine response format based on endpoint used
      let responseText, sources;
      if (endpoint.includes('/chat/send')) {
        // Chat endpoint response (ChatResponse format)
        responseText = data.content;
        // Chat endpoint doesn't return source chunks in the same format
        sources = [];
      } else {
        // Queries endpoint response (QueryResponse format)
        responseText = data.response_text;
        sources = data.source_chunks || [];
      }

      // Add the response to the chat
      const botMessage = {
        id: genId(),
        text: responseText,
        sender: 'bot',
        timestamp: new Date(),
        sources: sources
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
                          <strong>Document:</strong> {source.document_id}<br />
                          <span className="source-content">{source.content.substring(0, 100)}{source.content.length > 100 ? '...' : ''}</span>
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