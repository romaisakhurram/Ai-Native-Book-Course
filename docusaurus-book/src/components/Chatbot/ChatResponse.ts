/**
 * ChatResponse model
 * The data structure received from the backend
 */
export interface ChatResponse {
  responseId: string;
  content: string;
  timestamp: Date;
  status: 'success' | 'error';
  streamComplete?: boolean;
}

/**
 * Creates a new chat response
 * @param content The AI-generated response content
 * @param status The status of the response generation
 * @param streamComplete Indicates if streaming is complete (for SSE responses)
 * @returns A new chat response object
 */
export const createChatResponse = (
  content: string,
  status: 'success' | 'error' = 'success',
  streamComplete: boolean = false
): ChatResponse => {
  return {
    responseId: `resp-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`,
    content,
    timestamp: new Date(),
    status,
    streamComplete,
  };
};