import json

from .cella import Cella
from .mazeClient import Commands, send_command

# Comandi di maze client
COMMAND = Commands

_VISITATE = []   # Lista celle
_CAMMINO = []    # Lista cammino per il traceback


def remove_usless_neigh(me: Cella, vicini: dict) -> list:
    """Toglie le celle adiacenti (vicini) diagonali alla cella passata"""
    cont = 0

    tmp = vicini.copy()

    for elem in vicini:
        if elem['x'] != me.x:
            if elem['y'] != me.y:
                del tmp[cont]
                cont -= 1
        cont += 1
    return tmp


def movimento(cella_attuale: Cella, vicini: list) -> bool:
    """Capisce come muoversi tra le celle vicine, e aggiunge
    il movimento fatto e l'inverso alla coda"""
    for neigh in vicini:
        # Controlla se c'è un vicino non visitato
        trovato = False
        for cell in _VISITATE:
            if (neigh['x'] == cell.x and neigh['y'] == cell.y):
                trovato = True
        #---------------------------------------#

        if not trovato:
            if cella_attuale.y < neigh['y'] and cella_attuale.x == neigh['x']:
                send_command(COMMAND.MOVE_LEFT)
                _CAMMINO.append((COMMAND.MOVE_LEFT, COMMAND.MOVE_RIGHT))

            elif cella_attuale.y > neigh['y'] and cella_attuale.x == neigh['x']:
                send_command(COMMAND.MOVE_RIGHT)
                _CAMMINO.append((COMMAND.MOVE_RIGHT, COMMAND.MOVE_LEFT))

            elif cella_attuale.y == neigh['y'] and cella_attuale.x < neigh['x']:
                send_command(COMMAND.MOVE_UP)
                _CAMMINO.append((COMMAND.MOVE_UP, COMMAND.MOVE_DOWN))

            elif cella_attuale.y == neigh['y'] and cella_attuale.x > neigh['x']:
                send_command(COMMAND.MOVE_DOWN)
                _CAMMINO.append((COMMAND.MOVE_DOWN, COMMAND.MOVE_UP))

            return True     # Si è mosso
    return False            # Non ha trovato vicini validi, inizio traceback


def traceback() -> bool:
    """Tornando indietro controllo se ci sono vicini non visitati"""
    while True:
        # Se 0 sono tornato alla cella di inizio
        if len(_CAMMINO) == 0:
            return False    # Algoritmo finito

        cmd = _CAMMINO.pop()
        send_command(cmd[1])

        me = json.loads(send_command(COMMAND.GET_STATE))
        vicini = remove_usless_neigh(Cella(me), me['Neighbors'])

        for neigh in vicini:
            trovato = False

            # Controlla se c'è un vicino non visitato
            for cell in _VISITATE:
                if (neigh['x'] == cell.x and neigh['y'] == cell.y):
                    trovato = True

            if not trovato:
                return True  # La cella dove sono tornato ha ancora vicini da visitare


def create_csv(nome: str):
    """Creazione file csv con nome passatogli"""
    with open(nome, 'w') as myfile:
        myfile.write("x,y,color\n")
        for elem in _VISITATE:
            myfile.write(elem.to_csv())


def bfs_search(confronto=False):
    """Analizza l'intero grafo, se invocata con True permette di
    analizzarne un secondo"""
    inizio = True
    while len(_CAMMINO) != 0 or inizio:
        inizio = False

        obj_cell = json.loads(send_command(COMMAND.GET_STATE))
        cell_attuale = Cella(obj_cell)

        # Controlla se la cella è già stata visitata, in caso la aggiunge alla coda _VISITATE
        to_append = False
        for cell in _VISITATE:
            if cell.x == cell_attuale.x and cell.y == cell_attuale.y:
                to_append = True

        if not to_append:
            _VISITATE.append(cell_attuale)
        #-----------------------------------------------------------------------------------#

        # Se la cella non ha vicini da visitare inizia il traceback
        if not movimento(cell_attuale, remove_usless_neigh(cell_attuale, obj_cell['Neighbors'])):
            test = traceback()

            # Se il traceback ritorna True la cella ha vicini non visitati, quindi ricomincio ad esplorare
            if test:
                new_cell = json.loads(
                    send_command(COMMAND.GET_STATE))
                tmp = Cella(new_cell)

                # Se movimento ritorna False, non ci sono più celle da visitare
                if not movimento(tmp, remove_usless_neigh(tmp, new_cell['Neighbors'])):
                    break

    # Creo i csv
    print("Esporto i dati in CSV ...")
    if confronto:
        create_csv("data2.csv")
    else:
        create_csv("data.csv")

    _VISITATE.clear()
    _CAMMINO.clear()

    print("FATTO !\n")
