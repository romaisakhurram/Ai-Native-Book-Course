/**
 * SelectionHandler utility
 * Handles text selection functionality for the chatbot UI
 * Implements the requirement that text selection should be cleared from content but shown in chat context
 */

import { createMessageContext } from './MessageContext';

// Callback type for when text is selected
type OnTextSelectedCallback = (selectedText: string | null) => void;

class SelectionHandler {
  private onTextSelected: OnTextSelectedCallback | null = null;

  constructor() {
    // Add event listener for selection changes
    document.addEventListener('selectionchange', this.handleSelectionChange);
  }

  /**
   * Set the callback function to be called when text is selected
   */
  setOnTextSelectedCallback(callback: OnTextSelectedCallback): void {
    this.onTextSelected = callback;
  }

  /**
   * Handle changes in text selection
   */
  private handleSelectionChange = (): void => {
    const selection = window.getSelection();
    let selectedText = selection?.toString()?.trim() || null;

    // If there's selected text, ensure it doesn't exceed 500 words
    if (selectedText) {
      const wordCount = selectedText.split(/\s+/).length;
      if (wordCount > 500) {
        console.warn(`Selected text has ${wordCount} words, exceeding the 500-word limit. Truncating...`);
        const words = selectedText.split(/\s+/);
        selectedText = words.slice(0, 500).join(' ');
      }
    }

    // Notify the callback if text was selected
    if (this.onTextSelected) {
      this.onTextSelected(selectedText);
    }

    // Clear the selection if text was selected (requirement: clear selection but show in chat)
    if (selectedText) {
      this.clearSelection();
    }
  };

  /**
   * Clear the current text selection
   */
  clearSelection(): void {
    const selection = window.getSelection();
    if (selection) {
      selection.removeAllRanges();
    }
  }

  /**
   * Get the currently selected text (without clearing it)
   */
  getSelectedText(): string | null {
    const selection = window.getSelection();
    let selectedText = selection?.toString()?.trim() || null;

    // Ensure it doesn't exceed 500 words
    if (selectedText) {
      const wordCount = selectedText.split(/\s+/).length;
      if (wordCount > 500) {
        console.warn(`Selected text has ${wordCount} words, exceeding the 500-word limit. Truncating...`);
        const words = selectedText.split(/\s+/);
        selectedText = words.slice(0, 500).join(' ');
      }
    }

    return selectedText;
  }

  /**
   * Create a message context from selected text
   */
  createMessageContext(selectedText: string | null): any {
    if (!selectedText) {
      return null;
    }

    return createMessageContext(
      selectedText,
      window.location.pathname,
      {
        position: {
          start: 0, // Could be calculated if needed
          end: selectedText.length
        },
        length: selectedText.length
      }
    );
  }

  /**
   * Cleanup method to remove event listeners
   */
  cleanup(): void {
    document.removeEventListener('selectionchange', this.handleSelectionChange);
  }
}

// Create a singleton instance
export const selectionHandler = new SelectionHandler();

export default SelectionHandler;