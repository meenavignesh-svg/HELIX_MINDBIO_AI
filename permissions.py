"""Local permission prompts for Professor.

Choices are stored on this computer only in a small JSON file next to the app.
"""

from __future__ import annotations

import json
from pathlib import Path


PERMISSIONS_FILE = Path("professor_permissions.json")

DEFAULT_PERMISSIONS = {
    "microphone": False,
    "voice_output": True,
    "open_apps": False,
    "open_websites": False,
    "create_folders": False,
    "bioinformatics_tools": True,
    "cloud_ai": False,
}

PROMPTS = {
    "microphone": "Allow Professor to listen through your microphone?",
    "open_apps": "Allow Professor to open local apps like Chrome and VS Code?",
    "open_websites": "Allow Professor to open websites in your browser?",
    "create_folders": "Allow Professor to create folders inside your Documents folder?",
    "bioinformatics_tools": "Allow Professor to run offline bioinformatics tools?",
    "cloud_ai": "Allow Professor to use OpenAI/Gemini if API keys exist? This is not fully local.",
}


def load_permissions() -> dict[str, bool]:
    if not PERMISSIONS_FILE.exists():
        return DEFAULT_PERMISSIONS.copy()

    try:
        saved = json.loads(PERMISSIONS_FILE.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return DEFAULT_PERMISSIONS.copy()

    permissions = DEFAULT_PERMISSIONS.copy()
    permissions.update({key: bool(value) for key, value in saved.items()})
    return permissions


def save_permissions(permissions: dict[str, bool]) -> None:
    PERMISSIONS_FILE.write_text(json.dumps(permissions, indent=2), encoding="utf-8")


def ask_yes_no(question: str) -> bool:
    answer = input(f"{question} [y/N]: ").strip().lower()
    return answer in {"y", "yes"}


def first_run_setup() -> dict[str, bool]:
    permissions = load_permissions()
    if PERMISSIONS_FILE.exists():
        return permissions

    print("Professor privacy setup")
    print("Your choices stay local in professor_permissions.json.")
    print("You can edit or delete that file later to reset permissions.")
    print()

    for key, question in PROMPTS.items():
        permissions[key] = ask_yes_no(question)

    save_permissions(permissions)
    return permissions


def allowed(permissions: dict[str, bool], key: str) -> bool:
    return bool(permissions.get(key, False))
