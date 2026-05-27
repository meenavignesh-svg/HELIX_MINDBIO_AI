"""Configuration helpers for Professor.

API keys are read from environment variables only. Nothing sensitive should be
stored in this project.
"""

import os


WAKE_WORD = "professor"
ASSISTANT_NAME = "Professor"

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "").strip()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "").strip()

OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")


def has_cloud_ai() -> bool:
    """Return True when at least one supported cloud AI key is available."""
    return bool(OPENAI_API_KEY or GEMINI_API_KEY)
