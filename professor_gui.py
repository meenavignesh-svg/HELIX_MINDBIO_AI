"""Tkinter desktop interface with animated biotech visuals."""

from __future__ import annotations

import math
import threading
import time
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
        self.root.minsize(360, 150)
        self.root.configure(bg="#071014")
        self.angle = 0.0
        self.compact = False
        self.last_activity = time.time()
        self.permissions = self._permission_setup()
        self.speech: Speech | None = None
        self.voice_running = False
        self._build_layout()
        self._animate()
        self._worker_tick()

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
        for child in self.root.winfo_children():
            child.destroy()
        self.root.columnconfigure(0, weight=3)
        self.root.columnconfigure(1, weight=2)
        self.root.rowconfigure(0, weight=1)
        self.visual_panel = tk.Frame(self.root, bg="#071014")
        self.visual_panel.grid(row=0, column=0, sticky="nsew", padx=(18, 9), pady=18)
        self.visual_panel.rowconfigure(1, weight=1)
        self.visual_panel.columnconfigure(0, weight=1)
        tk.Label(self.visual_panel, text="Professor", bg="#071014", fg="#d8fff1", font=("Segoe UI", 34, "bold")).grid(row=0, column=0, sticky="w")
        tk.Label(self.visual_panel, text="Local biotech real-time worker", bg="#071014", fg="#7ad7c4", font=("Segoe UI", 13)).grid(row=0, column=0, sticky="w", pady=(48, 0))
        self.canvas = tk.Canvas(self.visual_panel, bg="#071014", highlightthickness=0)
        self.canvas.grid(row=1, column=0, sticky="nsew", pady=(18, 0))
        self.side = tk.Frame(self.root, bg="#0d1b22")
        self.side.grid(row=0, column=1, sticky="nsew", padx=(9, 18), pady=18)
        self.side.columnconfigure(0, weight=1)
        self.side.rowconfigure(5, weight=1)
        tk.Label(self.side, text="Local Control", bg="#0d1b22", fg="#f4fbf8", font=("Segoe UI", 19, "bold")).grid(row=0, column=0, sticky="w", padx=18, pady=(18, 4))
        self.status = tk.Label(self.side, text="Working locally. Cloud AI is off unless allowed.", bg="#0d1b22", fg="#9bb8b0", wraplength=380, justify="left", font=("Segoe UI", 10))
        self.status.grid(row=1, column=0, sticky="w", padx=18, pady=(0, 14))
        self.command = tk.Entry(self.side, bg="#13252d", fg="#ffffff", insertbackground="#ffffff", relief="flat", font=("Segoe UI", 12))
        self.command.grid(row=2, column=0, sticky="ew", padx=18, ipady=12)
        self.command.insert(0, "professor gc content of ATGCGCGTTA")
        self.command.bind("<Return>", lambda _event: self.run_text_command())
        self.command.bind("<Key>", lambda _event: self._touch())
        self.button_row = tk.Frame(self.side, bg="#0d1b22")
        self.button_row.grid(row=3, column=0, sticky="ew", padx=18, pady=12)
        for column in range(3):
            self.button_row.columnconfigure(column, weight=1)
        self._button("Run", self.run_text_command, "#34d399", "#062016", 0)
        self._button("Listen", self.start_voice, "#38bdf8", "#061722", 1)
        self._button("Shrink", self.shrink, "#f0abfc", "#1e1026", 2)
        self.worker_label = tk.Label(self.side, text="Worker: idle", bg="#10252d", fg="#a7f3d0", anchor="w", font=("Segoe UI", 10, "bold"), padx=12, pady=10)
        self.worker_label.grid(row=4, column=0, sticky="ew", padx=18, pady=(0, 12))
        self.log = scrolledtext.ScrolledText(self.side, bg="#071014", fg="#e5fff8", insertbackground="#ffffff", relief="flat", font=("Consolas", 10), wrap="word")
        self.log.grid(row=5, column=0, sticky="nsew", padx=18, pady=(0, 18))
        self._log("Professor is ready.")
        self._log("She will shrink after 90 seconds of no activity.")

    def _button(self, text: str, command, bg: str, fg: str, column: int) -> None:
        tk.Button(self.button_row, text=text, command=command, bg=bg, fg=fg, activebackground=bg, relief="flat", font=("Segoe UI", 11, "bold"), padx=12, pady=10).grid(row=0, column=column, sticky="ew", padx=4)

    def _touch(self) -> None:
        self.last_activity = time.time()

    def _log(self, text: str) -> None:
        self._touch()
        self.log.insert("end", text + "\n")
        self.log.see("end")

    def _clean_command(self, text: str) -> str:
        text = text.strip().lower()
        if text.startswith("professor"):
            return text.replace("professor", "", 1).strip(" ,")
        return text

    def run_text_command(self) -> None:
        self._touch()
        raw = self.command.get()
        response, _running = handle_command(self._clean_command(raw), self.permissions)
        self._log(f"You: {raw}")
        self._log(f"Professor: {response}")

    def start_voice(self) -> None:
        self._touch()
        if self.voice_running:
            self._log("Voice mode is already listening.")
            return
        self.voice_running = True
        self._log("Voice worker started. Say Professor, then your command.")
        threading.Thread(target=self._voice_loop, daemon=True).start()

    def _voice_loop(self) -> None:
        if self.speech is None:
            self.speech = Speech()
        self.speech.say("Professor voice worker is ready.")
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

    def shrink(self) -> None:
        self.compact = True
        self.root.geometry("360x150")
        self.root.attributes("-topmost", True)
        self.visual_panel.grid_remove()
        self.command.grid_remove()
        self.log.grid_remove()
        self.status.configure(text="Professor is working locally in compact mode.")
        self.root.title("Professor - working")
        for child in self.button_row.winfo_children():
            child.destroy()
        self.button_row.columnconfigure(0, weight=1)
        self.button_row.columnconfigure(1, weight=1)
        self._button("Expand", self.expand, "#34d399", "#062016", 0)
        self._button("Listen", self.start_voice, "#38bdf8", "#061722", 1)

    def expand(self) -> None:
        self.compact = False
        self.root.attributes("-topmost", False)
        self.root.geometry("1100x720")
        self._build_layout()
        self.root.title("Professor Voice Assistant")

    def _worker_tick(self) -> None:
        elapsed = int(time.time() - self.last_activity)
        mode = "listening" if self.voice_running else "idle"
        if hasattr(self, "worker_label"):
            self.worker_label.configure(text=f"Worker: {mode} | local | {elapsed}s since activity")
        if not self.compact and elapsed > 90:
            self.shrink()
        self.root.after(1000, self._worker_tick)

    def _animate(self) -> None:
        if hasattr(self, "canvas") and self.canvas.winfo_ismapped():
            self.canvas.delete("all")
            width = max(self.canvas.winfo_width(), 640)
            height = max(self.canvas.winfo_height(), 420)
            cx = width / 2
            cy = height / 2
            scale = min(width, height) / 5
            self.canvas.create_oval(cx - scale * 2, cy - scale * 1.45, cx + scale * 2, cy + scale * 1.45, outline="#16343b", width=2)
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
                for x1, y1, x2, _y2 in points:
                    x = x1 if strand == 0 else x2
                    if previous:
                        self.canvas.create_line(previous[0], previous[1], x, y1, fill="#d8fff1", width=2)
                    previous = (x, y1)
            self.canvas.create_text(cx, height - 48, text="Animated local biotech core", fill="#87f7df", font=("Segoe UI", 14, "bold"))
            self.angle += 0.055
        self.root.after(33, self._animate)

    def run(self) -> None:
        self.root.mainloop()


def run_app() -> None:
    ProfessorApp().run()
