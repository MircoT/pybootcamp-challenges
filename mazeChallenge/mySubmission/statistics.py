# -*- coding: utf-8 -*-
"""
The Maze Challenge - Functions to display plot and stats
Author: prushh
"""
import matplotlib.pyplot as plt


def _dark_subplots() -> tuple:
    '''
    Create subplots and set dark theme.
    '''
    plt.style.use('dark_background')
    fig, ax = plt.subplots()
    fig.patch.set_facecolor('#252526')
    ax.set_facecolor('#3c3c3c')

    return (fig, ax)


def plt_colors_dist(dict_: dict):
    '''
    Plot the colors distribution for all cells,
    show the number of cells for each color
    and the total cells number.
    '''
    colors = dict_.keys()
    cap_colors = [elm.capitalize() for elm in colors]
    values = dict_.values()

    title = f'Colors distribution in {sum(values)} cells'
    ylabel = 'Number of cells'

    _, ax = _dark_subplots()
    ax.set(title=title, ylabel=ylabel)

    y_top = max(values)
    plt.ylim(top=y_top+1.2)

    bars = ax.bar(cap_colors, values, color=colors)
    # Attach a text label above each bar displaying its height
    for bar in bars:
        height = bar.get_height()
        if height > 0:
            ax.text(
                bar.get_x() + bar.get_width()/2.,
                height*1.02,
                height,
                ha='center',
                va='bottom'
            )
    plt.show()


def plt_xy_dist(x_freq: dict, y_freq: dict):
    pass
