# Frontend Integration Guide

This document describes how to integrate the RAG chatbot into your Docusaurus book pages.

## Setup

### 1. Install Dependencies

```bash
npm install react-markdown remark-gfm
```

### 2. Add the ChatInterface Component

The chat interface component can be added to any Docusaurus page or layout. Here's an example of how to integrate it into your layout:

```jsx
// Example integration in a Docusaurus layout or page
import React, { useState, useEffect } from 'react';
import ChatInterface from './src/components/ChatInterface';

function YourLayout({ children }) {
  const [sessionId, setSessionId] = useState(null);
  
  // Create a new session when the component mounts
  useEffect(() => {
    const createSession = async () => {
      try {
        const response = await fetch('http://localhost:8000/api/v1/sessions', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ 
            user_id: 'anonymous' // or actual user ID
          })
        });
        
        const data = await response.json();
        setSessionId(data.session_id);
      } catch (error) {
        console.error('Error creating session:', error);
      }
    };
    
    createSession();
  }, []);
  
  return (
    <div style={{ display: 'flex', flexDirection: 'column' }}>
      <main style={{ flex: 1 }}>
        {children}
      </main>
      <aside style={{ position: 'fixed', bottom: 0, right: 0, width: '400px', height: '500px' }}>
        {sessionId && (
          <ChatInterface 
            sessionId={sessionId} 
            backendUrl={'http://localhost:8000'} 
          />
        )}
      </aside>
    </div>
  );
}
```

## Integration Options

### Option 1: Floating Sidebar
Add the chat interface to the side of your book pages as a persistent element.

### Option 2: Page Element
Add the chat interface as an element within specific book pages where users are likely to ask questions.

### Option 3: Toggle Overlay
Create a button that shows/hides the chat interface as an overlay.

## Text Selection Integration

The chat interface automatically detects text selection on the page. When users select text and toggle the "Use Selected Text Only" option, the queries will be limited to the selected text.

## Environment Configuration

Make sure to update the backendUrl in production to point to your deployed backend service.

## Styling

The chat interface comes with default CSS but can be customized by modifying the `ChatInterface.css` file or adding custom styles with higher specificity.