history_stack = []


def record_action(action):
    history_stack.append(action)


def undo_last():

    if not history_stack:
        return "Nothing to undo."

    action = history_stack.pop()

    if action["type"] == "create_file":
        import os
        os.remove(action["path"])
        return f"Undo successful. Deleted {action['path']}"

    if action["type"] == "create_folder":
        import os
        os.rmdir(action["path"])
        return f"Undo successful. Removed folder {action['path']}"

    return "Undo not supported for that command."