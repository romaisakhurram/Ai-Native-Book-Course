// API Configuration for deployed site
// This file sets the correct API endpoint for the deployed site
if (typeof process === 'undefined') {
  // Set environment variable for browser-based access
  window.REACT_APP_CHAT_API_URL = 'https://romaisakhurram-deploy-project.hf.space/api/v1';
}