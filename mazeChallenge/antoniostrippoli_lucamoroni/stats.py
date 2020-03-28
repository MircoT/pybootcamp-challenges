# -*- coding: utf-8 -*-
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap


def plot_map(visited: list):
    """
    Plots the map constructing a matrix.
    Remember that x = row index, y = column index.
    """
    # Colors mapping for matshow library method
    colors_map = {82: 1, 71: 2, 66: 3, 32: 4}
    cmap = ListedColormap(['k', 'r', 'g', 'b', 'w'])
    
    # Get the coordinates max and min
    x_min = min(visited, key=lambda el:el['x'])['x']
    x_max = max(visited, key=lambda el:el['x'])['x']
    y_min = min(visited, key=lambda el:el['y'])['y']
    y_max = max(visited, key=lambda el:el['y'])['y']

    matrix_plt = np.zeros((x_max - x_min + 1, y_max - y_min + 1))
    for el in visited:
        matrix_plt[
            x_max - el["x"],
            y_max - el["y"]
        ] = colors_map[el["val"]]

    # Plotting the matrix
    plt.matshow(matrix_plt, cmap=cmap)
    plt.suptitle('Maze representation')
    plt.xticks(range(0, y_max-y_min+1, 2), range(y_max, y_min-1, -2))
    plt.yticks(range(0, x_max-x_min+1, 2), range(x_max, x_min-1, -2))
    plt.show()


def plot_colors_dist(nodes_count: dict):
    """
    Additional plot that shows colors distribution in the map (not requested by any quest) 
    """
    # Prepare data
    names = list(nodes_count.keys())
    values = list(nodes_count.values())
    colors = ['0.5', 'r', 'g', 'b']
    total_cells = sum(nodes_count.values())

    # Plot
    fig, ax = plt.subplots()
    fig.suptitle(f"Colors distribution (total cells: {total_cells})")
    rects = ax.bar(names, values, color=colors, align='center')

    # Attach a text label above each bar in rects, displaying its height
    for rect in rects:
        height = rect.get_height()
        ax.annotate('{}'.format(height),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 1),  # 1 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom')

    plt.show()


def plot_colors_xy_dist(maze: "Maze", past_maze: "Maze"):
    """
    Plot a grouped bar chart that represents colors distribution on x and y
    """
    def preprocess_data_hist(colors_xy: tuple):
        """
        Internal function that preprocess data for matplotlib
        """
        colors_x, colors_y = colors_xy

        x_label = []
        x_red   = []
        x_green = []
        x_blue  = []
        x_white = []
        
        y_label = []
        y_red   = []
        y_green = []
        y_blue  = []
        y_white = []

        for key in sorted(colors_x):
            x_label.append(key)
            x_red.append(colors_x[key]["red"])
            x_green.append(colors_x[key]["green"])
            x_blue.append(colors_x[key]["blue"])
            x_white.append(colors_x[key]["white"])

        for key in sorted(colors_y):
            y_label.append(key)
            y_red.append(colors_y[key]["red"])
            y_green.append(colors_y[key]["green"])
            y_blue.append(colors_y[key]["blue"])
            y_white.append(colors_y[key]["white"])

        return x_label, x_red, x_green, x_blue, x_white, y_label, y_red, y_green, y_blue, y_white


    def plot_axes(ax1, ax2, colors_xy, label="", width=0.2):
        """
        Internal function that plots colors distribution on given axes
        Width is used to determine the width of each bar
        """
        # Preprocess data
        x_label, x_red, x_green, x_blue, x_white, y_label, y_red, y_green, y_blue, y_white = preprocess_data_hist(colors_xy)

        # Prepare bars for colors x distribution
        x = np.arange(len(x_label))
        ax1.bar(x - 3*width/2, x_red, width, label='Red', color="red")
        ax1.bar(x - width/2, x_green, width, label='Green', color="green")
        ax1.bar(x + width/2, x_blue, width, label='Blue', color="blue")
        ax1.bar(x + 3*width/2, x_white, width, label='White', color="grey")

        # Add some text for labels, title and custom x-axis tick labels, etc.
        ax1.set_ylabel('Frequency')
        ax1.set_title(label + "X (rows)")
        ax1.set_xticks(x)
        ax1.set_xticklabels(x_label)

        # Prepare bars for colors y distribution
        y = np.arange(len(y_label))  # the label locations
        ax2.bar(y - 3*width/2, y_red, width, label='Red', color="red")
        ax2.bar(y - width/2, y_green, width, label='Green', color="green")
        ax2.bar(y + width/2, y_blue, width, label='Blue', color="blue")
        ax2.bar(y + 3*width/2, y_white, width, label='White', color="grey")

        # Add some text for labels, title and custom x-axis tick labels, etc.
        ax2.set_ylabel('Frequency')
        ax2.set_title(label + "Y (cols)")
        ax2.set_xticks(y)
        ax2.set_xticklabels(y_label)


    # Create figure, axes and then plot
    if past_maze:
        fig, ((ax11, ax12), (ax21, ax22)) = plt.subplots(2,2)
        plot_axes(ax21, ax22, (past_maze.colors_x, past_maze.colors_y), label="PAST maze color distribution on ")
    else:
        fig, (ax11, ax12) = plt.subplots(1,2)
    
    fig.set_size_inches(12, 8)
    plot_axes(ax11, ax12, (maze.colors_x, maze.colors_y), label="CURRENT maze color distribution on ")
    plt.show()