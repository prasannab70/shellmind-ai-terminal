import subprocess
import os


def run_command(command):

    command = command.strip()

    # Handle clear screen
    if command in ["cls", "clear"]:
        os.system("cls")  # Windows clear
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

    # Execute normal shell commands
    try:
        result = subprocess.run(
            command,
            shell=True,
            text=True,
            capture_output=True
        )

        if result.stdout:
            print(result.stdout)

        if result.stderr:
            print(result.stderr)

    except Exception as e:
        print("Execution error:", e)