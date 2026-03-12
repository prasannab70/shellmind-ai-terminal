import os
import shutil

history_stack = []


def record(command, undo_command=None, backup=None):
    history_stack.append({
        "command": command,
        "undo": undo_command,
        "backup": backup
    })


def undo_last(stream_callback=None):

    if not history_stack:
        return "Nothing to undo."

    last = history_stack.pop()

    undo_cmd = last.get("undo")
    backup = last.get("backup")

    # restore backup file if exists
    if backup and os.path.exists(backup["backup_path"]):
        shutil.copy2(backup["backup_path"], backup["original_path"])
        os.remove(backup["backup_path"])
        return f"Undo successful. Restored {backup['original_path']}"

    if undo_cmd:
        import subprocess

        process = subprocess.Popen(
            undo_cmd,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True
        )

        out = process.communicate()[0]

        if stream_callback:
            stream_callback(out)

        return f"Undo executed:\n{undo_cmd}"

    return "Undo not supported for last command."
def generate_undo(command):

    cmd = command.strip()

    # mkdir
    if cmd.startswith("mkdir "):
        name = cmd.split(" ",1)[1]
        return f"rmdir {name}"

    # pip install
    if cmd.startswith("pip install "):
        pkg = cmd.split(" ",2)[2]
        return f"pip uninstall -y {pkg}"

    # move
    if cmd.startswith("move ") or cmd.startswith("mv "):
        parts = cmd.split()
        if len(parts) >= 3:
            return f"mv {parts[2]} {parts[1]}"

    # rename
    if cmd.startswith("rename "):
        parts = cmd.split()
        if len(parts) >= 3:
            return f"rename {parts[2]} {parts[1]}"

    return None  