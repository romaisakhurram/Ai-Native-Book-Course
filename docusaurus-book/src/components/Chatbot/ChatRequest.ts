/**
 * ChatRequest model
 * The data structure sent from the UI to the backend
 */
export interface ChatRequest {
  message: string;
  sessionId: string;
  context?: MessageContext;
}

/**
 * Creates a new chat request
 * @param message The user's message
 * @param sessionId The current session ID
 * @param context Optional context information
 * @returns A new chat request object
 */
export const createChatRequest = (
  message: string,
  sessionId: string,
  context?: MessageContext
): ChatRequest => {
  return {
    message,
    sessionId,
    context,
  };
};