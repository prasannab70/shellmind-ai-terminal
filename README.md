# ShellMind — AI-Powered Smart Terminal

An AI-augmented terminal that layers context-aware command suggestions, autonomous execution, and self-healing on top of a normal shell — usable either as a GUI app or a CLI/REPL.

## Features

- **Dual entry points** — launches a GUI by default, or drop into terminal/REPL mode with `--cli`.
- **AI intelligence layer** — context-aware command suggestions based on what you're doing in the shell.
- **Autonomous execution** — can act on suggestions itself rather than only proposing them.
- **Self-healing** — detects failed commands or broken states and attempts to recover.
- **Safety-check layer** — a dedicated module gates AI/autonomous actions before they touch the real system.
- **Cross-environment OS abstraction** — an `os_layer` module isolates platform-specific behavior so the core logic stays portable.

## Architecture

The codebase is split into clearly separated concerns, each in its own module:

```
.
├── main.py            # entry point — GUI by default, --cli for terminal mode
├── ui/                 # GUI + banner/terminal presentation (ui.gui, ui.banner)
├── core/               # core REPL loop (core.repl)
├── ai/                 # AI suggestion / reasoning logic
├── intelligence/       # context-aware command intelligence
├── autonomous/         # autonomous command execution
├── healing/            # self-healing / recovery logic
├── safety/             # safety checks gating autonomous actions
├── os_layer/           # cross-platform OS abstraction
├── suggestions/        # suggestion generation/ranking
├── context/            # session/context tracking
├── services/           # supporting services
├── config/             # configuration
├── utils/              # shared utilities
└── requirements.txt
```

This separation means the AI layer, the safety layer, and the execution layer are independent — the safety-check module can veto or gate anything the AI/autonomous layers propose before it reaches the real shell.

## Requirements

```
prompt_toolkit
requests
colorama
python-dotenv
```

## Setup & usage

```bash
pip install -r requirements.txt

# Create a .env file for any required API keys/config (see config/)

# Launch the GUI (default)
python main.py

# Or launch in terminal/REPL mode
python main.py --cli
```

## Notes

- This is an active/experimental project — the module boundaries (`ai`, `safety`, `healing`, `ui`) are designed to make it easy to swap out or harden individual pieces (e.g. tightening the safety layer) without touching the rest.
- Since `main.py` imports from `ui.gui`, `core.repl`, and `ui.banner`, make sure those packages' own dependencies (e.g. GUI toolkit requirements) are satisfied before launching in GUI mode.

## License

Add a license of your choice (MIT/Apache-2.0 are common for tools like this).
