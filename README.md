# AI Native Book Course

This is a Docusaurus-based book/course website featuring content about Physical AI & Humanoid Robotics.

## Prerequisites

- Node.js (version 18 or higher)
- npm or yarn package manager

## Installation

1. Navigate to the `frontend` directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

## Local Development

1. From the `frontend` directory, run:
```bash
npm start
```

This command starts a local development server and opens up a browser window. Most changes are reflected live without requiring a restart.

## Building for Production

1. From the `frontend` directory, run:
```bash
npm run build
```

This command generates static content into the `build` directory and can be served using any static content hosting service.

## Deployment to GitHub Pages

This site is configured for deployment to GitHub Pages with the following settings:

- Repository: `romaisakhurram/ai-native-book-course`
- Branch: `AI-Native-Book`
- Base URL: `/ai-native-book-course/`

### Manual Deployment

If you need to manually update the GitHub Pages site:

1. Build the site:
```bash
npm run build
```

2. Copy the contents of the `build` directory to the root of the repository
3. Commit and push changes to the `AI-Native-Book` branch

### GitHub Actions Deployment

The site is automatically deployed via GitHub Actions when changes are pushed to the `AI-Native-Book` branch. The workflow is defined in `.github/workflows/gh-pages.yml`.

## Troubleshooting GitHub Actions Deployment Issues

If you encounter the error "Multiple artifacts named 'github-pages' were unexpectedly found":

1. Go to your repository's Actions tab
2. Cancel any running workflow executions
3. Delete old artifacts in Settings > Actions > General > Artifacts
4. Push a new commit to trigger a fresh deployment

## Project Structure

- `/frontend` - Contains the Docusaurus source code
- `/backend` - Contains the backend API for the chatbot functionality
- `/docs` - Contains the book/course content in Markdown format
- `/assets` - Contains images and other static assets

## AI Assistant Features

The site includes an AI assistant powered by:
- A RAG (Retrieval Augmented Generation) system
- Vector database (Qdrant) for content retrieval
- OpenAI-compatible API for response generation

The assistant can answer questions about the book content and provide contextual help to readers.