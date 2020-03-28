import mazeClient
import argparse
import controls
import sys
from time import sleep
from bfs_search import bfs_search
from plotter import plot_maze
from naviga import free_move
from data_analyzer import plot_stats
from confronto import confronto


def main():
    # Creazione del menu Help
    parser = argparse.ArgumentParser(description='Maze Navigation.')

    parser.add_argument('--free_move', action='store_true', help='Permette di muovere il labirinto senza analizzarlo con le freccie direzionali e si può uscire dal programma digitando q.')
    parser.add_argument('--move_map', action='store_true', help='Permette di muovere il labirinto dopo averlo analizzato ed avere la mappa stampata.')
    parser.add_argument('--confront', action='store_true', help='Permette il confronto e la stampa sullo stesso istogramma delle frequenze dei colori RGB rispettivi agli assi di due labirinti differenti.')

    args = parser.parse_args()

    if len(sys.argv) > 2:
        print("Troppi argomenti !")
        return -1

    # Controlla se il mazeEngine è in esecuzione, sennò lo avvia
    try:
        mazeClient.send_command(mazeClient.Commands().GET_STATE)
    except ConnectionRefusedError:
        print("Il Maze Client è chiuso... Lo apro!")
        controls.open_maze()
        sleep(0.5)

    if args.free_move:
        free_move()
        mazeClient.send_command(mazeClient.Commands().EXIT)
        return 0

    if args.confront:
        confronto()
        return 0

    bfs_search()

    plot_maze()

    plot_stats()

    if args.move_map:
        free_move()

    mazeClient.send_command(mazeClient.Commands().EXIT)

if __name__ == '__main__':
    main()
