import os
from datetime import datetime


def analyze_folder(folder_path):

    if not os.path.exists(folder_path):
        return f"Folder '{folder_path}' does not exist."

    if not os.path.isdir(folder_path):
        return f"'{folder_path}' is not a folder."

    files = []
    total_size = 0

    for root, dirs, filenames in os.walk(folder_path):
        for f in filenames:

            full_path = os.path.join(root, f)

            try:
                size = os.path.getsize(full_path)
                total_size += size

                files.append((f, size))

            except:
                pass

    try:
        created = os.path.getctime(folder_path)
        created_time = datetime.fromtimestamp(created)
    except:
        created_time = "Unknown"

    size_kb = total_size / 1024

    output = []
    output.append("📁 Folder Analysis")
    output.append("")
    output.append(f"Folder  : {folder_path}")
    output.append(f"Created : {created_time}")
    output.append(f"Files   : {len(files)}")
    output.append(f"Size    : {size_kb:.2f} KB")
    output.append("")
    output.append("Files inside:")

    if not files:
        output.append("  (empty)")
    else:
        for name, size in files:
            kb = size / 1024
            output.append(f"  {name} ({kb:.2f} KB)")

    return "\n".join(output)