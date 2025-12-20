import React, { useState } from 'react';
import OriginalLayout from '@theme-original/Layout';
import ChatInterface from '@site/src/components/ChatInterface';

const Layout = (props) => {
  const [hovered, setHovered] = useState(false);

  return (
    <>
      <OriginalLayout {...props}>
        {props.children}
      </OriginalLayout>

      <div
        onMouseEnter={() => setHovered(true)}
        onMouseLeave={() => setHovered(false)}
        style={{
          position: 'fixed',
          bottom: '20px',
          right: '20px',
          zIndex: 9999,
          width: hovered ? '350px' : '40px',
          height: hovered ? '500px' : '40px',
          boxShadow: '0 4px 12px rgba(0, 0, 0, 0.15)',
          borderRadius: '8px',
          overflow: 'hidden',
          transition: 'width 0.3s, height 0.3s',
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center',
          backgroundColor: '#fff',
          cursor: 'pointer',
        }}
      >
        {hovered ? (
          <ChatInterface />
        ) : (
          <span
            style={{
              fontWeight: 'bold',
              fontSize: '20px',
              color: '#007bff',
            }}
          >
            ?
          </span>
        )}
      </div>
    </>
  );
};

export default Layout;
