import subprocess
import os
from utils.undo_manager import record, generate_undo


# store currently running process
current_process = None


def run_command(command, stream_callback=None):

    global current_process

    command = command.replace("\n", " ").strip()

    if not command:
        return ""

    # ------------------------------------------------
    # Windows aliases
    # ------------------------------------------------

    if command == "clear":
        command = "cls"

    if command == "ls":
        command = "dir"

    # ------------------------------------------------
    # Handle cd command
    # ------------------------------------------------

    if command.startswith("cd"):

        parts = command.split(maxsplit=1)

        if len(parts) == 1:
            out = os.getcwd()

            if stream_callback:
                stream_callback(out + "\n")

            return out

        try:
            os.chdir(parts[1])
            out = f"Changed directory to {os.getcwd()}"

        except Exception as e:
            out = str(e)

        if stream_callback:
            stream_callback(out + "\n")

        return out

    # ------------------------------------------------
    # Execute command
    # ------------------------------------------------

    try:

        current_process = subprocess.Popen(
            command,
            shell=True,
            stdin=subprocess.PIPE,   # allow interactive input
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
            universal_newlines=True
        )

        output = []

        if current_process.stdout is not None:

            for line in iter(current_process.stdout.readline, ''):

                if not line:
                    break

                output.append(line)

                if stream_callback:
                    stream_callback(line)

            current_process.stdout.close()

        current_process.wait()

        # ------------------------------------------------
        # Record undo only if command succeeded
        # ------------------------------------------------

        if current_process.returncode == 0:
            undo_cmd = generate_undo(command)
            record(command, undo_cmd)

        current_process = None

        return "".join(output)

    except Exception as e:

        error = str(e)

        if stream_callback:
            stream_callback(error + "\n")

        current_process = None

        return error


# ------------------------------------------------
# Send input to running interactive process
# ------------------------------------------------

def send_input(user_input):

    global current_process

    if current_process and current_process.stdin:
        try:
            current_process.stdin.write(user_input + "\n")
            current_process.stdin.flush()
        except Exception:
            pass