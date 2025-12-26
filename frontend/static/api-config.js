// API configuration for frontend
// This file is loaded dynamically by the Docusaurus application

(function() {
  window.API_CONFIG = {
    // Backend API URL - adjust this based on your deployment
    API_BASE_URL: typeof window !== 'undefined' && window.location.hostname === 'localhost'
      ? 'http://127.0.0.1:8000/api/v1'
      : 'https://romaisakhurram-deploy-project.hf.space/api/v1',

    // Timeout for API requests (in milliseconds)
    REQUEST_TIMEOUT: 30000,

    // Maximum number of retries for failed requests
    MAX_RETRIES: 3
  };

  console.log('API configuration loaded:', window.API_CONFIG);
})();