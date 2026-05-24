# Low-Token Chatbot Factory

This repo uses a low-token setup for repetitive chatbot generation.

## What Runs Automatically

GitHub Actions runs `.github/workflows/generate-chatbot.yml` on schedule. It installs Ollama on the runner, pulls a small local model, verifies the model can return usable chatbot JSON, then calls:

```bash
python tools/chatbot_factory/generate.py
```

The generator creates a new project under `ai-chatbots/` and commits it back to the repo.

## Email Notifications

The workflow can email `torrickytan@gmail.com` whenever a new chatbot is committed.

Add these GitHub repository secrets in Settings -> Secrets and variables -> Actions:

- `MAIL_USERNAME` - SMTP username, usually your Gmail address
- `MAIL_PASSWORD` - SMTP password or Gmail app password

Optional secrets:

- `MAIL_SERVER` - defaults to `smtp.gmail.com`
- `MAIL_PORT` - defaults to `465`
- `MAIL_FROM` - defaults to `MAIL_USERNAME`

Without `MAIL_USERNAME` and `MAIL_PASSWORD`, chatbot generation still works but email is skipped.

## Token Strategy

- Python templates create the repeated file structure.
- Ollama is mandatory for scheduled generation.
- If Ollama install, model pull, or response verification fails, the workflow fails instead of making a template-only chatbot.
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
ollama serve
ollama pull llama3.2:1b
OLLAMA_URL=http://localhost:11434 OLLAMA_MODEL=llama3.2:1b python tools/chatbot_factory/generate.py
```

## Output

Each generated chatbot includes:

- browser demo mode that works without setup
- optional Vercel real AI mode
- visitor-provided OpenAI API key flow
- README deployment notes
