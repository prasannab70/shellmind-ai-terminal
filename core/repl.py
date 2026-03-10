from prompt_toolkit import prompt
import os

from core.executor import run_command
from ai.ai_engine import ask_ai
from context.detector import detect_context
from core.os_detect import get_os
from safety.guard import check_risk
from healing.error_agent import error_agent


def start_terminal():

    while True:

        try:
            user_input = prompt(f"{os.getcwd()} > ").strip()

            if not user_input:
                continue

            # Exit command
            if user_input.lower() == "exit":
                print("Exiting ShellMind...")
                break


            # =========================================================
            # AI MODE
            # =========================================================

            if user_input.lower().startswith("ai:"):

                query = user_input[3:].strip().lower()


                if query == "help":

                    print("""
ShellMind AI Commands

Error Agent:
ai: scan project
ai: show errors
ai: explain errors
ai: fix errors
ai: fix file <path>
ai: clear errors
""")

                    continue


                # -----------------------------------------------------
                # ERROR AGENT COMMANDS
                # -----------------------------------------------------

                if query == "scan project":

                    result = error_agent.cmd_scan(os.getcwd())
                    print(result)
                    continue


                if query == "show errors":

                    result = error_agent.cmd_show_errors(os.getcwd())
                    print(result)
                    continue


                if query == "explain errors":

                    result = error_agent.cmd_explain_errors()
                    print(result)
                    continue


                if query == "fix errors":

                    result = error_agent.cmd_fix_all(os.getcwd())
                    print(result)
                    continue


                if query.startswith("fix file"):

                    parts = query.split(" ", 2)

                    if len(parts) < 3:
                        print("Usage: ai: fix file <path>")
                        continue

                    filepath = parts[2]

                    result = error_agent.cmd_fix_file(filepath, os.getcwd())
                    print(result)
                    continue


                if query == "clear errors":

                    result = error_agent.cmd_clear_errors(os.getcwd())
                    print(result)
                    continue


                # -----------------------------------------------------
                # NORMAL AI COMMAND GENERATION
                # -----------------------------------------------------

                context = detect_context()
                os_type = get_os()

                command = ask_ai(query, context, os_type)

                if not command:
                    print("AI could not generate a command.")
                    continue

                print("\nAI Suggested Command:")
                print(f"  {command}")
                print("──────────────────────────────")

                # Check risk
                risk = check_risk(command)

                if risk == "HIGH":
                    print("⚠ Warning: This command may be dangerous.")

                # Only suggest command, do not execute
                continue


            # =========================================================
            # NORMAL TERMINAL COMMANDS
            # =========================================================

            run_command(user_input)


        except KeyboardInterrupt:
            print("\nUse 'exit' to quit ShellMind.")