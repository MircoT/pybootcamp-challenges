import os
import subprocess
import sys

system = sys.platform


def del_seed():
    cmd = ""
    
    # Controlla il sistema operativo
    if "win64" in system or "win32" in system or "win86" in system:
        cmd = "del seed.maze"
    else:
        cmd = "rm -f seed.maze"
    
    os.system(cmd)


def open_maze():
    cmd = ""

    # Controlla il sistema operativo
    if "win64" in system or "win32" in system or "win86" in system:
        cmd = "mazeEngine.win.exe"
    elif "linux" in system:
        cmd = "./mazeEngine.linux.run"
    else:
        cmd = "./mazeEngine.mac.run"

    try:
        subprocess.Popen(cmd)   # subprocess permette di non dover aspettare l'output del comando
    except FileNotFoundError:
        print("Inserire il mazeEngine nella cartella di esecuzione del Main!")
        quit()
