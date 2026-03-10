import subprocess
import os
from safety.danger_detector import check_dangerous_command


def run_command(command):

    command = command.strip()

    if not command:
        return

    # ==============================
    # DANGER CHECK
    # ==============================

    result = check_dangerous_command(command)

    if result["danger"]:
        print(result["message"])

        confirm = input("\nDo you want to continue? (yes/no): ")

        if confirm.lower() != "yes":
            print("❌ Command cancelled.")
            return

    # ==============================
    # NORMAL COMMAND HANDLING
    # ==============================

    # Normalize Linux-style commands for Windows
    if command == "clear":
        command = "cls"

    if command == "ls":
        command = "dir"

    # Clear screen
    if command == "cls":
        os.system("cls")
        return

    # Handle cd manually
    if command.startswith("cd"):

        parts = command.split(maxsplit=1)

        if len(parts) == 1:
            print(os.getcwd())
            return

        path = parts[1]

        try:
            os.chdir(path)
        except Exception as e:
            print("Directory error:", e)

        return

    # Execute other commands
    try:

        result = subprocess.run(
            command,
            shell=True,
            text=True,
            capture_output=True
        )

        if result.stdout:
            print(result.stdout.strip())

        if result.stderr:
            print(result.stderr.strip())

    except Exception as e:
        print("Execution error:", e)