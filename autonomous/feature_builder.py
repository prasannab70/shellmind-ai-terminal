import subprocess

def install_missing(package):

    try:

        subprocess.run(f"pip install {package}",shell=True)

        return f"Installed {package}"

    except:
        return "Installation failed"