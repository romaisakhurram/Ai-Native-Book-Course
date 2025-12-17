import React, { useState, useEffect, useRef } from 'react';
import './ChatInterface.css'; // Import the CSS file for the chat interface

const ChatInterface = ({ sessionId, backendUrl = 'http://localhost:8000' }) => {
  const [messages, setMessages] = useState([]);
  const [inputText, setInputText] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [selectedText, setSelectedText] = useState('');
  const [queryMode, setQueryMode] = useState('FULL_BOOK'); // FULL_BOOK or SELECTED_TEXT_ONLY
  const messagesEndRef = useRef(null);

  // Function to scroll to the bottom of the chat
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  // Scroll to bottom whenever messages change
  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // Handle text selection
  useEffect(() => {
    const handleTextSelection = () => {
      const selectedText = window.getSelection().toString().trim();
      if (selectedText) {
        setSelectedText(selectedText);
      }
    };

    document.addEventListener('mouseup', handleTextSelection);
    return () => {
      document.removeEventListener('mouseup', handleTextSelection);
    };
  }, []);

  // Function to send a message to the backend
  const sendMessage = async () => {
    if (!inputText.trim() || isLoading) return;

    // Add user message to the chat
    const userMessage = {
      id: Date.now(),
      text: inputText,
      sender: 'user',
      timestamp: new Date()
    };
    setMessages(prev => [...prev, userMessage]);
    setIsLoading(true);
    
    try {
      // Prepare the query request
      const queryRequest = {
        query_text: inputText,
        query_mode: queryMode,
        selected_text: queryMode === 'SELECTED_TEXT_ONLY' ? selectedText : null
      };

      // Send the query to the backend
      const response = await fetch(`${backendUrl}/api/v1/sessions/${sessionId}/queries`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(queryRequest)
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();

      // Add the response to the chat
      const botMessage = {
        id: Date.now() + 1,
        text: data.response_text,
        sender: 'bot',
        timestamp: new Date(),
        sources: data.source_chunks || []
      };
      
      setMessages(prev => [...prev, botMessage]);
    } catch (error) {
      console.error('Error sending message:', error);
      
      // Add an error message to the chat
      const errorMessage = {
        id: Date.now() + 1,
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

  // Toggle between full book and selected text mode
  const toggleQueryMode = () => {
    setQueryMode(prev => prev === 'FULL_BOOK' ? 'SELECTED_TEXT_ONLY' : 'FULL_BOOK');
  };

  return (
    <div className="chat-interface">
      <div className="chat-header">
        <h3>RAG Chatbot</h3>
        <div className="query-mode-toggle">
          <label>
            <input
              type="checkbox"
              checked={queryMode === 'SELECTED_TEXT_ONLY'}
              onChange={toggleQueryMode}
            />
            Use Selected Text Only
          </label>
        </div>
      </div>
      
      {selectedText && queryMode === 'SELECTED_TEXT_ONLY' && (
        <div className="selected-text-preview">
          <strong>Selected Text:</strong> {selectedText.substring(0, 100)}{selectedText.length > 100 ? '...' : ''}
        </div>
      )}
      
      <div className="chat-messages">
        {messages.length === 0 ? (
          <div className="welcome-message">
            <p>Hello! I'm your book assistant. Ask me anything about the content you're reading.</p>
          </div>
        ) : (
          messages.map((message) => (
            <div 
              key={message.id} 
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
              <div className="message-timestamp">
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
        <input
          type="text"
          value={inputText}
          onChange={(e) => setInputText(e.target.value)}
          placeholder={queryMode === 'SELECTED_TEXT_ONLY' ? "Ask about selected text..." : "Ask about the book content..."}
          disabled={isLoading}
        />
        <button type="submit" disabled={isLoading || !inputText.trim()}>
          Send
        </button>
      </form>
    </div>
  );
};

export default ChatInterface;