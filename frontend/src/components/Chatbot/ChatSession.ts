/**
 * ChatSession model
 * Represents a single user's interaction with the chatbot during a browser session
 */
export interface ChatSession {
  sessionId: string;
  createdAt: Date;
  messages: Message[];
  isActive: boolean;
}

/**
 * Creates a new chat session
 * @returns A new chat session with a unique ID and current timestamp
 */
export const createChatSession = (): ChatSession => {
  return {
    sessionId: `sess-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`,
    createdAt: new Date(),
    messages: [],
    isActive: true,
  };
};