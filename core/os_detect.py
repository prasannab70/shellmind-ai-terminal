import platform

def get_os():
    """
    Detect the operating system.
    Returns the OS name.
    """
    return platform.system()