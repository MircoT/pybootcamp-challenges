import os
import subprocess
import sys


def del_seed():
    cmd = ""

    # Controlla il sistema operativo
    if sys.platform in ["win64", "win32", "win86"]:
        cmd = "del seed.maze"
    else:
        cmd = "rm -f seed.maze"

    os.system(cmd)


def open_maze():
    cmd = ""

    system = sys.platform
    # Controlla il sistema operativo
    if system in ["win64", "win32", "win86"]:
        cmd = "mazeEngine.win.exe"
    elif "linux" in system:
        cmd = "./mazeEngine.linux.run"
    else:
        cmd = "./mazeEngine.mac.run"

    try:
        # subprocess permette di non dover aspettare l'output del comando
        subprocess.Popen(cmd)
    except FileNotFoundError:
        print("Inserire il mazeEngine nella cartella di esecuzione del Main!")
        quit()
