import os

IGNORE = {".git","node_modules","__pycache__",".venv"}

def scan_project(root="."):

    files = []

    for path, dirs, filenames in os.walk(root):

        dirs[:] = [d for d in dirs if d not in IGNORE]

        for f in filenames:

            if f.endswith((".py",".js",".ts",".json",".md",".html",".css")):
                files.append(os.path.join(path,f))

    return files