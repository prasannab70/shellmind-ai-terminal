import tkinter as tk
from services.command_service import process_user_input


def launch_gui():

    root = tk.Tk()
    root.title("ShellMind AI Terminal")
    root.geometry("800x500")

    output_box = tk.Text(root, height=25, width=100)
    output_box.pack()

    input_box = tk.Entry(root, width=100)
    input_box.pack()

    def handle_command(event=None):

        user_input = input_box.get()

        result = process_user_input(user_input)

        output_box.insert(tk.END, f"\n> {result['command']}\n")
        output_box.insert(tk.END, result["output"] + "\n")

        input_box.delete(0, tk.END)

    input_box.bind("<Return>", handle_command)

    root.mainloop()