import React, { useState, useEffect, useRef } from 'react';
import MessageComponent from './MessageComponent';
import { Message, createMessage } from './Message';
import { ChatRequest, createChatRequest } from './ChatRequest';
import { streamMessage, initializeApiService } from '../../services/chat-api';
import { getSessionData, saveSession, loadSession, getCurrentSessionId, setCurrentSessionId } from '../../utils/session-storage';
import { selectionHandler } from './SelectionHandler';
import './ChatWindow.css';

const ChatWindow: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [sessionId, setSessionId] = useState<string | null>(null);
  const [selectedText, setSelectedText] = useState<string | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Initialize session when component mounts
  useEffect(() => {
    const initSession = async () => {
      await initializeApiService();

      // Get or create a session
      let currentSessionId = getCurrentSessionId();
      if (!currentSessionId) {
        // In a real implementation, we would call the backend to create a new session
        // For now, we'll generate a client-side ID
        currentSessionId = `sess-${Date.now()}`;
        setCurrentSessionId(currentSessionId);
      }

      setSessionId(currentSessionId);

      // Load any existing messages for this session
      const sessionData = loadSession(currentSessionId);
      if (sessionData && sessionData.messages) {
        setMessages(sessionData.messages);
      }
    };

    initSession();
  }, []);

  // Set up selection handler when component mounts
  useEffect(() => {
    const handleTextSelection = (text: string | null) => {
      setSelectedText(text);
    };

    selectionHandler.setOnTextSelectedCallback(handleTextSelection);

    // Cleanup function
    return () => {
      selectionHandler.setOnTextSelectedCallback(null);
    };
  }, []);

  // Save messages to session storage whenever they change
  useEffect(() => {
    if (sessionId && messages.length > 0) {
      saveSession(sessionId, { messages, lastUpdated: new Date() });
    }
  }, [messages, sessionId]);

  // Scroll to bottom of messages when they change
  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!inputValue.trim() || !sessionId) return;

    // Add user message to the chat
    const userMessage = createMessage('user', inputValue, selectedText ? { selectedText, sourcePage: window.location.pathname } : undefined);
    setMessages(prev => [...prev, userMessage]);

    // Clear the input and selected text
    setInputValue('');
    setSelectedText(null);

    // Set loading state
    setIsLoading(true);

    // Prepare the chat request
    const chatRequest: ChatRequest = createChatRequest(
      inputValue,
      sessionId,
      selectedText ? { selectedText, sourcePage: window.location.pathname } : undefined
    );

    // Send the message and handle streaming response
    streamMessage(
      chatRequest,
      (content, isComplete, status) => {
        // Update or add AI message
        setMessages(prev => {
          // Find the last AI message that is still pending
          const lastAIMessageIndex = prev.findLastIndex(msg => msg.type === 'ai' && msg.status === 'pending');

          if (lastAIMessageIndex !== -1) {
            // Update the existing message
            const updatedMessages = [...prev];
            const updatedMessage = { ...updatedMessages[lastAIMessageIndex], content: updatedMessages[lastAIMessageIndex].content + content };
            if (isComplete) {
              updatedMessage.status = 'complete';
            }
            updatedMessages[lastAIMessageIndex] = updatedMessage;
            return updatedMessages;
          } else {
            // Create a new message
            const newMessage = createMessage('ai', content, undefined);
            if (isComplete) {
              newMessage.status = 'complete';
            } else {
              newMessage.status = 'pending';
            }
            return [...prev, newMessage];
          }
        });
      },
      (error) => {
        console.error('Error streaming message:', error);
        // Add an error message
        setMessages(prev => [...prev, createMessage('ai', 'Sorry, I encountered an error processing your request.', undefined)]);
        setIsLoading(false);
      },
      () => {
        // Complete callback
        setIsLoading(false);
      }
    );
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e as any);
    }
  };

  const clearChatHistory = () => {
    if (window.confirm("Are you sure you want to clear the chat history?")) {
      // Set messages to empty array
      setMessages([]);
      // Also clear the session data in storage
      if (sessionId) {
        // Update session storage with empty messages
        saveSession(sessionId, { messages: [], lastUpdated: new Date(), createdAt: new Date() });
      }
    }
  };

  return (
    <div className="chat-window">
      <div className="chat-messages">
        {messages.length === 0 ? (
          <div className="welcome-message">
            <p>Hello! I'm your book assistant. You can ask me questions about the content, or select text and ask about it specifically.</p>
          </div>
        ) : (
          messages.map((message) => (
            <MessageComponent
              key={message.id}
              message={message}
            />
          ))
        )}
        {isLoading && (
          <div className="loading-indicator">
            <div className="typing-indicator">
              <span></span>
              <span></span>
              <span></span>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      <div className="chat-controls">
        <button
          className="clear-history-button"
          onClick={clearChatHistory}
          aria-label="Clear chat history"
        >
          Clear History
        </button>
      </div>

      <form className="chat-input-form" onSubmit={handleSubmit}>
        {selectedText && (
          <div className="selected-text-context">
            <small>Context: "{selectedText.substring(0, 100)}{selectedText.length > 100 ? '...' : ''}"</small>
          </div>
        )}
        <div className="input-container">
          <textarea
            className="chat-input"
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Ask a question about the book..."
            rows={1}
            aria-label="Type your message"
          />
          <button
            type="submit"
            className="send-button"
            disabled={!inputValue.trim() || isLoading}
            aria-label="Send message"
          >
            Send
          </button>
        </div>
      </form>
    </div>
  );
};

export default ChatWindow;