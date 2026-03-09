from prompt_toolkit import prompt
import os

from core.executor import run_command
from ai.ai_engine import ask_ai
from context.detector import detect_context
from core.os_detect import get_os


def start_terminal():

    while True:

        user_input = prompt(f"{os.getcwd()} > ").strip()

        if not user_input:
            continue

        if user_input.lower() == "exit":
            print("Exiting ShellMind...")
            break

        # AI Mode
        if user_input.lower().startswith("ai:"):

            query = user_input[3:].strip()

            context = detect_context()
            os_type = get_os()

            command = ask_ai(query, context, os_type)

            print("\nAI Suggested Command:")
            print(command)
            print("─" * 30)

            continue

        # Normal command execution
        run_command(user_input)