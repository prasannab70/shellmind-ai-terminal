import os

def analyze_architecture(root="."):

    structure = {}

    for path, dirs, files in os.walk(root):

        structure[path] = files

    return structure