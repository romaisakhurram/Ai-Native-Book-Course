import React from 'react';
import { Message as MessageType } from './Message'; // Import the interface from the .ts file
import './Message.css';

interface MessageComponentProps {
  message: MessageType;
}

const MessageComponent: React.FC<MessageComponentProps> = ({ message }) => {
  const isUser = message.type === 'user';

  // Format the timestamp for display
  const formatTime = (date: Date) => {
    return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  };

  return (
    <div className={`message ${isUser ? 'user-message' : 'ai-message'}`}>
      <div className="message-content">
        {isUser ? (
          <>
            <div className="user-bubble">
              <p>{message.content}</p>
            </div>
            <div className="message-timestamp">{formatTime(message.timestamp)}</div>
          </>
        ) : (
          <>
            <div className="ai-bubble">
              <p>{message.content}</p>
            </div>
            <div className="message-timestamp">{formatTime(message.timestamp)}</div>
          </>
        )}
      </div>
    </div>
  );
};

export default MessageComponent;