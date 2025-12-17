/**
 * Utility functions for handling text selection in the book
 */

// Function to get the currently selected text
export const getSelectedText = () => {
  return window.getSelection ? window.getSelection().toString().trim() : '';
};

// Function to get information about the selected text
export const getSelectionInfo = () => {
  const selection = window.getSelection();
  
  if (!selection || selection.toString().trim() === '') {
    return null;
  }
  
  const range = selection.getRangeAt(0);
  const selectedText = selection.toString().trim();
  
  // Get the bounding rectangle for the selection
  const rect = range.getBoundingClientRect();
  
  // Get the container element
  const container = range.commonAncestorContainer;
  const element = container.nodeType === 1 ? container : container.parentElement;
  
  return {
    text: selectedText,
    range: range,
    rect: rect,
    element: element,
    position: {
      x: rect.left + window.scrollX,
      y: rect.top + window.scrollY
    }
  };
};

// Function to add event listener for text selection
export const addSelectionListener = (callback) => {
  const handleSelection = () => {
    const selectionInfo = getSelectionInfo();
    if (selectionInfo) {
      callback(selectionInfo);
    }
  };

  document.addEventListener('mouseup', handleSelection);
  
  // Return a function to remove the event listener
  return () => {
    document.removeEventListener('mouseup', handleSelection);
  };
};

// Function to highlight selected text
export const highlightSelectedText = () => {
  const selection = window.getSelection();
  
  if (!selection || selection.rangeCount === 0) {
    return null;
  }
  
  const range = selection.getRangeAt(0);
  const preSelectionRange = range.cloneRange();
  preSelectionRange.selectNodeContents(document.body);
  preSelectionRange.setEnd(range.startContainer, range.startOffset);
  
  const start = preSelectionRange.toString().length;
  const end = start + range.toString().length;
  
  return {
    text: range.toString(),
    start: start,
    end: end,
    range: range
  };
};

// Function to clear text selection
export const clearSelection = () => {
  if (window.getSelection) {
    window.getSelection().removeAllRanges();
  } else if (document.selection) {
    document.selection.empty();
  }
};

// Function to wrap selected text with a highlight element
export const wrapSelectedText = (wrapperElement) => {
  const selection = window.getSelection();
  
  if (!selection || selection.rangeCount === 0) {
    return false;
  }
  
  const range = selection.getRangeAt(0);
  const wrapper = wrapperElement || document.createElement('mark');
  
  range.surroundContents(wrapper);
  return true;
};