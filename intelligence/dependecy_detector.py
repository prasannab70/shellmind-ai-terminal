import json

def detect_dependencies():

    deps = []

    try:
        with open("requirements.txt") as f:
            deps += f.read().splitlines()
    except:
        pass

    try:
        with open("package.json") as f:
            data = json.load(f)
            deps += list(data.get("dependencies",{}).keys())
    except:
        pass

    return deps