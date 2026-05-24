# Low-Token Chatbot Factory

This repo uses a low-token setup for repetitive chatbot generation.

## What Runs Automatically

GitHub Actions runs `.github/workflows/generate-chatbot.yml` on schedule. It installs Ollama on the runner, pulls a small local model, then calls:

```bash
python tools/chatbot_factory/generate.py
```

The generator creates a new project under `ai-chatbots/` and commits it back to the repo.

## Token Strategy

- Python templates create the repeated file structure.
- Ollama generates small theme copy locally inside the GitHub Action.
- If Ollama install or model pull fails, the generator falls back to built-in template copy.
- Manual review can be saved for bugs, architecture, biotech logic, optimization, and top project polish.

## Ollama Defaults

The workflow uses `llama3.2:1b` by default because it is small enough for GitHub-hosted runners.

You can manually run the workflow and choose another model, but larger models may be slow or fail on free GitHub runners.

## Manual Run

Go to Actions -> Generate chatbot project -> Run workflow. You can optionally provide:

- theme slug, such as `robot-gardener`, `startup-coach`, `biotech-notes`, or `game-master`
- Ollama model, such as `llama3.2:1b`

## Local Run

If you have Ollama installed locally:

```bash
OLLAMA_URL=http://localhost:11434 OLLAMA_MODEL=llama3.2:1b python tools/chatbot_factory/generate.py
```

Without Ollama, the script still works using templates.

## Output

Each generated chatbot includes:

- browser demo mode that works without setup
- optional Vercel real AI mode
- visitor-provided OpenAI API key flow
- README deployment notes
