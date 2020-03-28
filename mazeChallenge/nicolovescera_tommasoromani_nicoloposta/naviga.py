import mazeClient
import getch

command = mazeClient.Commands

# Capice quale comando mandare al server usando freccie direzionali come input
def move(input: str) -> str:
    option = {
        "H": command.MOVE_UP,
        "P": command.MOVE_DOWN,
        "M": command.MOVE_RIGHT,
        "K": command.MOVE_LEFT
    }

    return mazeClient.send_command(option[input])


# Permette di muoversi liberamente nel labirinto
def free_move():
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
