from time import sleep

from .bfs_search import bfs_search, COMMAND
from .controls import del_seed, open_maze
from .data_analyzer import plot_stats
from .mazeClient import send_command


# Genera 2 grafici e li confronta
def confronto():
    bfs_search()
    send_command(COMMAND.EXIT)

    del_seed()
    open_maze()

    sleep(0.5)

    bfs_search(confronto=True)
    send_command(COMMAND.EXIT)

    plot_stats(confronto=True)  # Stampa i grafici
