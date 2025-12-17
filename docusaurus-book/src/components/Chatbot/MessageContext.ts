/**
 * MessageContext model
 * Information that provides context for a message, particularly selected text
 */
export interface MessageContext {
  selectedText: string | null;
  sourcePage: string;
  selectionMetadata?: {
    position?: { start: number; end: number };
    length?: number;
  };
}

/**
 * Creates a new message context
 * @param selectedText The text selected by the user (max 500 words)
 * @param sourcePage The URL or identifier of the page where text was selected
 * @param selectionMetadata Additional properties about the selection
 * @returns A new message context object
 */
export const createMessageContext = (
  selectedText: string | null,
  sourcePage: string,
  selectionMetadata?: MessageContext['selectionMetadata']
): MessageContext => {
  // Ensure selected text doesn't exceed 500 words
  if (selectedText && selectedText.split(/\s+/).length > 500) {
    console.warn('Selected text exceeds 500-word limit, truncating...');
    const words = selectedText.split(/\s+/);
    selectedText = words.slice(0, 500).join(' ');
  }

  return {
    selectedText,
    sourcePage,
    selectionMetadata,
  };
};