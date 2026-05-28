"""Light themed chat window for JANET."""

from __future__ import annotations

import queue
import threading
import tkinter as tk
from tkinter import scrolledtext

from helixmind_bio_ai import HelixMindBioAI


class JanetChatApp:
    def __init__(self) -> None:
        self.assistant = HelixMindBioAI()
        self.responses: queue.Queue[str] = queue.Queue()

        self.root = tk.Tk()
        self.root.title("JANET - Bioinformatics Desktop Assistant")
        self.root.geometry("920x680")
        self.root.minsize(720, 520)
        self.root.configure(bg="#f7faf9")

        self.header = tk.Frame(self.root, bg="#ffffff", height=72)
        self.header.pack(fill="x")
        self.header.pack_propagate(False)

        self.title = tk.Label(
            self.header,
            text="JANET",
            bg="#ffffff",
            fg="#111827",
            font=("Segoe UI", 22, "bold"),
        )
        self.title.pack(side="left", padx=(24, 10))

        self.subtitle = tk.Label(
            self.header,
            text="Fast local assistant for bioinformatics and desktop work",
            bg="#ffffff",
            fg="#4b5563",
            font=("Segoe UI", 10),
        )
        self.subtitle.pack(side="left", pady=(8, 0))

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

        self.entry = tk.Entry(
            self.input_bar,
            bg="#ffffff",
            fg="#111827",
            insertbackground="#111827",
            relief="solid",
            bd=1,
            font=("Segoe UI", 12),
        )
        self.entry.pack(side="left", fill="x", expand=True, ipady=13)
        self.entry.bind("<Return>", self.send_message)

        self.send = tk.Button(
            self.input_bar,
            text="Send",
            bg="#10b981",
            fg="#ffffff",
            activebackground="#059669",
            activeforeground="#ffffff",
            relief="flat",
            padx=24,
            pady=12,
            font=("Segoe UI", 11, "bold"),
            command=self.send_message,
        )
        self.send.pack(side="left", padx=(10, 0))

        self.add_message("JANET", "Ready. Ask me to analyze sequences, open apps, type text, or run queued jobs.", "janet")
        self.root.after(100, self.poll_responses)

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
        self.add_message("You", text, "user")
        threading.Thread(target=self.run_command, args=(text,), daemon=True).start()

    def run_command(self, text: str) -> None:
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
