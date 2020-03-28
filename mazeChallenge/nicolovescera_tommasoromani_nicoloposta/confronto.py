import mazeClient
import controls
from bfs_search import bfs_search
from bfs_search import command
from data_analyzer import plot_stats
from time import sleep

# Genera 2 grafici e li confronta 
def confronto():
    bfs_search()
    mazeClient.send_command(command.EXIT)

    controls.del_seed()
    controls.open_maze()
    
    sleep(0.5)
    
    bfs_search(confronto=True)
    mazeClient.send_command(command.EXIT)

    plot_stats(confronto=True)  # Stampa i grafici
