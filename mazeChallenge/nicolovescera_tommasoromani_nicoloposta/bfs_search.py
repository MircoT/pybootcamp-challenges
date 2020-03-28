import json
import mazeClient
from cella import Cella


# Comandi di maze client
command = mazeClient.Commands

visitate    = []   # Lista celle visitate
cammino     = []    # Lista cammino per il traceback


# Toglie le celle adiacenti (vicini) diagonali alla cella passata
def remove_usless_neigh(me: Cella, vicini: dict) -> list:
    cont = 0

    tmp = vicini.copy()

    for elem in vicini:
        if elem['x'] != me.x:
            if elem['y'] != me.y:
                del tmp[cont]
                cont -= 1
        cont += 1
    return tmp


# Capisce come muoversi tra le celle vicine, e aggiunge il movimento fatto e l'inverso alla coda
def movimento(cella_attuale: Cella, vicini: list) -> bool:
    for neigh in vicini:
        # Controlla se c'è un vicino non visitato
        trovato = False
        for cell in visitate:
            if (neigh['x'] == cell.x and neigh['y'] == cell.y):
                trovato = True
        #---------------------------------------#

        if not trovato:
            if cella_attuale.y < neigh['y'] and cella_attuale.x == neigh['x']:
                mazeClient.send_command(command.MOVE_LEFT)
                cammino.append((command.MOVE_LEFT, command.MOVE_RIGHT))

            elif cella_attuale.y > neigh['y'] and cella_attuale.x == neigh['x']:
                mazeClient.send_command(command.MOVE_RIGHT)
                cammino.append((command.MOVE_RIGHT, command.MOVE_LEFT))

            elif cella_attuale.y == neigh['y'] and cella_attuale.x < neigh['x']:
                mazeClient.send_command(command.MOVE_UP)
                cammino.append((command.MOVE_UP, command.MOVE_DOWN))

            elif cella_attuale.y == neigh['y'] and cella_attuale.x > neigh['x']:
                mazeClient.send_command(command.MOVE_DOWN)
                cammino.append((command.MOVE_DOWN, command.MOVE_UP))

            return True     # Si è mosso
    return False            # Non ha trovato vicini validi, inizio traceback


# Tornando indietro controllo se ci sono vicini non visitati
def traceback() -> bool:
    while True:
        # Se 0 sono tornato alla cella di inizio
        if len(cammino) == 0:
            return False    # Algoritmo finito

        cmd = cammino.pop()
        mazeClient.send_command(cmd[1])

        me = json.loads(mazeClient.send_command(command.GET_STATE))
        vicini = remove_usless_neigh(Cella(me), me['Neighbors'])

        for neigh in vicini:
            trovato = False

            # Controlla se c'è un vicino non visitato
            for cell in visitate:
                if (neigh['x'] == cell.x and neigh['y'] == cell.y):
                    trovato = True

            if not trovato:
                return True # La cella dove sono tornato ha ancora vicini da visitare


# Creazione file csv con nome passatogli
def create_csv(nome: str):
    with open(nome, 'w') as myfile:
        myfile.write("x,y,color\n")
        for elem in visitate:
            myfile.write(elem.to_csv())


# Analizza l'intero grafo, se invocata con True permette di analizzarne un secondo
def bfs_search(confronto=False):
    inizio = True
    while len(cammino) != 0 or inizio:
        inizio = False

        obj_cell = json.loads(mazeClient.send_command(command.GET_STATE))
        cell_attuale = Cella(obj_cell)

        # Controlla se la cella è già stata visitata, in caso la aggiunge alla coda visitate
        to_append = False
        for cell in visitate:
            if cell.x == cell_attuale.x and cell.y == cell_attuale.y:
                to_append = True

        if not to_append:
            visitate.append(cell_attuale)
        #-----------------------------------------------------------------------------------#

        # Se la cella non ha vicini da visitare inizia il traceback
        if not movimento(cell_attuale, remove_usless_neigh(cell_attuale, obj_cell['Neighbors'])):
            test = traceback()
            
            # Se il traceback ritorna True la cella ha vicini non visitati, quindi ricomincio ad esplorare
            if test:
                new_cell = json.loads(mazeClient.send_command(command.GET_STATE))
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

    visitate.clear()
    cammino.clear()

    print("FATTO !\n")
