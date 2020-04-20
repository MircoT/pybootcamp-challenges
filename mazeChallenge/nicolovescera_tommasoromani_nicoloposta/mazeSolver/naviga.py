import getch

from .mazeClient import send_command
from .mazeClient import Commands as command


def move(input: str) -> str:
    """Capice quale comando mandare al server usando freccie direzionali
    come input"""
    option = {
        "H": command.MOVE_UP,
        "P": command.MOVE_DOWN,
        "M": command.MOVE_RIGHT,
        "K": command.MOVE_LEFT
    }

    return send_command(option[input])


def free_move():
    """Permette di muoversi liberamente nel labirinto"""
    fine = False
    print("Per muoversi usare le freccie direzionali.\nPer uscire digitare q.")
    while not fine:
        # Controllo del caratere inserito
        escape = getch.getch()  # Prende il primo carattere delle freccie direzionali
        if escape != b'\x00':
            if escape == b'q':
                fine = True
                continue

            print("Carattere invalido !")
            continue

        char_ = getch.getch()   # Prende il secondo carattere delle freccie direzionali

        move(char_.decode("ascii"))
