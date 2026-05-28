# JANET Bio AI

**JANET** is a light-themed, local-first Windows assistant for bioinformatics and desktop work. She has a ChatGPT-like desktop chat window, a proper desktop shortcut icon, fast command execution, and local bioinformatics tools.

Wake word: `janet`

Legacy wake word: `helix` still works.

## What Is New

- Light ChatGPT-like desktop chat window
- JANET desktop shortcut icon
- Windows installer builds `JANETSetup.exe`
- Fast mode on by default
- Local workspace: `JANET_Workspace`
- Local session log: `janet_session_log.txt`

## Desktop App

After installing, open **JANET** from the Start Menu or desktop shortcut.

The app opens a light chat window where you can type commands like:

```text
janet status
janet open any app chrome
janet type text Hello, I am JANET.
janet gc content of ATGCGCGTTA
janet search pubmed for crispr diagnostics
```

## Icon

JANET uses a clean light bio/AI icon with rounded science-node geometry. It intentionally avoids swastika-like or extremist-looking shapes.

Source icon asset:

```text
assets/janet_icon.svg
```

Build icon generated during installer build:

```text
assets/janet_icon.ico
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

## Quick Start From Source

1. Install Python 3.10+ and tick **Add python.exe to PATH**.
2. Double-click `install_helixmind_bio_ai.bat`.
3. Double-click `HelixMindBioAI.bat`.

## Windows Installer

GitHub Actions builds a Windows installer:

```text
JANETSetup.exe
```

Latest release:

```text
https://github.com/meenavignesh-svg/HELIX_MINDBIO_AI/releases/latest
```

Workflow:

```text
.github/workflows/build-helixmind-bio-ai-installer.yml
```

## Safety Rules

- No API keys are hardcoded.
- She will not type passwords, OTPs, API keys, tokens, secrets, or credit card data.
- No destructive system commands are included.
- The assistant does not run unknown shell commands from generated text.
- File writing is limited to explicit FASTA export commands, the local session log, and `JANET_Workspace`.
- Restart, shutdown, delete, and system-control destruction are intentionally not implemented.
