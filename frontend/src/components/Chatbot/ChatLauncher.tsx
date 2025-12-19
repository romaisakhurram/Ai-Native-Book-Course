import React, { useState, useEffect } from 'react';
import ChatPanel from './ChatPanel';
import ChatWindow from './ChatWindow';
import './ChatLauncher.css';

const ChatLauncher: React.FC = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [showChatWindow, setShowChatWindow] = useState(false);

  const toggleChat = () => {
    setIsOpen(!isOpen);
    if (!isOpen) {
      // When opening, show the chat window after a small delay to allow panel animation
      setTimeout(() => setShowChatWindow(true), 150);
    } else {
      // When closing, hide the chat window first, then close the panel
      setShowChatWindow(false);
      setTimeout(() => setIsOpen(false), 150);
    }
  };

  const closeChat = () => {
    setShowChatWindow(false);
    setTimeout(() => setIsOpen(false), 150);
  };

  return (
    <>
      <div className={`chat-launcher ${isOpen ? 'hidden' : ''}`}>
        <button 
          className="chat-launcher-button"
          onClick={toggleChat}
          aria-label={isOpen ? "Close chat" : "Open chat"}
          title={isOpen ? "Close chat" : "Open chat"}
        >
          <span className="chat-icon">💬</span>
        </button>
      </div>
      
      {isOpen && (
        <ChatPanel isOpen={isOpen} onClose={closeChat}>
          {showChatWindow ? <ChatWindow isOpen={true} onClose={closeChat} /> : null}
        </ChatPanel>
      )}
    </>
  );
};

export default ChatLauncher;