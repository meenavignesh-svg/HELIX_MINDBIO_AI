# HelixMind Bio AI Command Guide

Use `helix` before a command in voice mode. In text mode, either style works.

## Real-Time Presence

```text
helix status
helix project CRISPR off-target study
helix presence on
helix quiet mode
helix what are you doing
helix are you there
```

## Session Notes

```text
helix note extracted sample from patient dataset
helix show notes
```

## Job Queue

```text
helix add job gc content of ATGCGCGTTA
helix add job primer stats ATGCGTACGTAGCTAGCTA
helix add job write file plan.txt with analyze FASTA and design primers
helix show jobs
helix run jobs
helix clear jobs
```

## General Safe Work

```text
helix create folder crispr_project
helix write file notes.txt with today I checked primer GC
helix read file notes.txt
helix list files
helix list files crispr_project
helix make checklist collect FASTA, run GC, design primers
helix summarize text paste your paragraph here
helix draft email I finished the sequence report and primer check
```

## Apps And Websites

```text
helix open app notepad
helix open app calculator
helix open app paint
helix open app explorer
helix open app chrome
helix open app vscode
helix open google
helix open youtube
helix open github
helix open chatgpt
helix search web for ncbi blast tutorial
```

## Core

```text
helix help
helix time
helix exit
```

## Sequence Analysis

```text
helix report ATGCGCGTTA
helix gc content of ATGCGCGTTA
helix reverse complement of ATGCCGTA
helix transcribe ATGCCGTA
helix translate dna ATGGCCATTGTA
helix longest orf of AAATGAAATTTTAA
```

## Bioinformatics Utilities

```text
helix codon usage ATGGCCATTGTA
helix restriction scan GAATTCGGATCC
helix primer stats ATGCGTACGTAGCTAGCTA
helix find motif ATG in CCCAATGTTTATG
helix kmer count 3 ATGCGCGTTA
helix protein weight of MTEYK
helix compare ATGCC with ATGCA
helix align ATGCC with ATGCA
```

## FASTA

```text
helix summarize fasta C:\path\to\file.fasta
helix save fasta ATGCGT named sample1 to C:\path\sample.fasta
```

## Science Websites

```text
helix open ncbi
helix open blast
helix open uniprot
helix open ensembl
helix open pdb
helix open pubmed
helix search pubmed for crispr diagnostics
```

## Safety Limits

HelixMind will not delete files, restart/shutdown the computer, run unknown shell commands, or silently control private files. General file writing is limited to `HelixMind_Workspace`.
