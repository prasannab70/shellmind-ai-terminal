from ai.ai_engine import ask_ai

def analyze_error(error_log):

    prompt = f"""
You are a senior software engineer.

Fix this error:

{error_log}

Explain the cause and provide the fix.
"""

    return ask_ai(prompt)