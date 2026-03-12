# safety/danger_detector.py

from safety.danger_patterns import DANGER_PATTERNS


def check_dangerous_command(command: str):
    """
    Check if a command is dangerous and explain what it does.
    """

    if not command:
        return {
            "danger": False,
            "message": "Empty command."
        }

    command_lower = str(command).lower().strip()

    for pattern, explanation in DANGER_PATTERNS.items():
        if pattern in command_lower:
            return {
                "danger": True,
                "pattern": pattern,
                "message": (
                    f"\n⚠️ Dangerous Command Detected!\n"
                    f"Command: {command}\n"
                    f"Reason: {explanation}"
                )
            }

    return {
        "danger": False,
        "message": "Command appears safe."
    }