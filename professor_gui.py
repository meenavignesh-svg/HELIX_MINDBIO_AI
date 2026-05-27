"""Tkinter desktop interface with animated biotech visuals."""

from __future__ import annotations

import math
import threading
import tkinter as tk
from tkinter import messagebox, scrolledtext

from commands import handle_command
from permissions import PERMISSIONS_FILE, PROMPTS, load_permissions, save_permissions
from speech import Speech


class ProfessorApp:
    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title("Professor Voice Assistant")
        self.root.geometry("1100x720")
        self.root.minsize(900, 620)
        self.root.configure(bg="#071014")
        self.angle = 0.0
        self.permissions = self._permission_setup()
        self.speech: Speech | None = None
        self.voice_running = False
        self._build_layout()
        self._animate()

    def _permission_setup(self) -> dict[str, bool]:
        permissions = load_permissions()
        if PERMISSIONS_FILE.exists():
            return permissions
        messagebox.showinfo("Professor privacy setup", "Professor will ask what she can access. Choices stay local on this computer.")
        for key, question in PROMPTS.items():
            permissions[key] = messagebox.askyesno("Local permission", question)
        save_permissions(permissions)
        return permissions

    def _build_layout(self) -> None:
        self.root.columnconfigure(0, weight=3)
        self.root.columnconfigure(1, weight=2)
        self.root.rowconfigure(0, weight=1)
        visual_panel = tk.Frame(self.root, bg="#071014")
        visual_panel.grid(row=0, column=0, sticky="nsew", padx=(18, 9), pady=18)
        visual_panel.rowconfigure(1, weight=1)
        visual_panel.columnconfigure(0, weight=1)
        tk.Label(visual_panel, text="Professor", bg="#071014", fg="#d8fff1", font=("Segoe UI", 34, "bold")).grid(row=0, column=0, sticky="w")
        tk.Label(visual_panel, text="Local biotech voice assistant", bg="#071014", fg="#7ad7c4", font=("Segoe UI", 13)).grid(row=0, column=0, sticky="w", pady=(48, 0))
        self.canvas = tk.Canvas(visual_panel, bg="#071014", highlightthickness=0)
        self.canvas.grid(row=1, column=0, sticky="nsew", pady=(18, 0))
        side = tk.Frame(self.root, bg="#0d1b22")
        side.grid(row=0, column=1, sticky="nsew", padx=(9, 18), pady=18)
        side.columnconfigure(0, weight=1)
        side.rowconfigure(4, weight=1)
        tk.Label(side, text="Local Control", bg="#0d1b22", fg="#f4fbf8", font=("Segoe UI", 19, "bold")).grid(row=0, column=0, sticky="w", padx=18, pady=(18, 4))
        tk.Label(side, text="Stays local. Cloud AI is off unless allowed.", bg="#0d1b22", fg="#9bb8b0", wraplength=380, justify="left", font=("Segoe UI", 10)).grid(row=1, column=0, sticky="w", padx=18, pady=(0, 14))
        self.command = tk.Entry(side, bg="#13252d", fg="#ffffff", insertbackground="#ffffff", relief="flat", font=("Segoe UI", 12))
        self.command.grid(row=2, column=0, sticky="ew", padx=18, ipady=12)
        self.command.insert(0, "professor gc content of ATGCGCGTTA")
        self.command.bind("<Return>", lambda _event: self.run_text_command())
        buttons = tk.Frame(side, bg="#0d1b22")
        buttons.grid(row=3, column=0, sticky="ew", padx=18, pady=12)
        buttons.columnconfigure(0, weight=1)
        buttons.columnconfigure(1, weight=1)
        tk.Button(buttons, text="Run Command", command=self.run_text_command, bg="#34d399", fg="#062016", activebackground="#5eead4", relief="flat", font=("Segoe UI", 11, "bold"), padx=12, pady=10).grid(row=0, column=0, sticky="ew", padx=(0, 6))
        tk.Button(buttons, text="Start Voice", command=self.start_voice, bg="#38bdf8", fg="#061722", activebackground="#7dd3fc", relief="flat", font=("Segoe UI", 11, "bold"), padx=12, pady=10).grid(row=0, column=1, sticky="ew", padx=(6, 0))
        self.log = scrolledtext.ScrolledText(side, bg="#071014", fg="#e5fff8", insertbackground="#ffffff", relief="flat", font=("Consolas", 10), wrap="word")
        self.log.grid(row=4, column=0, sticky="nsew", padx=18, pady=(0, 18))
        self._log("Professor is ready.")
        self._log("Try: professor explain bioinformatics")

    def _log(self, text: str) -> None:
        self.log.insert("end", text + "\n")
        self.log.see("end")

    def _clean_command(self, text: str) -> str:
        text = text.strip().lower()
        if text.startswith("professor"):
            return text.replace("professor", "", 1).strip(" ,")
        return text

    def run_text_command(self) -> None:
        raw = self.command.get()
        response, _running = handle_command(self._clean_command(raw), self.permissions)
        self._log(f"You: {raw}")
        self._log(f"Professor: {response}")

    def start_voice(self) -> None:
        if self.voice_running:
            self._log("Voice mode is already listening.")
            return
        self.voice_running = True
        self._log("Voice mode started. Say Professor, then your command.")
        threading.Thread(target=self._voice_loop, daemon=True).start()

    def _voice_loop(self) -> None:
        if self.speech is None:
            self.speech = Speech()
        self.speech.say("Professor voice mode is ready.")
        while self.voice_running:
            heard = self.speech.listen()
            if not heard or "professor" not in heard:
                continue
            response, running = handle_command(self._clean_command(heard), self.permissions)
            self.root.after(0, self._log, f"You: {heard}")
            self.root.after(0, self._log, f"Professor: {response}")
            self.speech.say(response)
            if not running:
                self.voice_running = False

    def _animate(self) -> None:
        self.canvas.delete("all")
        width = max(self.canvas.winfo_width(), 640)
        height = max(self.canvas.winfo_height(), 420)
        cx = width / 2
        cy = height / 2
        scale = min(width, height) / 5
        self.canvas.create_oval(cx - scale * 2.0, cy - scale * 1.45, cx + scale * 2.0, cy + scale * 1.45, outline="#16343b", width=2)
        points = []
        for index in range(34):
            y = cy - scale * 1.25 + index * (scale * 2.5 / 33)
            phase = self.angle + index * 0.46
            depth = math.cos(phase)
            radius = scale * (0.72 + depth * 0.18)
            x1 = cx + math.sin(phase) * radius
            x2 = cx + math.sin(phase + math.pi) * radius
            color = "#7dd3fc" if depth > 0 else "#34d399"
            size = 5 + depth * 2
            points.append((x1, y, x2, y))
            self.canvas.create_line(x1, y, x2, y, fill="#25535a", width=2)
            self.canvas.create_oval(x1 - size, y - size, x1 + size, y + size, fill=color, outline="")
            self.canvas.create_oval(x2 - size, y - size, x2 + size, y + size, fill="#f0abfc", outline="")
        for strand in (0, 2):
            previous = None
            for x1, y1, x2, y2 in points:
                x = x1 if strand == 0 else x2
                if previous:
                    self.canvas.create_line(previous[0], previous[1], x, y1, fill="#d8fff1", width=2)
                previous = (x, y1)
        for ring in range(6):
            pulse = (math.sin(self.angle * 1.7 + ring) + 1) / 2
            r = scale * (1.55 + ring * 0.13 + pulse * 0.04)
            self.canvas.create_oval(cx - r * 1.45, cy - r, cx + r * 1.45, cy + r, outline="#12333a", width=1)
        self.canvas.create_text(cx, height - 48, text="Animated local biotech core", fill="#87f7df", font=("Segoe UI", 14, "bold"))
        self.angle += 0.055
        self.root.after(33, self._animate)

    def run(self) -> None:
        self.root.mainloop()


def run_app() -> None:
    ProfessorApp().run()
