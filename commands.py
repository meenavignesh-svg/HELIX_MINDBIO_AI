"""Safe Windows command handlers for Professor."""

from __future__ import annotations

import datetime as dt
import os
import subprocess
import webbrowser
from pathlib import Path

import bioinformatics
import config


SAFE_FOLDER_ROOT = Path.home() / "Documents" / "Professor Folders"


def open_chrome() -> str:
    chrome_paths = [
        os.getenv("ProgramFiles", "") + r"\Google\Chrome\Application\chrome.exe",
        os.getenv("ProgramFiles(x86)", "") + r"\Google\Chrome\Application\chrome.exe",
    ]
    for path in chrome_paths:
        if path and Path(path).exists():
            subprocess.Popen([path])
            return "Opening Chrome."

    webbrowser.open("https://www.google.com")
    return "Chrome was not found directly, so I opened Google in your default browser."


def open_vscode() -> str:
    try:
        subprocess.Popen(["code"])
        return "Opening Visual Studio Code."
    except FileNotFoundError:
        return "VS Code command was not found. Install VS Code and enable the code command in PATH."


def open_youtube() -> str:
    webbrowser.open("https://www.youtube.com")
    return "Opening YouTube."


def search_google(query: str) -> str:
    cleaned = query.strip()
    if not cleaned:
        return "Tell me what to search for."
    webbrowser.open(f"https://www.google.com/search?q={cleaned.replace(' ', '+')}")
    return f"Searching Google for {cleaned}."


def create_folder(name: str) -> str:
    safe_name = "".join(ch for ch in name if ch.isalnum() or ch in (" ", "-", "_")).strip()
    if not safe_name:
        return "Please say a simple folder name."

    SAFE_FOLDER_ROOT.mkdir(parents=True, exist_ok=True)
    folder = SAFE_FOLDER_ROOT / safe_name
    folder.mkdir(exist_ok=True)
    return f"Created folder {folder}."


def tell_time() -> str:
    current_time = dt.datetime.now().strftime("%I:%M %p")
    return f"The time is {current_time}."


def open_folder() -> str:
    SAFE_FOLDER_ROOT.mkdir(parents=True, exist_ok=True)
    os.startfile(SAFE_FOLDER_ROOT)  # type: ignore[attr-defined]
    return f"Opening {SAFE_FOLDER_ROOT}."


def optional_ai_answer(prompt: str) -> str:
    """Use cloud AI only when an API key exists. Never run AI output as commands."""
    if not config.has_cloud_ai():
        return "Cloud AI is not configured. I can still help with local commands."

    if config.OPENAI_API_KEY:
        try:
            from openai import OpenAI

            client = OpenAI(api_key=config.OPENAI_API_KEY)
            response = client.responses.create(
                model=config.OPENAI_MODEL,
                instructions="You are Professor, a concise, safe, voice-first Windows desktop assistant.",
                input=prompt,
            )
            return response.output_text or "I did not get a response."
        except Exception as exc:
            return f"OpenAI mode failed: {exc}"

    if config.GEMINI_API_KEY:
        try:
            import google.generativeai as genai

            genai.configure(api_key=config.GEMINI_API_KEY)
            model = genai.GenerativeModel(config.GEMINI_MODEL)
            response = model.generate_content(prompt)
            return response.text or "I did not get a response."
        except Exception as exc:
            return f"Gemini mode failed: {exc}"

    return "Cloud AI is not available right now."


def handle_command(command: str) -> tuple[str, bool]:
    """Return a spoken response and whether the app should keep running."""
    command = command.lower().strip()

    if not command:
        return "I did not catch that.", True
    if command in {"exit", "quit", "stop professor", "goodbye"}:
        return "Goodbye.", False
    if "open chrome" in command:
        return open_chrome(), True
    if "open vscode" in command or "open vs code" in command:
        return open_vscode(), True
    if "open youtube" in command:
        return open_youtube(), True
    if command.startswith("search google for "):
        return search_google(command.replace("search google for ", "", 1)), True
    if command.startswith("create folder "):
        return create_folder(command.replace("create folder ", "", 1)), True
    if "open folders" in command or "open folder" in command:
        return open_folder(), True
    if "tell time" in command or "what time" in command:
        return tell_time(), True
    if "what is bioinformatics" in command or "explain bioinformatics" in command:
        return bioinformatics.explain_bioinformatics(), True
    if command.startswith("gc content of "):
        return bioinformatics.gc_content(command.replace("gc content of ", "", 1)), True
    if command.startswith("reverse complement of "):
        return bioinformatics.reverse_complement(command.replace("reverse complement of ", "", 1)), True
    if command.startswith("transcribe "):
        return bioinformatics.transcribe(command.replace("transcribe ", "", 1)), True
    if command.startswith("translate dna "):
        return bioinformatics.translate_dna(command.replace("translate dna ", "", 1)), True
    if "shutdown" in command or "restart" in command:
        return "I will not shut down or restart without a separate confirmation feature.", True

    return optional_ai_answer(command), True
