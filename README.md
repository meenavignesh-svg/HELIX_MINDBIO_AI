# AI Chat Bots Per Minute

A growing collection of small themed chatbot projects. Each chatbot has its own folder, browser demo, and setup notes.

## Chatbot Catalog

| S.No | Chatbot | Made On (UTC) | Folder | Notes |
| ---: | --- | --- | --- | --- |
| 1 | Moon Cafe | 2026-05-24 14:38 UTC | `ai-chatbots/moon-cafe-chatbot-2026-05-24-1438z` | Browser demo |
| 2 | Pirate Map | 2026-05-24 14:39 UTC | `ai-chatbots/pirate-map-chatbot-2026-05-24-1439z` | Browser demo |
| 3 | Lab Mentor | 2026-05-24 14:40 UTC | `ai-chatbots/lab-mentor-chatbot-2026-05-24-1440z` | Browser demo with AI backend option |
| 4 | Ocean Medic | 2026-05-24 15:03 UTC | `ai-chatbots/ocean-medic-chatbot-2026-05-24-1503z` | Browser demo with AI backend option |
| 5 | Museum Guide | 2026-05-24 15:13 UTC | `ai-chatbots/museum-guide-chatbot-2026-05-24-1513z` | Browser demo with AI backend option |
| 6 | Travel Planner | 2026-05-24 15:18 UTC | `ai-chatbots/travel-planner-chatbot-2026-05-24-1518z` | Browser demo with AI backend option |
| 7 | Forest Ranger | 2026-05-24 15:20 UTC | `ai-chatbots/forest-ranger-chatbot-2026-05-24-1520z` | Browser demo with AI backend option |
| 8 | City Chef | 2026-05-24 15:22 UTC | `ai-chatbots/city-chef-chatbot-2026-05-24-1522z` | Browser demo with AI backend option |
| 9 | Study Buddy | 2026-05-24 15:23 UTC | `ai-chatbots/study-buddy-chatbot-2026-05-24-1523z` | Browser demo with AI backend option |
| 10 | Fitness Coach | 2026-05-24 15:26 UTC | `ai-chatbots/fitness-coach-chatbot-2026-05-24-1526z` | Browser demo with AI backend option |
| 11 | Budget Mentor | 2026-05-24 15:32 UTC | `ai-chatbots/budget-mentor-chatbot-2026-05-24-1532z` | Browser demo with optional Vercel AI mode |
| 12 | Beat Producer | 2026-05-24 15:41 UTC | `ai-chatbots/beat-producer-chatbot-2026-05-24-1541z` | Browser demo with optional Vercel AI mode |
| 13 | Robot Gardener | 2026-05-24 16:10 UTC | `ai-chatbots/robot-gardener-chatbot-2026-05-24-1610z` | Browser demo with optional Vercel AI mode |
| 14 | Startup Coach | 2026-05-24 16:21 UTC | `ai-chatbots/startup-coach-chatbot-2026-05-24-1621z` | Browser demo with optional Vercel AI mode |

## How To Try A Chatbot

Open the chatbot folder, then open `public/index.html` for newer projects. Some older projects use `index.html` directly in the project folder.

## Modes

- Browser demo: works immediately in a browser with built-in replies.
- AI backend option: includes backend files for real AI responses when configured.
- Optional Vercel AI mode: can be deployed to Vercel and asks visitors for their own OpenAI API key.

## Automation

The repository includes a chatbot factory workflow in `.github/workflows/generate-chatbot.yml`. It is designed to create new chatbot projects on a schedule using Python templates and Ollama.

More details:

- `CHATBOT_CATALOG.md`
- `LOW_TOKEN_FACTORY.md`
- `tools/chatbot_factory/README.md`
