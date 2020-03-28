import numpy as np
import pandas as pd
from colorama import Back, init


# Dizionario per stampa di colori a video
dict_colori2 = {'white': 1, 'red': 2, 'blue': 3, 'green': 4}


# Carica i dati del file passato in un DataFrame
def load_data(fname: str) -> pd.DataFrame:
    data = pd.read_csv(fname)

    return data

# Stampa a video della Mappa
def print_matrix(matrice: np.ndarray):
    str_ = ""
    for i in range(len(matrice)):
        for j in range(len(matrice)):
            if matrice[i][j] == 0:
                str_ += Back.BLACK + "  "
            elif matrice[i][j] == 1:
                str_ += Back.WHITE + "  "
            elif matrice[i][j] == 2:
                str_ += Back.RED + "  "
            elif matrice[i][j] == 3:
                str_ += Back.BLUE + "  "
            elif matrice[i][j] == 4:
                str_ += Back.GREEN + "  "

        str_ += Back.BLACK + "\n"
    print(str_)


# Creazione e modifica della matrice prima della stampa a video
def plot_maze():
    init(autoreset=True)    # Server per l'output colorato

    data = load_data('data.csv')

    max_x = data['x'].max()
    max_y = data['y'].max()

    massimo = max(max_y, max_x)

    matrice = np.zeros((massimo, massimo), dtype=int)

    # Sistema le coordinate nella matrice
    for _, row in data.iterrows():
        matrice[- int(row['x']) % massimo][- int(row['y']) % massimo] = dict_colori2[row['color']]

    print_matrix(matrice)
    print("\nLa mappa è orientata come nel MazeEngine.\nLa riga delle X inizia dal basso verso l'alto.\nLa riga delle Y parte da destra a sinitra nelle verticali.\n")    
