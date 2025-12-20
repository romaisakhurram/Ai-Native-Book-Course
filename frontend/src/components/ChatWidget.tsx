import React, { useState } from "react";

export default function ChatWidget() {
  const [open, setOpen] = useState(false);

  return (
    <div
      onMouseEnter={() => setOpen(true)}
      onMouseLeave={() => setOpen(false)}
      style={{
        position: "fixed",
        bottom: "20px",
        right: "20px",
        width: open ? "300px" : "60px",
        height: open ? "400px" : "60px",
        background: "white",
        border: "1px solid #ccc",
        borderRadius: "10px",
        zIndex: 9999,
        overflow: "hidden",
        transition: "all 0.3s ease",
        cursor: "pointer",
      }}
    >
      {open ? (
        <div style={{ padding: "10px", height: "100%" }}>
          <strong>RAG Chatbot</strong>
          <p style={{ fontStyle: "italic", marginTop: "5px" }}>
            Hello! I'm your book assistant. Ask me anything about the content you're reading.
          </p>
          <textarea
            placeholder="Ask about the book content..."
            style={{
              width: "100%",
              marginTop: "10px",
              height: "200px",
              resize: "none",
            }}
          />
          <button
            style={{
              marginTop: "5px",
              width: "100%",
              padding: "5px",
              background: "#555",
              color: "white",
              border: "none",
              borderRadius: "5px",
            }}
          >
            Send
          </button>
        </div>
      ) : (
        <div
          style={{
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            height: "100%",
            fontWeight: "bold",
          }}
        >
          Chat
        </div>
      )}
    </div>
  );
}
