import sys
from ui.gui import launch_gui
from core.repl import start_terminal
from ui.banner import show_banner


def main():
    """
    Entry point for ShellMind.

    --cli flag launches terminal mode.
    Default launches GUI.
    """

    args = [arg.lower() for arg in sys.argv]

    if "--cli" in args:
        show_banner()
        start_terminal()
    else:
        launch_gui()


if __name__ == "__main__":
    main()