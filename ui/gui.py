import tkinter as tk
from tkinter import ttk, scrolledtext
import threading
import itertools
import time
import subprocess
from datetime import datetime

from core.command_handler import handle_command
from core.executor import send_input, current_process


COMMAND_ICONS = {
    "git": "🔧",
    "pip": "📦",
    "python": "🐍",
    "npm": "📦",
    "docker": "🐳",
    "ls": "📁"
}

STATUS_ICONS = {
    "success": "✅",
    "error": "❌",
    "running": "⏳"
}

SUGGESTIONS = [
    "ai:help",
    "ai:scan project",
    "ai:create folder test",
    "ai:create python file app",
    "ai:install numpy",
    "ai:install requirements",
    "ai:create git repo",
    "ai:git status",
    "ai:docker build"
]


def get_icon(cmd):
    for k in COMMAND_ICONS:
        if cmd.startswith(k):
            return COMMAND_ICONS[k]
    return "⚡"


class GradientFrame(tk.Canvas):

    def __init__(self, parent, c1, c2):
        super().__init__(parent, highlightthickness=0)
        self.c1 = c1
        self.c2 = c2
        self.bind("<Configure>", self.draw)

    def draw(self, event=None):

        self.delete("all")

        w = self.winfo_width()
        h = self.winfo_height()

        r1, g1, b1 = self.winfo_rgb(self.c1)
        r2, g2, b2 = self.winfo_rgb(self.c2)

        r_ratio = (r2 - r1) / h
        g_ratio = (g2 - g1) / h
        b_ratio = (b2 - b1) / h

        for i in range(h):

            nr = int(r1 + r_ratio * i)
            ng = int(g1 + g_ratio * i)
            nb = int(b1 + b_ratio * i)

            color = "#%4.4x%4.4x%4.4x" % (nr, ng, nb)

            self.create_line(0, i, w, i, fill=color)


def fade_in(widget):

    widget.update()

    for _ in range(6):
        widget.update()
        time.sleep(0.02)


class CommandBlock:

    def __init__(self, parent, command, logs):

        self.logs = logs
        self.start = time.time()

        icon = get_icon(command)

        self.frame = tk.Frame(parent, bg="#1a1a1a", bd=1, relief="solid")

        header = tk.Frame(self.frame, bg="#222")
        header.pack(fill="x")

        self.status = tk.Label(
            header,
            text=STATUS_ICONS["running"],
            bg="#222",
            fg="#00ff9c",
            font=("Consolas", 10, "bold")
        )
        self.status.pack(side="left", padx=6)

        tk.Label(
            header,
            text=f"{icon} {command}",
            bg="#222",
            fg="#4cc9f0",
            font=("Consolas", 11, "bold")
        ).pack(side="left", padx=4)

        self.time = tk.Label(
            header,
            text="0s",
            bg="#222",
            fg="#aaa",
            font=("Consolas", 10)
        )
        self.time.pack(side="right", padx=6)

        self.toggle = tk.Button(
            header,
            text="▼",
            bg="#222",
            fg="white",
            relief="flat",
            command=self.toggle_view
        )
        self.toggle.pack(side="right")

        self.progress = ttk.Progressbar(self.frame, mode="indeterminate")
        self.progress.pack(fill="x", padx=5)

        self.output = tk.Text(
            self.frame,
            height=6,
            bg="#0c0c0c",
            fg="white",
            font=("Consolas", 11),
            wrap="word"
        )

        self.output.tag_config("success", foreground="#50fa7b")
        self.output.tag_config("error", foreground="#ff5555")

        self.output.pack(fill="x", padx=5, pady=5)

        self.collapsed = False

    def start_progress(self):
        self.progress.start(10)

    def stop_progress(self):
        self.progress.stop()
        self.progress.pack_forget()

    def write_line(self, text):

        tag = None

        if "error" in text.lower():
            tag = "error"
        elif "success" in text.lower():
            tag = "success"

        self.output.insert("end", text + "\n", tag)
        self.output.see("end")

        self.logs.insert("end", text + "\n")
        self.logs.see("end")

    def finish(self, success=True):

        self.stop_progress()

        duration = round(time.time() - self.start, 2)
        self.time.config(text=f"{duration}s")

        if success:
            self.status.config(text=STATUS_ICONS["success"], fg="#50fa7b")
        else:
            self.status.config(text=STATUS_ICONS["error"], fg="#ff5555")

    def toggle_view(self):

        if self.collapsed:
            self.output.pack(fill="x", padx=5, pady=5)
            self.toggle.config(text="▼")
        else:
            self.output.pack_forget()
            self.toggle.config(text="▶")

        self.collapsed = not self.collapsed


def launch_gui():

    root = tk.Tk()
    root.title("ShellMind AI Terminal")
    root.geometry("1300x750")

    gradient = GradientFrame(root, "#121212", "#1e1e1e")
    gradient.pack(fill="both", expand=True)

    history = []

    header = tk.Frame(gradient, bg="#1f1f1f")
    header.pack(fill="x")

    tk.Label(
        header,
        text="ShellMind AI Terminal",
        fg="#00ff9c",
        bg="#1f1f1f",
        font=("Consolas", 14, "bold")
    ).pack(side="left", padx=10)

    status = tk.Label(header, text="READY", bg="#1f1f1f", fg="#aaa")
    status.pack(side="right", padx=10)

    notebook = ttk.Notebook(gradient)
    notebook.pack(fill="both", expand=True)

    tab = tk.Frame(notebook, bg="#121212")
    notebook.add(tab, text="Terminal 1")

    main = tk.Frame(tab, bg="#121212")
    main.pack(fill="both", expand=True)

    canvas = tk.Canvas(main, bg="#121212", highlightthickness=0)
    canvas.pack(side="left", fill="both", expand=True)

    scroll = tk.Scrollbar(main, command=canvas.yview)
    scroll.pack(side="right", fill="y")

    canvas.configure(yscrollcommand=scroll.set)

    inner = tk.Frame(canvas, bg="#121212")
    canvas.create_window((0, 0), window=inner, anchor="nw")

    inner.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    sidebar = tk.Frame(main, width=320, bg="#1e1e1e")
    sidebar.pack(side="right", fill="y")

    tk.Label(sidebar, text="AI Assistant",
             fg="#00ff9c", bg="#1e1e1e",
             font=("Consolas", 12, "bold")).pack(pady=6)

    chat = scrolledtext.ScrolledText(sidebar, bg="#121212", fg="white", height=15)
    chat.pack(fill="x", padx=8)

    tk.Label(sidebar, text="Logs Viewer",
             fg="#ffaa00", bg="#1e1e1e",
             font=("Consolas", 11, "bold")).pack(pady=6)

    logs = scrolledtext.ScrolledText(sidebar, bg="#0c0c0c", fg="#aaa", height=15)
    logs.pack(fill="both", expand=True, padx=8)

    input_frame = tk.Frame(root, bg="#121212")
    input_frame.pack(fill="x")

    tk.Label(input_frame, text="shellmind >", fg="#00ff9c", bg="#121212",
             font=("Consolas", 12)).pack(side="left", padx=5)

    entry = tk.Entry(input_frame, bg="#1e1e1e", fg="white",
                     insertbackground="white",
                     font=("Consolas", 12))
    entry.pack(side="left", fill="x", expand=True, padx=5)

    suggestion_box = tk.Listbox(root, bg="#1e1e1e", fg="white")

    def show_suggestions(event):

        text = entry.get()

        suggestion_box.delete(0, "end")

        for cmd in SUGGESTIONS:
            if cmd.startswith(text):
                suggestion_box.insert("end", cmd)

        if suggestion_box.size() > 0:
            suggestion_box.place(x=10, y=root.winfo_height() - 120, width=400)
        else:
            suggestion_box.place_forget()

    entry.bind("<KeyRelease>", show_suggestions)

    def use_suggestion(event):

        selection = suggestion_box.get("active")
        entry.delete(0, "end")
        entry.insert(0, selection)
        suggestion_box.place_forget()

    suggestion_box.bind("<Double-Button-1>", use_suggestion)

    date_label = tk.Label(inner, text=datetime.now().strftime("%Y-%m-%d"),
                          fg="#777", bg="#121212", font=("Consolas", 9))
    date_label.pack(anchor="w", padx=6)

    def run(e):

        user = entry.get()
        if not user:
            return

        entry.delete(0, "end")
        history.append(user)

        chat.insert("end", f"User: {user}\n")
        chat.see("end")

        block = CommandBlock(inner, user, logs)
        block.frame.pack(fill="x", padx=6, pady=6)

        block.start_progress()

        fade_in(block.frame)

        threading.Thread(
            target=execute_cli,
            args=(block, user),
            daemon=True
        ).start()

    def execute_cli(block, user):

        spinner_cycle = itertools.cycle(["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"])

        running = True

        start_time = time.time()

        def spinner():

            if running:
                icon = next(spinner_cycle)
                root.after(0, lambda: block.status.config(text=f"{icon}"))
                root.after(120, spinner)

        spinner()

        def stream(line):
            root.after(0, lambda: block.write_line(line))

        out = handle_command(user, stream_callback=stream)

        running = False

        duration = round(time.time() - start_time, 2)

        if out:
            root.after(0, lambda: block.write_line(str(out)))

        success = not ("error" in str(out).lower() or "failed" in str(out).lower())

        root.after(0, lambda: block.finish(success))

        root.after(0, lambda: chat.insert("end", f"AI: {str(out)[:120]}\n\n"))

    entry.bind("<Return>", run)

    root.mainloop()