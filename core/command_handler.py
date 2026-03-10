import os

from core.executor import run_command
from ai.ai_engine import ask_ai
from context.detector import detect_context
from core.os_detect import get_os
from safety.danger_detector import check_dangerous_command
from healing.error_agent import error_agent
from ai.natural_commands import parse_natural_command


def handle_command(user_input, stream_callback=None):

    # ---------------------------------------------------------
    # NORMAL TERMINAL COMMAND
    # ---------------------------------------------------------

    if not user_input.lower().startswith("ai:"):
        return run_command(user_input, stream_callback)

    # ---------------------------------------------------------
    # AI MODE
    # ---------------------------------------------------------

    query = user_input[3:].strip().lower()

    # ---------------------------------------------------------
    # HELP
    # ---------------------------------------------------------

    if query == "help":

        return """
ShellMind AI Commands

Project Analysis
----------------
ai: scan project
ai: show errors
ai: explain errors
ai: fix errors
ai: fix file <path>
ai: clear errors

File Operations
---------------
ai:create folder test
ai:make a new folder called project
ai:create file test.txt
ai:create python file app
ai:remove file test.txt
ai:delete folder temp
"""

    # ---------------------------------------------------------
    # ERROR AGENT COMMANDS
    # ---------------------------------------------------------

    if query == "scan project":
        result = error_agent.cmd_scan(os.getcwd())
        if stream_callback:
            stream_callback(result + "\n")
        return result

    if query == "show errors":
        result = error_agent.cmd_show_errors(os.getcwd())
        if stream_callback:
            stream_callback(result + "\n")
        return result

    if query == "explain errors":
        result = error_agent.cmd_explain_errors()
        if stream_callback:
            stream_callback(result + "\n")
        return result

    if query == "fix errors":
        result = error_agent.cmd_fix_all(os.getcwd())
        if stream_callback:
            stream_callback(result + "\n")
        return result

    if query.startswith("fix file"):

        parts = query.split(" ", 2)

        if len(parts) < 3:
            return "Usage: ai: fix file <path>"

        filepath = parts[2]

        result = error_agent.cmd_fix_file(filepath, os.getcwd())

        if stream_callback:
            stream_callback(result + "\n")

        return result

    if query == "clear errors":
        result = error_agent.cmd_clear_errors(os.getcwd())

        if stream_callback:
            stream_callback(result + "\n")

        return result

    # ---------------------------------------------------------
    # NATURAL LANGUAGE COMMANDS
    # ---------------------------------------------------------

    natural_result = parse_natural_command(query, stream_callback)

    if natural_result:
        return natural_result

    # ---------------------------------------------------------
    # AI COMMAND GENERATION
    # ---------------------------------------------------------

    context = detect_context()
    os_type = get_os()

    command = ask_ai(query, context, os_type)

    if not command:
        return "AI could not generate a command."

    risk = check_dangerous_command(command)

    if stream_callback:
        stream_callback(f"\nAI Suggested Command:\n  {command}\n")

    if risk == "HIGH":
        warning = "⚠ Warning: This command may be dangerous.\n"
        if stream_callback:
            stream_callback(warning)
        return warning

    # Execute generated command so GUI shows output
    return run_command(command, stream_callback)