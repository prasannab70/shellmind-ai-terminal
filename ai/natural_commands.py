from core.executor import run_command
import re
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

# ---------------------------------------------------------
# WORD VARIATIONS
# ---------------------------------------------------------

CREATE_WORDS = ["create", "make", "generate", "build", "add"]

DELETE_WORDS = ["delete", "remove", "destroy", "erase"]

FOLDER_WORDS = ["folder", "directory", "dir"]

FILE_WORDS = ["file", "document"]

def detect_create_file_in_folder(query):

    pattern = r"create .*file (.+?) (?:in|inside) (?:folder )?(.+)"
    m = re.search(pattern, query)

    if not m:
        return None

    filename = m.group(1).strip()
    folder = m.group(2).strip()

    return f"create_file:{folder}/{filename}"
# ---------------------------------------------------------
# CLEAN INPUT
# ---------------------------------------------------------

def normalize_query(query):

    q = query.lower()

    replacements = {
        "initialize": "init",
        "initialise": "init",
        "repository": "repo",
        "directory": "folder",
        "start": "run",
        "execute": "run",
        "launch": "run",
        "container": "docker container"
    }

    for k, v in replacements.items():
        q = q.replace(k, v)

    fillers = ["a", "new", "called", "named", "the"]

    for f in fillers:
        q = q.replace(f" {f} ", " ")

    return q.strip()


# ---------------------------------------------------------
# CREATE FOLDER
# ---------------------------------------------------------

def try_create_folder(q):

    for action in CREATE_WORDS:
        for target in FOLDER_WORDS:

            pattern = rf"{action} .*{target} (.+)"
            m = re.search(pattern, q)

            if m:
                name = m.group(1).strip()
                return f"create_folder:{name}"

    return None


# ---------------------------------------------------------
# CREATE FILE
# ---------------------------------------------------------

def try_create_file(q):

    for action in CREATE_WORDS:
        for target in FILE_WORDS:

            pattern = rf"{action} .*{target} (.+)"
            m = re.search(pattern, q)

            if m:

                name = m.group(1).strip()

                if "python file" in q and not name.endswith(".py"):
                    name += ".py"

                return f"create_file:{name}"

    return None


# ---------------------------------------------------------
# DELETE FILE
# ---------------------------------------------------------

def try_delete_file(q):

    for action in DELETE_WORDS:
        for target in FILE_WORDS:

            pattern = rf"{action} .*{target} (.+)"
            m = re.search(pattern, q)

            if m:
                name = m.group(1).strip()
                return f"delete_file:{name}"

    return None


# ---------------------------------------------------------
# DELETE FOLDER
# ---------------------------------------------------------

def try_delete_folder(q):

    for action in DELETE_WORDS:
        for target in FOLDER_WORDS:

            pattern = rf"{action} .*{target} (.+)"
            m = re.search(pattern, q)

            if m:
                name = m.group(1).strip()
                return f"delete_folder:{name}"

    return None


# ---------------------------------------------------------
# COPY FILE
# ---------------------------------------------------------

def try_copy_file(q):

    m = re.search(r"copy .*file (.+) to (.+)", q)

    if m:
        src = m.group(1).strip()
        dst = m.group(2).strip()
        return f"copy_file:{src}:{dst}"

    return None


# ---------------------------------------------------------
# MOVE FILE
# ---------------------------------------------------------

def try_move_file(q):

    m = re.search(r"move .*file (.+) to (.+)", q)

    if m:
        src = m.group(1).strip()
        dst = m.group(2).strip()
        return f"move_file:{src}:{dst}"

    return None


# ---------------------------------------------------------
# RENAME FILE
# ---------------------------------------------------------

def try_rename_file(q):

    m = re.search(r"rename .*file (.+) to (.+)", q)

    if m:
        src = m.group(1).strip()
        dst = m.group(2).strip()
        return f"rename_file:{src}:{dst}"

    return None


# ---------------------------------------------------------
# OPEN FOLDER
# ---------------------------------------------------------

def try_open_folder(q):

    m = re.search(r"open .*folder (.+)", q)

    if m:
        name = m.group(1).strip()
        return f"open_folder:{name}"

    return None


# ---------------------------------------------------------
# PYTHON COMMANDS
# ---------------------------------------------------------

def try_python_commands(q, stream_callback=None):

    m = re.search(r"run python file (.+)", q)
    if m:
        name = m.group(1).strip()
        if not name.endswith(".py"):
            name += ".py"
        return f"python {name}"

    m = re.search(r"create python file (.+)", q)
    if m:
        name = m.group(1).strip()
        if not name.endswith(".py"):
            name += ".py"
        return f"type nul > {name}"

    m = re.search(r"install python package (.+)", q)
    if m:
        pkg = m.group(1).strip()
        return f"pip install {pkg}"

    return None


# ---------------------------------------------------------
# DOCKER COMMANDS
# ---------------------------------------------------------

def try_docker_commands(q, stream_callback=None):

    if "docker build" in q or "build docker image" in q:
        return "docker build ."

    if "run docker container" in q or "docker run" in q:
        return "docker run"

    if "docker images" in q or "show docker images" in q:
        return "docker images"

    if "docker ps" in q or "list docker containers" in q:
        return "docker ps"

    return None


# ---------------------------------------------------------
# GIT COMMANDS
# ---------------------------------------------------------

def try_git_commands(q, stream_callback=None):

    if "init git" in q or "create git repo" in q or "make git repo" in q:
        return "git init"

    if "git status" in q or "show git status" in q:
        return "git status"

    if "commit changes" in q:
        return 'git commit -m "update"'

    if "push changes" in q:
        return "git push"

    if "pull changes" in q:
        return "git pull"

    return None


# ---------------------------------------------------------
# DEPENDENCY COMMANDS
# ---------------------------------------------------------

def try_dependency_commands(q, stream_callback=None):

    if "install requirements" in q or "install python dependencies" in q:
        return "pip install -r requirements.txt"

    if "install node dependencies" in q or "install npm dependencies" in q:
        return "npm install"

    m = re.search(r"install npm package (.+)", q)
    if m:
        pkg = m.group(1).strip()
        return f"npm install {pkg}"

    m = re.search(r"(install|add) dependency (.+)", q)
    if m:
        pkg = m.group(2).strip()
        return f"pip install {pkg}"

    m = re.search(r"install (.+)", q)
    if m:
        pkg = m.group(1).strip()
        return f"pip install {pkg}"

    return None


# ---------------------------------------------------------
# MAIN PARSER
# ---------------------------------------------------------

def parse_natural_command(query, stream_callback=None):

    q = normalize_query(query)

    checks = [
        try_create_folder,
        try_create_file,
        try_delete_file,
        try_delete_folder,
        try_copy_file,
        try_move_file,
        try_rename_file,
        try_open_folder
    ]

    for func in checks:
        result = func(q)
        if result:

            # execute file operations if sudo mode
            if stream_callback and ":" in result:

                parts = result.split(":")
                action = parts[0]

                if action == "create_folder":
                    return create_folder(parts[1])

                if action == "create_file":
                    return create_file(parts[1])

                if action == "delete_file":
                    return delete_file(parts[1])

                if action == "delete_folder":
                    return delete_folder(parts[1])

                if action == "copy_file":
                    return copy_file(parts[1], parts[2])

                if action == "move_file":
                    return move_file(parts[1], parts[2])

                if action == "rename_file":
                    return rename_file(parts[1], parts[2])

                if action == "open_folder":
                    return open_folder(parts[1])

            return result

    result = try_python_commands(q, stream_callback)
    if result:
        return run_command(result, stream_callback)

    result = try_git_commands(q, stream_callback)
    if result:
        return run_command(result, stream_callback)

    result = try_dependency_commands(q, stream_callback)
    if result:
        return run_command(result, stream_callback)

    result = try_docker_commands(q, stream_callback)
    if result:
        return run_command(result, stream_callback)
    
    result = detect_create_file_in_folder(q)
    if result:
        return result

    return None