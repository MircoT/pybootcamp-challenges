# -*- coding: utf-8 -*-
"""
The Maze Challenge - Functions to display plot and stats
Author: prushh
"""
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.colors import ListedColormap


def _dark_subplots(nrows: int = 1, ncols: int = 1) -> tuple:
    '''
    Create subplots and set dark theme.
    '''
    plt.style.use('dark_background')
    fig, axes = plt.subplots(nrows=nrows, ncols=ncols)
    fig.patch.set_facecolor('#252526')
    if isinstance(axes, np.ndarray):
        # For multiple axes
        for i in range(len(axes)):
            for j in range(len(axes[i])):
                axes[i][j].set_facecolor('#3c3c3c')
    else:
        # For single ax
        axes.set_facecolor('#3c3c3c')

    return (fig, axes)


def plt_colors_dist(dict_: dict):
    '''
    Plot the colors distribution for all cells,
    show the number of cells for each color
    and the total cells number.
    '''
    # Prepares colors list and labels
    colors = dict_.keys()
    cap_colors = ['Green' if x == '#00ff00' else x.capitalize()
                  for x in colors]
    values = dict_.values()

    title = f'Colors distribution for {sum(values)} cells'
    ylabel = 'Number of cells'

    # Create subplot ad customize it
    fig, ax = _dark_subplots()
    fig.suptitle(title, fontsize=15)
    ax.set_ylabel(ylabel)

    bars = ax.bar(cap_colors, values, color=colors)
    # Attach a text label above each bar displaying its height
    for bar in bars:
        height = bar.get_height()
        if height > 0:
            ax.text(
                bar.get_x() + bar.get_width()/2.,
                height+0.01,
                height,
                ha='center',
                va='bottom'
            )
    plt.show()


def plt_xy_dist(xy_freq: dict, old_xy_freq: dict):
    '''
    Plot the histogram of the color frequency
    distribution for X e Y coordinates.
    If old_freq is not empty, show the previous distribution.
    '''
    # Prepares colors list and labels
    colors = xy_freq['x'][list(xy_freq['x'].keys())[0]].keys()
    title = 'Colors distribution for XY coordinates'
    title_x = 'X distribution'
    title_y = 'Y distribution'
    old_title_x = f'Old {title_x}'
    old_title_y = f'Old {title_y}'
    ylabel = 'Number of cells'

    # Creates pandas.DataFrame (more simple to manage) and sort them for index
    # Current maze information
    df_x = pd.DataFrame.from_dict(xy_freq['x'], orient='index').sort_index()
    df_y = pd.DataFrame.from_dict(xy_freq['y'], orient='index').sort_index()

    # Create subplot ad customize it
    fig, axes = _dark_subplots(nrows=2, ncols=2)
    fig.suptitle(title, fontsize=15)
    df_x.plot.bar(figsize=(12, 8), ax=axes[0][0], yticks=_get_max_tick(
        df_x), color=colors, legend=False)
    df_y.plot.bar(ax=axes[0][1], yticks=_get_max_tick(
        df_y), color=colors, legend=False)
    axes[0][0].set(title=title_x, ylabel=ylabel)
    axes[0][1].set(title=title_y)

    if len(old_xy_freq):
        # Old maze information
        old_df_x = pd.DataFrame.from_dict(
            old_xy_freq['x'], orient='index').sort_index()
        old_df_y = pd.DataFrame.from_dict(
            old_xy_freq['y'], orient='index').sort_index()

        # Create subplot ad customize it
        old_df_x.plot.bar(ax=axes[1][0], yticks=_get_max_tick(
            old_df_x), color=colors, legend=False)
        old_df_y.plot.bar(ax=axes[1][1], yticks=_get_max_tick(
            old_df_y), color=colors, legend=False)

        axes[1][0].set(title=old_title_x, ylabel=ylabel)
        axes[1][1].set(title=old_title_y)

    plt.show()


def plt_map(visited: list):
    '''
    Plot the explored maze as a map.
    '''
    title = 'Map of the explored maze'
    cmap = ListedColormap(['black', 'white', 'blue', '#00ff00', 'red'])
    colors_code = {
        32: 1,
        66: 2,
        71: 3,
        82: 4
    }

    # Simple solution for max/min with pd.DataFrame
    df = pd.DataFrame(visited)
    min_x = df.x.min()
    min_y = df.y.min()
    max_x = df.x.max()
    max_y = df.y.max()

    # Returns a new 2-D array of int, filled with zeros
    matrix = np.zeros(_get_dimensions(max_x, min_x, max_y, min_y), dtype=int)
    for node in visited:
        x = max_x - node["x"]
        y = max_y - node["y"]
        # Fills matrix position with
        # the color_code converted
        matrix[x, y] = colors_code[node["val"]]

    # Create subplot ad customize it
    fig, ax = _dark_subplots()
    fig.suptitle(title, fontsize=15)
    ax.matshow(matrix, cmap=cmap)
    plt.xticks(_get_range(max_y, min_y), _get_range(max_y, min_y, True))
    plt.yticks(_get_range(max_x, min_x), _get_range(max_x, min_x, True))

    plt.show()


def _get_dimensions(max_x: int, min_x: int, max_y: int, min_y: int) -> tuple:
    '''
    Returns width and length for matrix creation,
    based on coordinates max/min value.
    '''
    width = max_x - min_x + 1
    length = max_y - min_y + 1
    return (width, length)


def _get_range(max_: int, min_: int, reverse=False):
    '''
    Returns range for ticks in the plot.
    '''
    if reverse:
        return range(max_, min_ - 1, -2)
    return range(0, max_ - min_ + 1, 2)


def _get_max_tick(df: 'pd.DataFrame') -> range:
    '''
    Returns the max value from pandas DataFrame as a whole.
    '''
    return range(0, df.max().max() + 1)
