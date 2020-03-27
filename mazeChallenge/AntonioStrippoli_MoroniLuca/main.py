# -*- coding: utf-8 -*-
"""
MazeChallenge - by MircoT
Solvers: Luca Moroni, Antonio Strippoli

PSEUDOCODICE ITERATIVO:
- Scegli un vicino NON visitato:
    - Vai dal vicino
- Altrimenti (nessun vicino ok):
    - Controlla se puoi andare back
        - Vai back
    - Altrimenti (sono tornato all'origine):
        - Termina
"""
import mazeClient
import json
import pickle
from time import sleep
from stats import plot_map, plot_colors_dist, plot_colors_xy_dist


def update_counter(color: int):
    """
    Update counters of tiles' colors
    """
    c_map = {
        82: 'red',
        71: 'green',
        66: 'blue',
        32: 'white'
    }
    nodes_count[c_map[color]] += 1


def get_dict(data: bytes):
    """
    Parse data and returns a dictionary (more usable)
    """
    return json.loads(data.decode('ascii'))


def inverse_command(cmd: "mazeClient.Commands"):
    """
    Returns the "Go Back" command
    """
    c = command  # More compact writing
    cmd_map = {
        c.MOVE_LEFT:  c.MOVE_RIGHT,
        c.MOVE_RIGHT: c.MOVE_LEFT,
        c.MOVE_UP:    c.MOVE_DOWN,
        c.MOVE_DOWN:  c.MOVE_UP,
        c.GET_STATE:  c.GET_STATE
    }
    return cmd_map[cmd]


def get_reachable_neighbors(v: dict):
    """
    Returns valid neighbors (excludes the diagonal ones)
    """
    tmp = []
    for el in v["Neighbors"]:
        if (el["x"] - v["userX"] == 0) or (el["y"] - v["userY"] == 0):
            tmp.append(el)
    return tmp


def get_command(org: dict, dst: dict) -> "mazeClient.Commands":
    """
    Return command to let you move from org to dst
    """
    diff_x = org['userX'] - dst['x']
    diff_y = org['userY'] - dst['y']

    if diff_x == 1:
        return command.MOVE_DOWN
    elif diff_x == -1:
        return command.MOVE_UP
    elif diff_y == 1:
        return command.MOVE_RIGHT
    elif diff_y == -1:
        return command.MOVE_LEFT
    return command.GET_STATE  # Bad usage


def dfs_visit(v: dict, last_cmd: str):
    """
    DFS Algorithm to explore the maze
    """
    for u in get_reachable_neighbors(v):
        if u not in visited:
            # Visit the neighbor
            visited.append(u)
            update_counter(u['val'])

            # Move to neighbor
            cmd = get_command(v, u)
            u = get_dict(mazeClient.send_command(cmd))
            #sleep(1)

            # Visit from that neighbor
            dfs_visit(u, cmd)

    # Move back, no more valid neighbors
    mazeClient.send_command(inverse_command(last_cmd))
    #sleep(1)


if __name__ == '__main__':
    # Initialize variables
    command = mazeClient.Commands
    visited = [] # Grey nodes
    nodes_count = {
        'white': 0,
        'red': 0,
        'green': 0,
        'blue': 0
    }

    # Visit the root (starting position)
    curr_node = get_dict(mazeClient.send_command(command.GET_STATE))
    visited.append({
        'x': curr_node['userX'],
        'y': curr_node['userY'],
        'val': curr_node['userVal']
    })

    # Start exploration
    dfs_visit(curr_node, command.GET_STATE)

    # Get data of past map (if they exist)
    try:
        with open('past_stats.pickle', 'rb') as f:
            past_visited = pickle.load(f)
    except FileNotFoundError:
        past_visited = []

    # Quests
    plot_map(visited)
    plot_colors_xy_dist(past_visited, visited)
    plot_colors_dist(nodes_count)

    # Print statistics
    print(nodes_count)

    # Save current map
    with open('past_stats.pickle', 'wb') as f:
        pickle.dump(visited, f)