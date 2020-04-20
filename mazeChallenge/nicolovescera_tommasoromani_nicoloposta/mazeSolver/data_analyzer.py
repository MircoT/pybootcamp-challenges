import matplotlib.pyplot as plt
import pandas as pd

from .plotter import load_data


def plot_coordinata(data: pd.DataFrame, coordinata: str, alpha_value=1.0, title="Grafico 1"):
    """Stampa il dataframe passatogli come istogramma"""
    data = data[[coordinata, 'color']]

    rosse = data[data['color'] == 'red'].groupby(coordinata).count()
    blu = data[data['color'] == 'blue'].groupby(coordinata).count()
    verdi = data[data['color'] == 'green'].groupby(coordinata).count()

    ax = pd.concat([rosse, verdi, blu], axis=1).plot(
        kind='bar', color=['r', 'g', 'b'])
    ax.legend(["R", "G", "B"])
    ax.set_title(title)


def cell_stats(data: pd.DataFrame):
    """Conta il totale delle celle e il colore"""
    colors = data['color'].value_counts()

    print(
        f"\nIl totale delle celle nel labirinto è di {data['color'].count()}.\n")

    # Tolgo le celle bianche
    colors.drop('white', inplace=True)

    for color, value in colors.iteritems():
        print(f"{color}:\t{value}")


def plot_stats(confronto=False):
    """Stampa a video gli istogrammi, se invocata con True confronta
    le due distribuzioni nei relativi istogrammi"""
    data = load_data("data.csv")

    if confronto:
        data2 = load_data("data2.csv")

    if not confronto:
        cell_stats(data)

    plot_coordinata(data, 'x')
    if confronto:
        plot_coordinata(data2, 'x', alpha_value=0.5, title="Grafico 2")

    plot_coordinata(data, 'y')
    if confronto:
        plot_coordinata(data2, 'y', alpha_value=0.5, title="Grafico 2")

    plt.show()
