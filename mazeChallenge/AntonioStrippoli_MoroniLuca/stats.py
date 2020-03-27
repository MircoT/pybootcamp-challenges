# -*- coding: utf-8 -*-
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap


def plot_map(visited):
    """
    Plots the map constructing a matrix
    """
    # Colors mapping for matshow library method
    colors_map = {82: 1, 71: 2, 66: 3, 32: 4}
    cmap = ListedColormap(['k', 'r', 'g', 'b', 'w'])
    
    # Get the coordinates max and min
    x_min = min(visited, key=lambda el:el['x'])['x']
    x_max = max(visited, key=lambda el:el['x'])['x']
    y_min = min(visited, key=lambda el:el['y'])['y']
    y_max = max(visited, key=lambda el:el['y'])['y']

    # Create Matrix plot
    matrix_plt = np.zeros((x_max + 1, y_max + 1))
    for el in visited:
        matrix_plt[
            x_max - el["x"] + 1,
            y_max - el["y"] + 1
        ] = colors_map[el["val"]]

    # Plotting the matrix
    plt.matshow(matrix_plt, cmap=cmap)

    plt.xlim((0, y_max - y_min + 2))
    plt.ylim((x_max - x_min + 2, 0))
    
    plt.show()


def plot_colors_dist(nodes_count):
    """
    Additional plot that shows colors distribution in the map
    """
    # Preare data
    names = list(nodes_count.keys())
    values = list(nodes_count.values())
    colors = ['0.5', 'r', 'g', 'b']

    # Concat values near names
    for i in range(len(names)):
        names[i] += f"\n{values[i]}"

    # Plot
    fig, axs = plt.subplots(1, 3, figsize=(9, 4), sharey=True)
    axs[0].bar(names, values, color=colors)
    axs[1].scatter(names, values)
    axs[2].plot(names, values)
    fig.suptitle("Colors distribution")

    plt.show()


def plot_colors_xy_dist(past_plot: list, actual_plot: list):
    """
    Bla bla
    """

    def preprocess_data_hist(to_plot: list):
        """
        Bla bla
        """
        x_colors = {}
        y_colors = {}

        # molteplici riscritture, struttura di appoggio, necessaria per gestire i dati satellite durante il 
        # riordinamento, sfetchando ordinatamente nel popolamento delle liste di output
        for el in to_plot:

            x_colors[el["x"]] = {
                'red':0,
                'green':0,
                'blue':0,
                'white':0
            }

            y_colors[el["y"]] = {
                'red':0,
                'green':0,
                'blue':0,
                'white':0
            }

        for el in to_plot:

            x = el["x"]
            y = el["y"]

            if el["val"] == 82:
                x_colors[x]['red'] += 1
                y_colors[y]['red'] += 1 # red
            elif el["val"] == 71:
                x_colors[x]['green'] += 1
                y_colors[y]['green'] += 1 # green
            elif el["val"] == 66:
                x_colors[x]['blue'] += 1
                y_colors[y]['blue'] += 1 # blue
            elif el["val"] == 32:
                x_colors[x]['white'] += 1
                y_colors[y]['white'] += 1 # white

        x_s = []
        x_red = []
        x_green = []
        x_blue = []
        x_white = []

        for key in sorted(x_colors):
            x_s.append(key)
            x_red.append(x_colors[key]["red"])
            x_green.append(x_colors[key]["green"])
            x_blue.append(x_colors[key]["blue"])
            x_white.append(x_colors[key]["white"])

        y_s = []
        y_red = []
        y_green = []
        y_blue = []
        y_white = []

        for key in sorted(y_colors):
            y_s.append(key)
            y_red.append(y_colors[key]["red"])
            y_green.append(y_colors[key]["green"])
            y_blue.append(y_colors[key]["blue"])
            y_white.append(y_colors[key]["white"])


        return x_s, x_red, x_green, x_blue, x_white, y_s, y_red, y_green, y_blue, y_white

    # nested function used only for this purpose
    def autolabel(ax, rects):
        """Attach a text label above each bar in *rects*, displaying its height."""
        for rect in rects:
            height = rect.get_height()
            ax.annotate('{}'.format(height),
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom')

    
    fig, ((ax11, ax12), (ax21, ax22)) = plt.subplots(2,2)

    def plot_axes(ax1, ax2, to_plot):

        if len(to_plot) == 0:
            return

        x_s, x_red, x_green, x_blue, x_white, y_s, y_red, y_green, y_blue, y_white = preprocess_data_hist(to_plot)

        width = 0.2  # the width of the bars

        # ---------------------- X

        x = np.arange(len(x_s))  # the label locations

        rect_red = ax1.bar(x - 3*width/2, x_red, width, label='Red', color="red")
        rect_green = ax1.bar(x - width/2, x_green, width, label='Green', color="green")
        rect_blue = ax1.bar(x + width/2, x_blue, width, label='Blue', color="blue")
        rect_white = ax1.bar(x + 3*width/2, x_white, width, label='White', color="grey")

        # Add some text for labels, title and custom x-axis tick labels, etc.
        ax1.set_ylabel('Frequency')
        ax1.set_title('Frequencies for X variable')
        ax1.set_xticks(x)
        ax1.set_xticklabels(x_s)
        ax1.legend()

        autolabel(ax1, rect_red)
        autolabel(ax1, rect_blue)
        autolabel(ax1, rect_green)
        autolabel(ax1, rect_white)

        leg = ax1.get_legend()
        leg.legendHandles[0].set_color('red')
        leg.legendHandles[1].set_color('green')
        leg.legendHandles[2].set_color('blue')
        leg.legendHandles[3].set_color('grey')


        # ---------------------------Y

        y = np.arange(len(y_s))  # the label locations

        rect_red1 = ax2.bar(y - 3*width/2, y_red, width, label='Red', color="red")
        rect_green1 = ax2.bar(y - width/2, y_green, width, label='Green', color="green")
        rect_blue1 = ax2.bar(y + width/2, y_blue, width, label='Blue', color="blue")
        rect_white1 = ax2.bar(y + 3*width/2, y_white, width, label='White', color="grey")

        # Add some text for labels, title and custom x-axis tick labels, etc.
        ax2.set_ylabel('Frequency')
        ax2.set_title('Frequencies for Y variable')
        ax2.set_xticks(y)
        ax2.set_xticklabels(y_s)
        ax2.legend()

        autolabel(ax2, rect_red1)
        autolabel(ax2, rect_blue1)
        autolabel(ax2, rect_green1)
        autolabel(ax2, rect_white1)

        leg = ax2.get_legend()
        leg.legendHandles[0].set_color('red')
        leg.legendHandles[1].set_color('green')
        leg.legendHandles[2].set_color('blue')
        leg.legendHandles[3].set_color('grey')


    plot_axes(ax11, ax12, past_plot)
    plot_axes(ax21, ax22, actual_plot)

    # fig.tight_layout()
    fig.set_size_inches(18.5, 10.5)

    plt.show()