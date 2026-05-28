"""HelixMind Bio AI - local voice/text assistant for bioinformatics work."""

from __future__ import annotations

import datetime as dt
import os
import re
import subprocess
import webbrowser
from pathlib import Path

import pyttsx3
import speech_recognition as sr

import bioinformatics_tools as bio

WAKE_WORD = "helix"
APP_NAME = "HelixMind Bio AI"


class HelixMindBioAI:
    def __init__(self) -> None:
        self.engine = pyttsx3.init()
        self.engine.setProperty("rate", 172)
        self.recognizer = sr.Recognizer()
        self.session_notes: list[str] = []

    def speak(self, text: str) -> None:
        print(f"\n{APP_NAME}: {text}\n")
        try:
            self.engine.say(text.replace("\n", ". "))
            self.engine.runAndWait()
        except Exception:
            print("Voice output is unavailable, but text mode is still working.")

    def listen(self) -> str:
        with sr.Microphone() as source:
            print("Listening...")
            self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
            audio = self.recognizer.listen(source, timeout=6, phrase_time_limit=12)
        try:
            text = self.recognizer.recognize_google(audio)
            print(f"You: {text}")
            return text.lower().strip()
        except Exception:
            return ""

    def normalize(self, command: str) -> str:
        command = command.lower().strip()
        if command.startswith(WAKE_WORD):
            command = command.replace(WAKE_WORD, "", 1).strip(" ,")
        return command

    def answer(self, command: str) -> tuple[str, bool]:
        command = self.normalize(command)

        if command in {"exit", "quit", "stop", "sleep"}:
            return "Session saved in memory only. Goodbye.", False
        if command in {"help", "commands", "what can you do"}:
            return self.help_text(), True
        if "time" in command:
            return f"The time is {dt.datetime.now().strftime('%I:%M %p')}.", True

        site_response = self.open_science_site(command)
        if site_response:
            return site_response, True

        if command.startswith("note "):
            note = command.replace("note ", "", 1).strip()
            self.session_notes.append(note)
            return f"Added session note {len(self.session_notes)}.", True
        if command in {"show notes", "list notes"}:
            if not self.session_notes:
                return "No session notes yet.", True
            return "Session notes:\n" + "\n".join(f"{i + 1}. {note}" for i, note in enumerate(self.session_notes)), True
        if command.startswith("open folder "):
            return self.open_folder(command.replace("open folder ", "", 1)), True

        if "explain bioinformatics" in command:
            return "Bioinformatics uses computing to study DNA, RNA, proteins, variants, genomes, and biological datasets.", True
        if command.startswith("report "):
            return bio.sequence_report(command.replace("report ", "", 1)), True
        if command.startswith("gc content of "):
            return bio.gc_content(command.replace("gc content of ", "", 1)), True
        if command.startswith("reverse complement of "):
            return bio.reverse_complement(command.replace("reverse complement of ", "", 1)), True
        if command.startswith("transcribe "):
            return bio.transcribe(command.replace("transcribe ", "", 1)), True
        if command.startswith("translate dna "):
            return bio.translate_dna(command.replace("translate dna ", "", 1)), True
        if command.startswith("longest orf of "):
            return bio.longest_orf(command.replace("longest orf of ", "", 1)), True
        if command.startswith("protein weight of "):
            return bio.protein_weight(command.replace("protein weight of ", "", 1)), True
        if command.startswith("primer stats "):
            return bio.primer_stats(command.replace("primer stats ", "", 1)), True
        if command.startswith("restriction scan "):
            return bio.restriction_scan(command.replace("restriction scan ", "", 1)), True
        if command.startswith("codon usage "):
            return bio.codon_usage(command.replace("codon usage ", "", 1)), True
        if command.startswith("kmer count "):
            return self.handle_kmers(command), True
        if command.startswith("find motif "):
            return self.handle_motif(command), True
        if command.startswith("compare "):
            return self.handle_compare(command), True
        if command.startswith("summarize fasta "):
            try:
                return bio.summarize_fasta(command.replace("summarize fasta ", "", 1)), True
            except Exception as exc:
                return f"Could not read FASTA file: {exc}", True
        if command.startswith("save fasta "):
            return self.handle_save_fasta(command), True
        if command.startswith("align "):
            return self.handle_alignment(command), True

        return self.help_text(), True

    def open_science_site(self, command: str) -> str | None:
        sites = {
            "open ncbi": "https://www.ncbi.nlm.nih.gov/",
            "open uniprot": "https://www.uniprot.org/",
            "open blast": "https://blast.ncbi.nlm.nih.gov/",
            "open ensembl": "https://www.ensembl.org/",
            "open pdb": "https://www.rcsb.org/",
            "open pubmed": "https://pubmed.ncbi.nlm.nih.gov/",
        }
        for phrase, url in sites.items():
            if phrase in command:
                webbrowser.open(url)
                return f"Opening {phrase.replace('open ', '').upper()}."
        if command.startswith("search pubmed for "):
            query = command.replace("search pubmed for ", "", 1).strip()
            webbrowser.open("https://pubmed.ncbi.nlm.nih.gov/?term=" + query.replace(" ", "+"))
            return f"Searching PubMed for {query}."
        return None

    def open_folder(self, folder_text: str) -> str:
        path = Path(folder_text.strip().strip('"')).expanduser()
        if not path.exists():
            return f"Folder not found: {path}"
        subprocess.Popen(f'explorer "{path}"')
        return f"Opening folder: {path}"

    def handle_kmers(self, command: str) -> str:
        payload = command.replace("kmer count ", "", 1)
        parts = payload.split(" ", 1)
        if parts and parts[0].isdigit() and len(parts) == 2:
            return bio.kmer_counts(parts[1], int(parts[0]))
        return bio.kmer_counts(payload)

    def handle_motif(self, command: str) -> str:
        payload = command.replace("find motif ", "", 1)
        if " in " not in payload:
            return "Use: find motif ATG in ATGCGTATG"
        motif, sequence = payload.split(" in ", 1)
        return bio.find_motif(sequence, motif)

    def handle_compare(self, command: str) -> str:
        payload = command.replace("compare ", "", 1)
        if " with " not in payload:
            return "Use: compare ATGCC with ATGCA"
        seq_a, seq_b = payload.split(" with ", 1)
        return bio.compare_sequences(seq_a, seq_b)

    def handle_alignment(self, command: str) -> str:
        payload = command.replace("align ", "", 1)
        if " with " not in payload:
            return "Use: align ATGCC with ATGCA"
        seq_a, seq_b = payload.split(" with ", 1)
        return bio.global_align(seq_a, seq_b)

    def handle_save_fasta(self, command: str) -> str:
        match = re.match(r"save fasta (.+?) named (.+?) to (.+)", command)
        if not match:
            return "Use: save fasta ATGCGT named sample1 to C:\\path\\sample.fasta"
        sequence, name, path = match.groups()
        try:
            return bio.write_fasta(path, name, sequence)
        except Exception as exc:
            return f"Could not save FASTA file: {exc}"

    def help_text(self) -> str:
        return (
            "I can work offline with DNA, RNA, protein, and FASTA tasks. Try:\n"
            "helix report ATGCGCGTTA\n"
            "helix gc content of ATGCGCGTTA\n"
            "helix reverse complement of ATGCCGTA\n"
            "helix translate dna ATGGCCATTGTA\n"
            "helix codon usage ATGGCCATTGTA\n"
            "helix restriction scan GAATTCGGATCC\n"
            "helix primer stats ATGCGTACGTAGCTAGCTA\n"
            "helix compare ATGCC with ATGCA\n"
            "helix search pubmed for crispr diagnostics"
        )

    def run_text_mode(self) -> None:
        self.speak(f"{APP_NAME} text mode is ready. Type help for commands.")
        while True:
            command = input("You: ")
            response, keep_running = self.answer(command)
            self.speak(response)
            if not keep_running:
                break

    def run_voice_mode(self) -> None:
        self.speak(f"{APP_NAME} voice mode is ready. Say Helix, then your command.")
        while True:
            command = self.listen()
            if not command or WAKE_WORD not in command:
                continue
            response, keep_running = self.answer(command)
            self.speak(response)
            if not keep_running:
                break


if __name__ == "__main__":
    assistant = HelixMindBioAI()
    preferred_mode = os.getenv("HELIXMIND_MODE", "").strip().lower()
    mode = preferred_mode or input("Type mode or voice mode? [text/voice]: ").strip().lower()
    if mode.startswith("v"):
        assistant.run_voice_mode()
    else:
        assistant.run_text_mode()
