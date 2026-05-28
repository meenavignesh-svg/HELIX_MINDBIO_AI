"""Light themed chat window for JANET."""

from __future__ import annotations

import queue
import threading
import tkinter as tk
from tkinter import scrolledtext, ttk

from ai_providers import AIProviderManager
from helixmind_bio_ai import HelixMindBioAI


class JanetChatApp:
    def __init__(self) -> None:
        self.assistant = HelixMindBioAI()
        self.ai = AIProviderManager()
        self.responses: queue.Queue[str] = queue.Queue()

        self.root = tk.Tk()
        self.root.title("JANET - Local OpenClaw-Style Desktop Agent")
        self.root.geometry("1040x760")
        self.root.minsize(820, 600)
        self.root.configure(bg="#f7faf9")

        self.header = tk.Frame(self.root, bg="#ffffff", height=76)
        self.header.pack(fill="x")
        self.header.pack_propagate(False)

        self.title = tk.Label(self.header, text="JANET", bg="#ffffff", fg="#111827", font=("Segoe UI", 22, "bold"))
        self.title.pack(side="left", padx=(24, 10))

        self.subtitle = tk.Label(
            self.header,
            text="Local OpenClaw-style agent: plan, chat, control apps, type, click, remember, and use optional AI",
            bg="#ffffff",
            fg="#4b5563",
            font=("Segoe UI", 10),
        )
        self.subtitle.pack(side="left", pady=(8, 0))

        self.settings = tk.Frame(self.root, bg="#eefaf6", padx=14, pady=10)
        self.settings.pack(fill="x", padx=18, pady=(14, 0))

        tk.Label(self.settings, text="AI", bg="#eefaf6", fg="#111827", font=("Segoe UI", 10, "bold")).pack(side="left", padx=(0, 8))
        self.provider = ttk.Combobox(self.settings, values=["local", "ollama", "openai", "gemini", "anthropic", "openrouter", "compatible"], width=12, state="readonly")
        self.provider.set("local")
        self.provider.pack(side="left", padx=(0, 8))

        self.model = tk.Entry(self.settings, width=22, bg="#ffffff", fg="#111827", relief="solid", bd=1)
        self.model.insert(0, "model optional")
        self.model.pack(side="left", padx=(0, 8), ipady=4)

        self.endpoint = tk.Entry(self.settings, width=30, bg="#ffffff", fg="#111827", relief="solid", bd=1)
        self.endpoint.insert(0, "endpoint optional")
        self.endpoint.pack(side="left", padx=(0, 8), ipady=4)

        self.api_key = tk.Entry(self.settings, width=26, bg="#ffffff", fg="#111827", relief="solid", bd=1, show="*")
        self.api_key.insert(0, "")
        self.api_key.pack(side="left", padx=(0, 8), ipady=4)

        self.save_ai = tk.Button(self.settings, text="Use AI", bg="#2563eb", fg="#ffffff", relief="flat", padx=14, pady=6, command=self.configure_ai)
        self.save_ai.pack(side="left")

        self.ai_status = tk.Label(self.settings, text=self.ai.status(), bg="#eefaf6", fg="#475569", font=("Segoe UI", 9))
        self.ai_status.pack(side="left", padx=(12, 0))

        self.chat = scrolledtext.ScrolledText(
            self.root,
            wrap="word",
            bg="#f7faf9",
            fg="#111827",
            insertbackground="#111827",
            relief="flat",
            padx=22,
            pady=18,
            font=("Segoe UI", 11),
        )
        self.chat.pack(fill="both", expand=True, padx=18, pady=(18, 8))
        self.chat.tag_configure("janet", foreground="#047857", font=("Segoe UI", 11, "bold"))
        self.chat.tag_configure("user", foreground="#2563eb", font=("Segoe UI", 11, "bold"))
        self.chat.tag_configure("body", foreground="#111827", font=("Segoe UI", 11))
        self.chat.configure(state="disabled")

        self.input_bar = tk.Frame(self.root, bg="#f7faf9")
        self.input_bar.pack(fill="x", padx=18, pady=(0, 18))

        self.entry = tk.Entry(self.input_bar, bg="#ffffff", fg="#111827", insertbackground="#111827", relief="solid", bd=1, font=("Segoe UI", 12))
        self.entry.pack(side="left", fill="x", expand=True, ipady=13)
        self.entry.bind("<Return>", self.send_message)

        self.send = tk.Button(self.input_bar, text="Send", bg="#10b981", fg="#ffffff", activebackground="#059669", activeforeground="#ffffff", relief="flat", padx=24, pady=12, font=("Segoe UI", 11, "bold"), command=self.send_message)
        self.send.pack(side="left", padx=(10, 0))

        self.add_message(
            "JANET",
            "Ready. I can plan locally, control desktop apps, run bioinformatics tools, and optionally use your chosen AI provider for reasoning. Keys stay in this app session unless you set environment variables yourself.",
            "janet",
        )
        self.root.after(100, self.poll_responses)

    def configure_ai(self) -> None:
        model = "" if self.model.get().strip() == "model optional" else self.model.get().strip()
        endpoint = "" if self.endpoint.get().strip() == "endpoint optional" else self.endpoint.get().strip()
        self.ai.configure(self.provider.get(), model=model, api_key=self.api_key.get(), endpoint=endpoint)
        self.ai_status.configure(text=self.ai.status())
        self.add_message("JANET", "AI settings updated for this session. I will still use local tools for desktop actions.", "janet")

    def add_message(self, speaker: str, text: str, tag: str) -> None:
        self.chat.configure(state="normal")
        self.chat.insert("end", f"{speaker}\n", tag)
        self.chat.insert("end", f"{text}\n\n", "body")
        self.chat.configure(state="disabled")
        self.chat.see("end")

    def send_message(self, event: object | None = None) -> None:
        text = self.entry.get().strip()
        if not text:
            return
        self.entry.delete(0, "end")
        shown_text = text if not self.looks_secret(text) else "[hidden sensitive input]"
        self.add_message("You", shown_text, "user")
        threading.Thread(target=self.run_command, args=(text,), daemon=True).start()

    def looks_secret(self, text: str) -> bool:
        lowered = text.lower()
        return any(word in lowered for word in ("api key", "password", "token", "secret", "credit card", "cvv"))

    def run_command(self, text: str) -> None:
        lowered = text.strip().lower()
        if lowered.startswith(("ask ai ", "ai ")):
            prompt = text.split(" ", 2)[-1]
            response = self.ai.ask(prompt)
            self.responses.put(response)
            return
        if lowered.startswith(("plan ", "make a plan ", "agent plan ")):
            goal = text.split(" ", 1)[1] if " " in text else text
            response = self.ai.ask("Create a short visible action plan for this desktop task. Do not include destructive or secret-handling steps. Goal: " + goal)
            self.responses.put(response)
            return
        response, keep_running = self.assistant.answer(text)
        self.responses.put(response)
        if not keep_running:
            self.root.after(500, self.root.destroy)

    def poll_responses(self) -> None:
        while not self.responses.empty():
            self.add_message("JANET", self.responses.get(), "janet")
        self.root.after(100, self.poll_responses)

    def run(self) -> None:
        self.entry.focus_set()
        self.root.mainloop()


if __name__ == "__main__":
    JanetChatApp().run()
