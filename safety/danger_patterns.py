# safety/danger_patterns.py

DANGER_PATTERNS = {

    "rm -rf": "Deletes files or folders recursively and forcefully.",
    "rm -r": "Deletes directories recursively.",
    "rmdir": "Removes a directory.",
    "del ": "Deletes files in Windows.",
    "erase ": "Deletes files in Windows.",
    "rd /s": "Removes directory and all contents.",

    "shutdown": "Shuts down the system.",
    "reboot": "Restarts the system.",
    "format": "Formats a disk or drive.",
    "mkfs": "Creates a filesystem on a device.",
    "diskpart": "Disk partitioning tool that can erase disks.",
    "fdisk": "Disk partition tool which can modify disks.",

    "delete_folder:": "Deletes a folder using internal AI command.",
    "delete_file:": "Deletes a file using internal AI command."
}