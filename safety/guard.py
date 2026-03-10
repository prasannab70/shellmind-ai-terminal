DANGEROUS_PATTERNS = [
    "rm -rf",
    "del /f",
    "format",
    "shutdown",
]


def check_risk(command):

    cmd = command.lower()

    for pattern in DANGEROUS_PATTERNS:
        if pattern in cmd:
            return "HIGH"

    return "LOW"