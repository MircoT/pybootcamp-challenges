# -*- coding: utf-8 -*-
"""
MazeChallenge - by MircoT
Solvers: Antonio Strippoli, Luca Moroni
"""
from mazeClient import send_command
from mazeClient import Commands as command
import json
import pickle
from time import sleep
from stats import plot_map, plot_colors_dist, plot_colors_xy_dist


class Maze():
    """
    Class that contains methods to solve the maze
    """
    def __init__(self):
        # Initialize variables used to collect data from maze
        # visited = map representation
        # colors_xy = distribution of colors on x,y axes
        # colors_count = count of each color present in the map
        self.visited = []
        self.colors_x = {}
        self.colors_y = {}
        self.colors_count = {
            'red':   0,
            'green': 0,
            'blue':  0,
            'white': 0
        }

        # Initialize map to better manage colors
        self.c_map = {
            82: 'red',
            71: 'green',
            66: 'blue',
            32: 'white'
        }

        # Visit the root (starting position)
        curr_node = self.get_dict(send_command(command.GET_STATE))
        self.visited.append({
            'x': curr_node['userX'],
            'y': curr_node['userY'],
            'val': curr_node['userVal']
        })

        # Explore the maze
        self.dfs_visit(curr_node, command.GET_STATE)


    def get_dict(self, data: bytes):
        """
        Parse data and returns a dictionary (more usable)
        """
        return json.loads(data.decode('ascii'))


    def get_inverse_command(self, cmd: "mazeClient.Commands"):
        """
        Returns the "Go Back" command
        """
        cmd_map = {
            command.MOVE_LEFT:  command.MOVE_RIGHT,
            command.MOVE_RIGHT: command.MOVE_LEFT,
            command.MOVE_UP:    command.MOVE_DOWN,
            command.MOVE_DOWN:  command.MOVE_UP,
            command.GET_STATE:  command.GET_STATE
        }
        return cmd_map[cmd]


    def get_command_from_pos(self, org: dict, dst: dict) -> "mazeClient.Commands":
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


    def get_reachable_neighbors(self, v: dict):
        """
        Returns valid neighbors (excludes the diagonal ones)
        """
        tmp = []
        for el in v["Neighbors"]:
            if (el["x"] - v["userX"] == 0) or (el["y"] - v["userY"] == 0):
                tmp.append(el)
        return tmp


    def visit_node(self, node: dict):
        """
        Visit a node and save informations about it
        """
        # Extract data from node
        node_x = node['x']
        node_y = node['y']
        node_color = self.c_map[node['val']]

        # Save informations
        self.visited.append(node)
        self.colors_count[node_color] += 1
        self.colors_x.setdefault(node_x, {
            'red':   0,
            'green': 0,
            'blue':  0,
            'white': 0
        })[node_color] += 1
        self.colors_y.setdefault(node_y, {
            'red':   0,
            'green': 0,
            'blue':  0,
            'white': 0
        })[node_color] += 1


    def dfs_visit(self, v: dict, last_cmd: str):
        """
        DFS Algorithm to explore the maze
        """
        for u in self.get_reachable_neighbors(v):
            if u not in self.visited:
                # Visit the neighbor
                self.visit_node(u)

                # Move to neighbor
                cmd = self.get_command_from_pos(v, u)
                u = self.get_dict(send_command(cmd))
                #sleep(0.5)

                # Visit from that neighbor
                self.dfs_visit(u, cmd)

        # Move back, no more valid neighbors
        send_command(self.get_inverse_command(last_cmd))
        #sleep(0.5)


if __name__ == '__main__':
    # Explore the Maze (Quests 1-2-3)
    maze = Maze()

    # Get data of past map (if they exist)
    try:
        with open('past_maze.pickle', 'rb') as f:
            past_maze = pickle.load(f)
    except FileNotFoundError:
        past_maze = None

    # Plot statistics of the maze (Quests 3-4-5, Advanced Quest 2)
    plot_colors_dist(maze.colors_count)
    plot_colors_xy_dist(maze, past_maze)
    plot_map(maze.visited)

    # Save current map (Part of Advanced Quest 2)
    with open('past_maze.pickle', 'wb') as f:
        pickle.dump(maze, f)