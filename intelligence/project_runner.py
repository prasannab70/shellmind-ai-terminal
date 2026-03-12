import os
import subprocess

def detect_project():

    if os.path.exists("package.json"):
        return "node"

    if os.path.exists("requirements.txt"):
        return "python"

    if os.path.exists("docker-compose.yml"):
        return "docker"

    return None


def run_project():

    t = detect_project()

    if t == "node":
        return subprocess.run("npm start", shell=True)

    if t == "python":
        return subprocess.run("python main.py", shell=True)

    if t == "docker":
        return subprocess.run("docker-compose up", shell=True)

    return "Unknown project"