/**
 * Message model
 * Represents an individual message in the conversation history
 */
export interface Message {
  id: string;
  type: 'user' | 'ai';
  content: string;
  timestamp: Date;
  context?: MessageContext;
  status: 'pending' | 'complete' | 'error' | 'queued';
}

/**
 * Creates a new message
 * @param type The type of message (user or ai)
 * @param content The content of the message
 * @param context Optional context information
 * @returns A new message object
 */
export const createMessage = (
  type: 'user' | 'ai',
  content: string,
  context?: MessageContext
): Message => {
  return {
    id: `msg-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`,
    type,
    content,
    timestamp: new Date(),
    context,
    status: 'pending',
  };
};