# JANET Bio AI

**JANET** is a light-themed, local-first Windows desktop agent for bioinformatics and computer work. She is designed to work like a local OpenClaw-style assistant: chat, plan, remember task context, open apps, type, click, run visible steps, use local tools, and show an animated desktop presence.

Wake word: `janet`

Legacy wake word: `helix` still works.

## Animated Desktop Presence

JANET now has a lightweight animated avatar inside the desktop chat window:

- idle state: green standing-by glow
- thinking state: blue pulsing motion
- responding state: violet speaking animation
- orbiting bio/AI nodes
- light theme, no heavy 3D engine required

The animation runs inside the app window, so it stays lightweight for low-end Windows laptops.

## Local OpenClaw-Style Agent

JANET can:

- chat in a light desktop window
- show an animated presence while working
- make visible plans before work
- open desktop apps
- type or paste into the active window
- press keys and hotkeys
- click the mouse
- queue multi-step jobs
- keep local session notes
- run local bioinformatics tools
- use optional AI providers only when you configure them

Core execution stays local. JANET does not need cloud AI to open apps, type, click, manage notes, or run bioinformatics tools.

## Optional AI Providers

The chat window includes an **AI settings** row:

```text
Provider | Model | Endpoint | API key | Use AI
```

Supported modes:

- `local` fallback planning with no API key
- `ollama` for local LLMs
- `openai`
- `gemini`
- `anthropic`
- `openrouter`
- `compatible` for custom OpenAI-compatible APIs

API keys are not hardcoded in the repo. When pasted into the app, the key is kept in the running app session. You can also use environment variables yourself:

```text
JANET_AI_PROVIDER
JANET_AI_MODEL
JANET_AI_KEY
JANET_AI_ENDPOINT
```

## AI Commands

```text
ask ai explain this bioinformatics workflow
plan analyze this FASTA file, summarize GC, then open PubMed
agent plan open Chrome, search PubMed, and draft notes
```

## Desktop Control Commands

```text
janet desktop status
janet open any app chrome
janet open any app notepad
janet type text Hello, I am JANET.
janet paste text This goes into the active window.
janet press key enter
janet hotkey ctrl+s
janet wait 0.2
janet click
janet click 500 300
```

## Bioinformatics

JANET can help with DNA/RNA reports, GC content, reverse complements, transcription, translation, ORFs, codon usage, motifs, k-mers, primer stats, restriction-site scans, FASTA summaries, protein weight, sequence comparison, alignment, and PubMed/NCBI/BLAST/UniProt/Ensembl/PDB opening.

## Safety Rules

- No API keys are hardcoded.
- Session API keys are hidden in the UI field.
- She will not type passwords, OTPs, API keys, tokens, secrets, or credit card data into other apps.
- No destructive system commands are included.
- JANET does not run unknown shell commands from AI text.
- File writing is limited to explicit FASTA export commands, the local session log, and `JANET_Workspace`.
- Restart, shutdown, delete, and destructive system control are intentionally not implemented.

## Windows Installer

GitHub Actions builds:

```text
JANETSetup.exe
```

Latest release:

```text
https://github.com/meenavignesh-svg/HELIX_MINDBIO_AI/releases/latest
```
