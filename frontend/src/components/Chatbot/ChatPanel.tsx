import React from 'react';
import './ChatPanel.css';

interface ChatPanelProps {
  children: React.ReactNode;
  onClose: () => void;
}

const ChatPanel: React.FC<ChatPanelProps> = ({ children, onClose }) => {
  // Close panel when clicking on the overlay (but not on the panel content)
  const handleOverlayClick = (e: React.MouseEvent) => {
    if ((e.target as HTMLElement).classList.contains('chat-panel-overlay')) {
      onClose();
    }
  };

  return (
    <div className="chat-panel-overlay" onClick={handleOverlayClick}>
      <div className="chat-panel">
        <div className="chat-panel-header">
          <h3>Book Assistant</h3>
          <button
            className="close-button"
            onClick={onClose}
            aria-label="Close chat"
          >
            ×
          </button>
        </div>
        <div className="chat-panel-content">
          {children}
        </div>
      </div>
    </div>
  );
};

export default ChatPanel;