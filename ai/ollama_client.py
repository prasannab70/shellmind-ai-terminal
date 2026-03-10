import requests
import re

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "tinyllama"


def ask_ollama(prompt):

    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL,
                "prompt": prompt,
                "stream": False
            }
        )

        data = response.json()
        text = data.get("response", "").strip()

        # extract command inside backticks
        match = re.search(r"`([^`]+)`", text)

        if match:
            command = match.group(1)
        else:
            command = text.split("\n")[0]

        return command.strip()

    except Exception as e:
        print("AI Error:", e)
        return ""