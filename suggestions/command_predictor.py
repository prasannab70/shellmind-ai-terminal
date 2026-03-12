RULES = {
    "git init": "git add .",
    "git add .": "git commit -m 'initial commit'",
    "git commit": "git push origin main",
    "pip install": "python main.py",
    "npm install": "npm start"
}

def suggest_next(cmd):

    for k in RULES:

        if cmd.startswith(k):
            return RULES[k]

    return None