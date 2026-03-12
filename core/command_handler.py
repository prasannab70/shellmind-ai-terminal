import os
import re

from core.executor import run_command
from ai.ai_engine import ask_ai
from context.detector import detect_context
from core.os_detect import get_os
from ai.natural_commands import parse_natural_command
from utils.command_history import record_action, undo_last

from healing.file_ops import (
    create_folder,
    create_file,
    delete_folder,
    delete_file,
    copy_file,
    move_file,
    rename_file,
    open_folder
)

from safety.danger_detector import check_dangerous_command
from safety.folder_analyzer import analyze_folder


# ---------------------------------------------------------
# CONFIRMATION STATE (NEW)
# ---------------------------------------------------------

pending_confirm_command = None


# ---------------------------------------------------------
# SMART INTENT CLASSIFIER
# ---------------------------------------------------------

def classify_intent(query):

    question_words = [
        "what","why","how","when","where",
        "explain","tell","give","show"
    ]

    if any(query.startswith(q) for q in question_words):
        return "question"

    file_ops = [
        "create","make","generate","delete","remove","erase",
        "copy","move","rename","folder","file","directory"
    ]

    command_ops = [
        "install","run","start","build","deploy","setup",
        "docker","git","pip","npm","python","flask","fastapi"
    ]

    if any(w in query for w in file_ops):
        return "file"

    if any(w in query for w in command_ops):
        return "command"

    return "question"


# ---------------------------------------------------------
# NATURAL COMMAND EXPANSION
# ---------------------------------------------------------

def expand_natural_commands(query):

    rules = {

        "create flask api": "pip install flask && mkdir flask_api",
        "generate fastapi backend": "pip install fastapi uvicorn",
        "setup python project": "python -m venv venv",
        "setup python venv": "python -m venv venv",
        "install requirements": "pip install -r requirements.txt",
        "install dependencies": "pip install -r requirements.txt",
        "run flask app": "flask run",
        "run docker container": "docker run",
        "deploy docker container": "docker run",
        "build docker image": "docker build .",
        "start docker container": "docker run",
        "docker images": "docker images",
        "create git repo": "git init",
        "initialize git": "git init",
        "git status": "git status",
        "commit changes": 'git commit -m "update"',
        "commit and push git": 'git add . && git commit -m "update" && git push',

        "create git repo": "git init",
        "git init": "git init",
        "git status": "git status",
        "git add": "git add .",
        "git commit": 'git commit -m "update"',
        "git push": "git push",
        "git pull": "git pull",

        "docker build": "docker build .",
        "docker run": "docker run",
        "docker images": "docker images",
        "docker ps": "docker ps",

        "install numpy": "pip install numpy",
        "install pandas": "pip install pandas",
        "install requirements": "pip install -r requirements.txt",

        "install npm dependencies": "npm install",
    }

    for k,v in rules.items():
        if k in query:
            return v

    m = re.search(r"install (.+)", query)
    if m:
        pkg = m.group(1).strip()
        return f"pip install {pkg}"

    m = re.search(r"run python file (.+)", query)
    if m:
        name = m.group(1)

        if not name.endswith(".py"):
            name += ".py"

        return f"python {name}"

    return None


# ---------------------------------------------------------
# FILE OPERATION EXECUTOR
# ---------------------------------------------------------

def execute_file_operation(natural):

    if natural.startswith("create_folder:"):
        name = natural.split(":",1)[1]
        result = create_folder(name)
        record_action({"type": "create_folder","path": name})
        return result

    if natural.startswith("create_file:"):
        name = natural.split(":",1)[1]
        result = create_file(name)
        record_action({"type": "create_file","path": name})
        return result

    if natural.startswith("delete_folder:"):
        name = natural.split(":",1)[1]
        result = delete_folder(name)
        record_action({"type": "delete_folder","path": name})
        return result

    if natural.startswith("delete_file:"):
        name = natural.split(":",1)[1]
        result = delete_file(name)
        record_action({"type": "delete_file","path": name})
        return result

    if natural.startswith("copy_file:"):
        _,src,dst = natural.split(":")
        result = copy_file(src,dst)
        record_action({"type": "copy_file","src": src,"dst": dst})
        return result

    if natural.startswith("move_file:"):
        _,src,dst = natural.split(":")
        result = move_file(src,dst)
        record_action({"type": "move_file","src": src,"dst": dst})
        return result

    if natural.startswith("rename_file:"):
        _,src,dst = natural.split(":")
        result = rename_file(src,dst)
        record_action({"type": "rename_file","src": src,"dst": dst})
        return result

    if natural.startswith("open_folder:"):
        name = natural.split(":",1)[1]
        return open_folder(name)

    return None


# ---------------------------------------------------------
# MAIN COMMAND HANDLER
# ---------------------------------------------------------

def handle_command(user_input, stream_callback=None):

    global pending_confirm_command

    user_input = user_input.strip()

    # ---------------------------------------------
    # HANDLE YES / NO CONFIRMATION
    # ---------------------------------------------

    if pending_confirm_command:

        answer = user_input.lower()

        if answer in ["y","yes"]:
            cmd = pending_confirm_command
            pending_confirm_command = None

            if cmd.startswith("pip uninstall"):
                cmd = cmd + " -y"

            return run_command(cmd, stream_callback)

        elif answer in ["n","no"]:
            pending_confirm_command = None
            return "❌ Operation cancelled."

        else:
            return "Please type y or n."

    if not user_input.lower().startswith("ai:"):
        return run_command(user_input, stream_callback)

    query = user_input[3:].strip().lower()

    # -------------------------------------------------
    # DIRECT SHELL COMMAND
    # -------------------------------------------------

    direct_commands = (
        "pip ",
        "git ",
        "docker ",
        "npm ",
        "python ",
        "node "
    )

    if query.startswith(direct_commands):

        if query.startswith("pip uninstall"):
            pending_confirm_command = query
            return "⚠ This will uninstall a package. Continue? (y/n)"

        return run_command(query, stream_callback)

    # ---------------------------------------------
    # UNDO COMMAND
    # ---------------------------------------------

    if query == "undo":
        return undo_last()

    # ---------------------------------------------
    # ADMIN DELETE MODE
    # ---------------------------------------------

    if query.startswith("admin"):

        command = query.replace("admin","",1).strip()
        folder = command.split()[-1]

        analysis = analyze_folder(folder)

        output = "\n🔐 ADMIN DELETE MODE\n\n"
        output += "📁 Folder Analysis\n\n"
        output += analysis
        output += "\n\n🗑 Deleting folder...\n"

        delete_folder(folder)

        return output

    # ---------------------------------------------
    # QUESTION CHECK
    # ---------------------------------------------

    intent = classify_intent(query)

    if intent == "question":

        context = detect_context()
        os_type = get_os()

        return ask_ai(query, context, os_type)

    # ---------------------------------------------
    # NATURAL LANGUAGE PARSE
    # ---------------------------------------------

    natural = parse_natural_command(query)

    if natural:

        if natural.startswith("delete_folder:"):

            folder = natural.split(":")[1]
            analysis = analyze_folder(folder)

            pending_confirm_command = natural

            return f"""
⚠ Dangerous Command Detected!

Command: delete folder {folder}
Reason: You are deleting a directory.

📁 Folder Analysis

{analysis}

Do you want to continue? (yes/no):
"""

        file_result = execute_file_operation(natural)

        if file_result:
            return file_result

        command_to_run = natural

    else:

        expanded = expand_natural_commands(query)

        if expanded:
            command_to_run = expanded

        else:

            context = detect_context()
            os_type = get_os()

            ai_output = ask_ai(query, context, os_type)

            command_to_run = str(ai_output).strip()
            command_to_run = command_to_run.replace("```", "")

            lines = command_to_run.split("\n")

            for line in lines:

                line = line.strip()
                line = line.lstrip("$># ")

                if line.startswith(("pip", "git", "docker", "npm", "python")):
                    command_to_run = line
                    break
            else:
                command_to_run = lines[0].strip()

    # ---------------------------------------------
    # DANGEROUS COMMAND CHECK
    # ---------------------------------------------

    risk = check_dangerous_command(command_to_run)

    if risk == "HIGH":

        folder = command_to_run.split()[-1]
        analysis = analyze_folder(folder)

        pending_confirm_command = command_to_run

        return f"""
⚠ Dangerous Command Detected!

Command: {command_to_run}
Reason: You are deleting a directory.

📁 Folder Analysis

{analysis}

Do you want to continue? (yes/no):
"""

    return run_command(command_to_run, stream_callback)