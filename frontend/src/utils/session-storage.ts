/**
 * Session storage utility for chat history persistence
 * Uses browser's sessionStorage to persist chat history within a user session
 * Sessions are browser-based only (lost when browser is closed)
 */

// Define the structure to be stored in session storage
interface SessionStorageData {
  chatSessions: Record<string, ChatSessionData>;
  currentSessionId: string | null;
  lastActivity: Date;
}

// Define the structure for a single chat session
interface ChatSessionData {
  messages: any[]; // Using any to avoid circular import issues with Message interface
  lastUpdated: Date;
  createdAt: Date;
}

/**
 * Initialize the session storage with default values
 */
const initializeStorage = (): void => {
  const defaultData: SessionStorageData = {
    chatSessions: {},
    currentSessionId: null,
    lastActivity: new Date(),
  };
  sessionStorage.setItem('chatData', JSON.stringify(defaultData));
};

/**
 * Get the current session data from storage
 */
export const getSessionData = (): SessionStorageData => {
  const stored = sessionStorage.getItem('chatData');
  if (!stored) {
    initializeStorage();
    return getSessionData();
  }
  
  try {
    return JSON.parse(stored, (key, value) => {
      // Deserialize dates properly
      if (key === 'lastActivity' && typeof value === 'string') {
        return new Date(value);
      }
      return value;
    });
  } catch (e) {
    console.error('Error parsing session storage data, reinitializing:', e);
    initializeStorage();
    return getSessionData();
  }
};

/**
 * Save session data to storage
 */
export const setSessionData = (data: SessionStorageData): void => {
  try {
    // Serialize dates properly
    const serialized = JSON.stringify(data, (key, value) => {
      if (key === 'lastActivity' && value instanceof Date) {
        return value.toISOString();
      }
      return value;
    });
    sessionStorage.setItem('chatData', serialized);
  } catch (e) {
    console.error('Error saving session data:', e);
  }
};

/**
 * Get the current active session ID
 */
export const getCurrentSessionId = (): string | null => {
  const data = getSessionData();
  return data.currentSessionId;
};

/**
 * Set the current active session ID
 */
export const setCurrentSessionId = (sessionId: string): void => {
  const data = getSessionData();
  data.currentSessionId = sessionId;
  data.lastActivity = new Date();
  setSessionData(data);
};

/**
 * Save a chat session to storage
 */
export const saveSession = (sessionId: string, sessionData: any): void => {
  const data = getSessionData();
  data.chatSessions[sessionId] = sessionData;
  data.lastActivity = new Date();
  setSessionData(data);
};

/**
 * Load a chat session from storage
 */
export const loadSession = (sessionId: string): any | null => {
  const data = getSessionData();
  return data.chatSessions[sessionId] || null;
};

/**
 * Clear a specific chat session from storage
 */
export const clearSession = (sessionId: string): void => {
  const data = getSessionData();
  delete data.chatSessions[sessionId];
  if (data.currentSessionId === sessionId) {
    data.currentSessionId = null;
  }
  data.lastActivity = new Date();
  setSessionData(data);
};

/**
 * Clear all chat sessions from storage
 */
export const clearAllSessions = (): void => {
  const data = getSessionData();
  data.chatSessions = {};
  data.currentSessionId = null;
  data.lastActivity = new Date();
  setSessionData(data);
};

/**
 * Clear the current session's chat history only
 */
export const clearCurrentSessionHistory = (): void => {
  const data = getSessionData();
  if (data.currentSessionId && data.chatSessions[data.currentSessionId]) {
    // Keep the session but clear just the messages
    data.chatSessions[data.currentSessionId].messages = [];
    data.lastActivity = new Date();
    setSessionData(data);
  }
};

/**
 * Get all session IDs
 */
export const getAllSessionIds = (): string[] => {
  const data = getSessionData();
  return Object.keys(data.chatSessions);
};

/**
 * Update last activity timestamp
 */
export const updateLastActivity = (): void => {
  const data = getSessionData();
  data.lastActivity = new Date();
  setSessionData(data);
};