# -*- coding: utf-8 -*-
"""
The Maze Challenge - Main
Author: prushh
"""
import argparse
from time import sleep

from mazeClient import Commands as command

from engine import execute, kill
from controller import Controller
from functions import to_dict, get_response
from statistics import plt_colors_dist, plt_xy_dist

class Maze():
    '''
    Class for move inside maze and collect statistics.
    '''
    def __init__(self):
        '''
        Initialize structures to store data.
        '''
        self.visited = []
        self.colors_x = {}
        self.colors_y = {}
        self.colors_count = {
            'white': 0,
            'blue': 0,
            'green': 0,
            'red': 0
        }

        # Get start node information
        cur_node = to_dict(get_response(command.GET_STATE))
        self.visited.append({
            'x': cur_node['userX'],
            'y': cur_node['userY'],
            'val': cur_node['userVal']
        })

        # Start maze exploration
        self.explore(cur_node, command.GET_STATE)

    def __reverse_action(self, action: str) -> str:
        '''
        Returns reversed action based on key-value pair.
        ex: UP -> DOWN
        '''
        inv_act = {
            command.MOVE_UP: command.MOVE_DOWN,
            command.MOVE_DOWN: command.MOVE_UP,
            command.MOVE_LEFT: command.MOVE_RIGHT,
            command.MOVE_RIGHT: command.MOVE_LEFT,
            command.GET_STATE: command.GET_STATE
        }
        return inv_act[action]

    def __get_color_name(self, color: int) -> str:
        '''
        Returns color name specified by int code.
        ex: 32 -> white
        '''
        colors_code = {
            32: 'white',
            66: 'blue',
            71: 'green',
            82: 'red'
        }
        return colors_code[color]

    def __increment_coord_color(self, node: dict):
        '''
        Update the color frequency distribution
        for XY coordinates.
        '''
        x = node['x']
        y = node['y']
        c_code = node['val']
        dict_ = {
            'white': 0,
            'blue': 0,
            'green': 0,
            'red': 0
        }

        # If key does not exists create
        # and fill it with default value
        self.colors_x.setdefault(x, dict_)
        self.colors_y.setdefault(y, dict_)
        self.colors_x[x][self.__get_color_name(c_code)] += 1
        self.colors_y[y][self.__get_color_name(c_code)] += 1

    def __increment_color(self, color: int):
        '''
        Update the frequency of colors find in the maze.
        '''
        self.colors_count[self.__get_color_name(color)] += 1

    def __get_action(self, org: dict, dst: dict) -> str:
        '''
        Returns action to do based on position of
        origin and destination node.
        '''
        if dst['x'] == org['userX']:
            if dst['y'] == org['userY']+1:
                return command.MOVE_LEFT
            if dst['y'] == org['userY']-1:
                return command.MOVE_RIGHT
        if dst['y'] == org['userY']:
            if dst['x'] == org['userX']+1:
                return command.MOVE_UP
            if dst['x'] == org['userX']-1:
                return command.MOVE_DOWN
        # Unnecessary condition for diagonals
        return command.GET_STATE

    def __get_valid_neighbors(self, cur_node: dict) -> dict:
        '''
        Returns a list of valid neighbors, the accepted
        directions are: UP, DOWN, LEFT, RIGTH.
        '''
        valid = []
        for neighbor in cur_node['Neighbors']:
            # Nodes with same X or Y are accepted
            if (
                neighbor['x'] == cur_node['userX'] or
                neighbor['y'] == cur_node['userY']
            ):
                valid.append(neighbor)
        return valid

    def explore(self, cur_node: dict, last_act: str):
        '''
        Core for maze solver. It is a recursive function
        inspired to Depth-First-Search logic.
        '''
        neighbors = self.__get_valid_neighbors(cur_node)
        for neighbor in neighbors:
            if neighbor not in self.visited:
                self.visited.append(neighbor)
                self.__increment_coord_color(neighbor)
                self.__increment_color(neighbor['val'])

                action = self.__get_action(cur_node, neighbor)
                new_node = to_dict(get_response(action))
                if args.debug:
                    print(action)
                    sleep(0.5)

                self.explore(new_node, action)
        # There are not other valid near node,
        # reverse last action and go back
        reverse_act = self.__reverse_action(last_act)
        get_response(reverse_act)
        if args.debug:
            print(reverse_act)
            sleep(0.5)


def main():
    if args.controller and not args.no_stats:
        print(
            "ERROR: controller mode does not work"
            " without --no_stats argument..."
        )
        return 1

    pid = execute(args.file_path)
    if pid == -1:
        return 1

    if args.controller:
        print(
            "Controller Mode\n"
            " - Use WASD keys to move around the maze\n"
            " - Press F to inspect\n"
            " - Press E to exit"
        )
        Controller(args.debug).explore_maze()
    else:
        print(
            "Classic maze solver\n"
            "Waiting for engine..."
        )
        sleep(3)
        maze = Maze()
        if args.no_stats:
            print(f"Total cells visited: {len(maze.visited)}")
        else:
            print("Show statistics!")
            plt_colors_dist(maze.colors_count)
            plt_xy_dist(maze.colors_x, maze.colors_y)

    kill(pid)
    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="""
        \t\t'The Maze Challenge' by MircoT
        \t\t\tSolution by prushh
        ------------------------------------------------------------
        There are two modes of use:
         - Classic maze solver with stats
         - Controller mode (disable stats)
        You must specify mazeEngine.ext path for parallel execution.
        """,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        usage='%(prog)s file_path [--no_stats] [-c] [-d] [-h]'
    )
    parser.add_argument(
        'file_path', type=str,
        help='executable file to start engine'
    )
    parser.add_argument(
        '-c', '--controller',
        default=False,
        action='store_true',
        help='controller mode for interact with engine'
    )
    parser.add_argument(
        '--no_stats',
        default=False,
        action='store_true',
        help='hide statistical information'
    )
    parser.add_argument(
        '-d', '--debug',
        default=False,
        action='store_true',
        help='print debug information and more'
    )

    args = parser.parse_args()
    exit(main())
