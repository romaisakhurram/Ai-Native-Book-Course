/**
 * API service for chat endpoints
 * Handles communication between the UI and the backend chat API
 */
import { ChatRequest, ChatResponse, Message, MessageContext } from '../components/Chatbot';

// Define the base API URL from environment or default
let API_BASE_URL = process.env.REACT_APP_CHAT_API_URL || 'http://localhost:8000/api/v1';

// For deployed sites, use the production API endpoint
if (typeof window !== 'undefined' && window.location.hostname.includes('github.io')) {
  API_BASE_URL = window.ENV?.REACT_APP_CHAT_API_URL || 'https://romaisakhurram-deploy-project.hf.space/api/v1';
}

// Define the possible statuses for queued messages
type QueuedMessageStatus = 'queued' | 'sending' | 'sent' | 'error';

// Interface for managing queued messages
interface QueuedMessage {
  id: string;
  request: ChatRequest;
  timestamp: Date;
  status: QueuedMessageStatus;
  retries: number;
}

// In-memory queue for messages when AI service is unavailable
let messageQueue: QueuedMessage[] = [];

/**
 * Start a new chat session
 * @returns The new session ID
 */
export const startNewSession = async (): Promise<string> => {
  try {
    const response = await fetch(`${API_BASE_URL}/chat/start`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
    });

    if (!response.ok) {
      throw new Error(`Failed to start session: ${response.status} ${response.statusText}`);
    }

    const data = await response.json();
    return data.sessionId;
  } catch (error) {
    console.error('Error starting new session:', error);
    throw error;
  }
};

/**
 * Send a message to the backend (non-streaming)
 * @param request The chat request containing message, session ID, and context
 * @returns The chat response from the backend
 */
export const sendMessage = async (request: ChatRequest): Promise<ChatResponse> => {
  try {
    const response = await fetch(`${API_BASE_URL}/chat/send`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(request),
    });

    if (!response.ok) {
      throw new Error(`Failed to send message: ${response.status} ${response.statusText}`);
    }

    const data = await response.json();
    return {
      ...data,
      timestamp: new Date(data.timestamp),
    };
  } catch (error) {
    console.error('Error sending message:', error);

    // If we can't reach the service, add the message to the queue
    if (isNetworkError(error as Error)) {
      return queueMessage(request);
    }

    // For other errors (like 500), return a helpful error response
    return {
      responseId: `error_${Date.now()}`,
      content: "Sorry, I encountered an error processing your request. Please try again later.",
      timestamp: new Date(),
      status: 'error',
    };
  }
};

/**
 * Send a message and stream the response (Server-Sent Events)
 * @param request The chat request containing message, session ID, and context
 * @param onMessage Callback for each message chunk as it arrives
 * @param onError Callback for error handling
 * @param onComplete Optional callback for when streaming completes
 */
export const streamMessage = (
  request: ChatRequest, 
  onMessage: (content: string, isComplete: boolean, status: 'success' | 'error' | 'queued') => void,
  onError: (error: Error) => void,
  onComplete?: () => void
): void => {
  // If the service is unavailable, queue the message
  if (!isServiceAvailable()) {
    queueMessage(request);
    onMessage('', true, 'queued');
    if (onComplete) onComplete();
    return;
  }

  try {
    // Using fetch with streaming for SSE
    fetch(`${API_BASE_URL}/chat/stream`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(request),
    })
    .then(response => {
      if (!response.ok) {
        throw new Error(`Stream request failed: ${response.status} ${response.statusText}`);
      }

      const reader = response.body?.getReader();
      if (!reader) {
        throw new Error('Failed to get response reader');
      }

      const decoder = new TextDecoder();
      let buffer = '';

      const readStream = async (): Promise<void> => {
        try {
          while (true) {
            const { done, value } = await reader.read();
            
            if (done) {
              break;
            }

            // Decode the chunk and add to buffer
            const chunk = decoder.decode(value, { stream: true });
            buffer += chunk;

            // Process complete lines in the buffer
            const lines = buffer.split('\n');
            buffer = lines.pop() || ''; // Keep the incomplete line in the buffer

            for (const line of lines) {
              if (line.startsWith('data: ')) {
                try {
                  const data = JSON.parse(line.substring(6)); // Remove 'data: ' prefix
                  
                  if (data.content !== undefined) {
                    onMessage(data.content, data.done || false, data.status || 'success');
                  }
                  
                  if (data.done) {
                    if (onComplete) onComplete();
                    return;
                  }
                } catch (e) {
                  console.error('Error parsing SSE data:', e);
                }
              }
            }
          }
        } catch (error) {
          console.error('Error reading stream:', error);
          onError(error as Error);
        } finally {
          reader.releaseLock();
          if (onComplete) onComplete();
        }
      };

      readStream();
    })
    .catch(error => {
      console.error('Stream error:', error);
      
      // If it's a network error, queue the message
      if (isNetworkError(error)) {
        queueMessage(request);
        onMessage('', true, 'queued');
      } else {
        onError(error);
      }
      
      if (onComplete) onComplete();
    });
  } catch (error) {
    console.error('Error initiating stream:', error);
    onError(error as Error);
    
    // If it's a network error, queue the message
    if (isNetworkError(error as Error)) {
      queueMessage(request);
      onMessage('', true, 'queued');
    }
    
    if (onComplete) onComplete();
  }
};

/**
 * Queue a message for later processing when service is unavailable
 * @param request The chat request to queue
 */
export const queueMessage = (request: ChatRequest): ChatResponse => {
  const queuedMessage: QueuedMessage = {
    id: `queue-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`,
    request,
    timestamp: new Date(),
    status: 'queued',
    retries: 0,
  };

  messageQueue.push(queuedMessage);
  console.log(`Message queued (queue size: ${messageQueue.length}). It will be sent when the service is available.`);

  // Return a response indicating the message is queued
  return {
    responseId: queuedMessage.id,
    content: '',
    timestamp: new Date(),
    status: 'error',
    // We'll update this when the message is actually processed
  };
};

/**
 * Process queued messages when the service becomes available
 */
export const processQueuedMessages = async (): Promise<void> => {
  if (messageQueue.length === 0) {
    return; // Nothing to process
  }

  // Filter to only queued messages (not already being sent)
  const queuedMessages = messageQueue.filter(m => m.status === 'queued');
  
  for (const queuedMsg of queuedMessages) {
    try {
      // Update status to sending
      queuedMsg.status = 'sending';
      
      // Attempt to send the message
      await sendMessage(queuedMsg.request);
      
      // Update status to sent
      queuedMsg.status = 'sent';
      
      // Remove from queue
      messageQueue = messageQueue.filter(m => m.id !== queuedMsg.id);
      
      console.log(`Successfully sent queued message: ${queuedMsg.id}`);
    } catch (error) {
      console.error(`Failed to send queued message: ${queuedMsg.id}`, error);
      
      // Update status to error and increment retries
      queuedMsg.status = 'error';
      queuedMsg.retries++;
      
      // If we've retried too many times, remove from queue
      if (queuedMsg.retries > 3) {
        console.warn(`Dropping message after ${queuedMsg.retries} retries: ${queuedMsg.id}`);
        messageQueue = messageQueue.filter(m => m.id !== queuedMsg.id);
      }
    }
  }
};

/**
 * Get the current message queue
 */
export const getQueuedMessages = (): QueuedMessage[] => {
  return [...messageQueue];
};

/**
 * Check if the service is available by making a simple test request
 */
const isServiceAvailable = async (): Promise<boolean> => {
  try {
    const response = await fetch(`${API_BASE_URL}/health`, {
      method: 'GET',
      cache: 'no-cache',
    });
    return response.ok;
  } catch (error) {
    return false;
  }
};

/**
 * Check if an error is a network error
 */
const isNetworkError = (error: Error): boolean => {
  return (
    error.message.includes('Failed to fetch') ||
    error.message.includes('Network Error') ||
    error.message.includes('TypeError') ||
    error.message.includes('NetworkError') ||
    error.message.includes('ETIMEDOUT') ||
    error.message.includes('ECONNREFUSED') ||
    error.message.includes('ENOTFOUND')
  );
};

/**
 * Initialize the API service - check service availability and process any queued messages
 */
export const initializeApiService = async (): Promise<void> => {
  // Check if service is available and process any queued messages
  if (await isServiceAvailable()) {
    await processQueuedMessages();
  }
};