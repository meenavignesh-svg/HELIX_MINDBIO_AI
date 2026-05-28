# HelixMind Bio AI

**HelixMind Bio AI** is a local-first Windows assistant for bioinformatics and desktop work. She is designed to feel like a real-time worker living in your computer: always ready in the console, accepting text or voice commands, opening apps, typing into the active window, keeping session notes, queueing jobs, handling files in her workspace, and processing sequence tasks locally.

Wake word: `helix`

## What She Can Control

HelixMind can now use desktop-control commands:

- open installed apps through Windows search
- type or paste text into the active window
- press keys
- use keyboard shortcuts
- click the mouse
- wait between actions
- queue desktop actions with other jobs

She still blocks passwords, OTPs, API keys, secrets, destructive actions, and hidden background control.

## Desktop Control Commands

```text
helix desktop status
helix open any app chrome
helix open any app notepad
helix type text Hello, I am HelixMind.
helix paste text This goes into the active window.
helix press key enter
helix hotkey ctrl+s
helix wait 2
helix click
helix click 500 300
```

Example workflow:

```text
helix add job open any app notepad
helix add job wait 2
helix add job type text HelixMind is working inside this computer.
helix add job hotkey ctrl+s
helix run jobs
```

## Personality

HelixMind is not just a generic Jarvis clone. She is a focused local coworker for bioinformatics, research support, notes, folders, simple files, app control, typing, web searches, and lightweight productivity.

She can:

- stay open in text or voice mode
- report what she is doing with `helix status`
- remember session notes while running
- queue multiple jobs and process them together
- write a local session log to `helixmind_session_log.txt`
- create and read files inside `HelixMind_Workspace`
- open apps and useful websites
- type into the current active app window
- work offline for core DNA/RNA/protein analysis

## Bioinformatics

HelixMind Bio AI can help with:

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

## General Work

```text
helix create folder crispr_project
helix write file notes.txt with today I checked primer GC
helix read file notes.txt
helix list files
helix make checklist collect FASTA, run GC, design primers
helix summarize text paste your paragraph here
helix draft email I finished the sequence report and primer check
helix open google
helix open github
helix search web for ncbi blast tutorial
```

## Bioinformatics Examples

```text
helix report ATGCGCGTTA
helix gc content of ATGCGCGTTA
helix reverse complement of ATGCCGTA
helix translate dna ATGGCCATTGTA
helix codon usage ATGGCCATTGTA
helix restriction scan GAATTCGGATCC
helix primer stats ATGCGTACGTAGCTAGCTA
helix summarize fasta C:\path\to\file.fasta
helix search pubmed for crispr diagnostics
```

## Quick Start

1. Install Python 3.10+ and tick **Add python.exe to PATH**.
2. Double-click `install_helixmind_bio_ai.bat`.
3. Double-click `HelixMindBioAI.bat`.
4. Choose `text` or `voice` mode.

If desktop control says dependencies are missing, run `install_helixmind_bio_ai.bat` again.

## Local-First Privacy

The built-in bioinformatics tools run on the computer. HelixMind Bio AI does not upload your sequences to a cloud service. Browser-opening commands only open websites in your browser.

She does not watch private files automatically. You give her a folder, sequence, FASTA path, active window, or command when you want work done.

## Safety Rules

- No API keys are hardcoded.
- She will not type passwords, OTPs, API keys, tokens, or secrets.
- No destructive system commands are included.
- The assistant does not run unknown shell commands from generated text.
- File writing is limited to explicit FASTA export commands, the local session log, and `HelixMind_Workspace`.
- Restart, shutdown, delete, and system-control destruction are intentionally not implemented.

## Windows Installer

The included GitHub Actions workflow builds a Windows installer:

```text
.github/workflows/build-helixmind-bio-ai-installer.yml
```

When the workflow succeeds, it publishes `HelixMindBioAISetup.exe` in the latest release.

Latest release:

```text
https://github.com/meenavignesh-svg/HELIX_MINDBIO_AI/releases/latest
```
