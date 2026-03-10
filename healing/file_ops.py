import os

def create_folder():
    folder_name = input("Enter folder name: ")

    if not folder_name:
        print("Folder name cannot be empty")
        return

    os.makedirs(folder_name, exist_ok=True)
    print(f"Folder '{folder_name}' created successfully")


def create_file():
    file_name = input("Enter file name: ")

    if not file_name:
        print("File name cannot be empty")
        return

    with open(file_name, "w") as f:
        pass

    print(f"File '{file_name}' created successfully")