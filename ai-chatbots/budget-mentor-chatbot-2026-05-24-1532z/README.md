# Budget Mentor Chatbot

A Vercel-ready AI chatbot web app with a budget mentor theme. The page asks each visitor for their own OpenAI API key before chatting. The key is stored only in browser `sessionStorage` and sent to the serverless API route for each request.

## Includes

- Vercel serverless API route
- Official OpenAI Node SDK
- Visitor-provided API key flow
- Browser chat UI
- Budget mentor assistant instructions

## Local Run

Localhost only works on the computer running the app. Other people need the deployed Vercel public URL.

```bash
npm install
npm run dev
```

Open the local URL shown by Vercel CLI, usually `http://localhost:3000`.

## Deploy To Vercel

1. Import this GitHub repository in Vercel.
2. Set the root directory to `ai-chatbots/budget-mentor-chatbot-2026-05-24-1532z`.
3. Deploy.
4. Share the deployed Vercel URL.

No OpenAI API key is committed to this repo. Each visitor enters their own key in the page.

## Files

- `package.json`
- `vercel.json`
- `api/chat.js`
- `public/index.html`
- `public/style.css`
- `public/script.js`
