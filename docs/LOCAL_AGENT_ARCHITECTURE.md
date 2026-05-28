# JANET Local Agent Architecture

JANET is designed as a local OpenClaw-style desktop agent.

## Core Principle

JANET should execute work locally by default. Cloud AI is optional and should only be used when the user chooses a provider and supplies a key/session config.

## Layers

1. Chat UI
   - Light ChatGPT-like interface in `janet_chat.py`
   - Provider/model/endpoint/API-key controls
   - Keys are hidden in the UI and kept in memory for the app session

2. Local Agent Core
   - `helixmind_bio_ai.py`
   - Desktop control
   - Notes
   - Job queue
   - Bioinformatics commands
   - Local workspace and logs

3. Optional AI Connector
   - `ai_providers.py`
   - Local fallback planning
   - Ollama local LLM support
   - OpenAI-compatible APIs
   - Gemini
   - Anthropic
   - OpenRouter
   - Custom compatible endpoints

4. Tool Execution
   - App opening
   - Typing/pasting
   - Hotkeys
   - Mouse clicks
   - Bioinformatics functions
   - File workspace commands

## Provider Modes

```text
local       no API key, local fallback planner
ollama      local model through Ollama
openai      OpenAI chat completions endpoint
openrouter  OpenRouter chat completions endpoint
gemini      Gemini REST endpoint
anthropic   Anthropic messages endpoint
compatible  custom OpenAI-compatible endpoint
```

## Safety

JANET must not let AI text directly run arbitrary system commands. AI can suggest a plan; JANET executes only supported local commands.

Blocked categories:

- credit card data
- passwords
- OTPs
- API keys typed into other apps
- destructive delete commands
- shutdown/restart
- hidden background control
- arbitrary shell execution

## Goal

JANET should feel like a local desktop coworker: visible, fast, useful, and practical, with optional AI reasoning layered on top of local tools.
