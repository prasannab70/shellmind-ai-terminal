import subprocess
import os


def run_command(command, stream_callback=None):

    command = command.strip()

    if not command:
        return ""

    if command == "clear":
        command = "cls"

    if command == "ls":
        command = "dir"

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

    process = subprocess.Popen(
        command,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1
    )

    output = ""

    for line in iter(process.stdout.readline, ""):

        output += line

        if stream_callback:
            stream_callback(line)

    process.stdout.close()
    process.wait()

    return output