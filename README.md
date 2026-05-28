# JANET Bio AI

**JANET** is a light-themed, local-first Windows assistant for bioinformatics and desktop work. She is designed to feel like a fast real-time worker living in your computer: ready in the console, accepting text or voice commands, opening apps, typing into the active window, keeping session notes, queueing jobs, handling files in her workspace, and processing sequence tasks locally.

Wake word: `janet`

Legacy wake word: `helix` still works.

## Light Theme

JANET applies a light Windows console theme at startup:

```text
white background + black text
window title: JANET - Bioinformatics Desktop Assistant
workspace: JANET_Workspace
session log: janet_session_log.txt
```

Use this anytime:

```text
janet light theme
```

## What She Can Control

JANET can use desktop-control commands:

- open installed apps through Windows search
- type or paste text into the active window
- press keys
- use keyboard shortcuts
- click the mouse
- wait between actions
- queue desktop actions with other jobs

She still blocks passwords, OTPs, API keys, secrets, credit card details, destructive actions, and hidden background control.

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

Example workflow:

```text
janet add job open any app notepad
janet add job wait 0.5
janet add job type text JANET is working inside this computer.
janet add job hotkey ctrl+s
janet run jobs
```

## Personality

JANET is a focused local coworker for bioinformatics, research support, notes, folders, simple files, app control, typing, web searches, and lightweight productivity.

She can:

- stay open in text or voice mode
- work fast by default
- report status with `janet status`
- remember session notes while running
- queue multiple jobs and process them together
- write a local session log to `janet_session_log.txt`
- create and read files inside `JANET_Workspace`
- open apps and useful websites
- type into the current active app window
- work offline for core DNA/RNA/protein analysis

## Bioinformatics

JANET can help with:

- DNA/RNA cleanup and sequence reports
- GC and AT content
- reverse complement
- DNA to RNA transcription
- DNA translation
- longest ORF detection
- codon usage summaries
- motif search
- k-mer counting
- primer statistics and estimated Tm
- common restriction enzyme site scanning
- FASTA summaries with total bases and N50
- protein molecular weight estimation
- quick sequence comparison
- simple global alignment scoring
- PubMed, NCBI, BLAST, UniProt, Ensembl, and PDB opening/searching

## Quick Start

1. Install Python 3.10+ and tick **Add python.exe to PATH**.
2. Double-click `install_helixmind_bio_ai.bat`.
3. Double-click `HelixMindBioAI.bat`.
4. Choose `text` or `voice` mode.

If desktop control says dependencies are missing, run `install_helixmind_bio_ai.bat` again.

## Fast Mode

Fast mode is on by default. It turns off voice output in text mode, reduces desktop delays, and keeps responses short.

```text
janet fast mode
janet normal mode
janet voice output off
janet voice output on
```

## Safety Rules

- No API keys are hardcoded.
- She will not type passwords, OTPs, API keys, tokens, secrets, or credit card data.
- No destructive system commands are included.
- The assistant does not run unknown shell commands from generated text.
- File writing is limited to explicit FASTA export commands, the local session log, and `JANET_Workspace`.
- Restart, shutdown, delete, and system-control destruction are intentionally not implemented.

## Latest Release

```text
https://github.com/meenavignesh-svg/HELIX_MINDBIO_AI/releases/latest
```
