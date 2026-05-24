# Lab Mentor Chatbot

A ready-to-run AI chatbot web app with a practical lab mentor theme. The browser UI talks to a Node.js backend, and the backend calls the OpenAI Responses API with your server-side API key.

## What it includes

- Node.js Express backend
- OpenAI SDK integration
- Server-side `OPENAI_API_KEY` handling
- Browser chat interface
- Themed lab mentor system instructions

## Setup

1. Install Node.js 18 or newer.
2. Copy `.env.example` to `.env`.
3. Add your OpenAI API key to `.env`.
4. Install dependencies:

```bash
npm install
```

5. Start the app:

```bash
npm start
```

6. Open the local URL shown in the terminal, usually `http://localhost:3000`.

## Files

- `package.json` - scripts and dependencies
- `.env.example` - required environment variable
- `server.js` - backend API and static file server
- `public/index.html` - chat page
- `public/style.css` - interface styling
- `public/script.js` - browser chat behavior
