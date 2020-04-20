import json
import os
from time import sleep

import matplotlib.pyplot as plt
import numpy as np

import mazeClient

# reminder:
# down moovment: decrease x
# up moovment: increase x
# right moovment: decrease y
# left moovment: increase y

# 82: red
# 32: white
# 71: green
# 66: blue


def find_dimension(explored_maze):
    first_cell = explored_maze[0]
    x_max = first_cell["x"]
    y_max = first_cell["y"]
    x_min = first_cell["x"]
    y_min = first_cell["y"]
    for elm in explored_maze:
        if elm["x"] > x_max:
            x_max = elm["x"]
        if elm["x"] < x_min:
            x_min = elm["x"]
        if elm["y"] > y_max:
            y_max = elm["y"]
        if elm["y"] < y_min:
            y_min = elm["y"]
    return x_max, x_min, y_max, y_min


def is_in_maze(explored_maze, block):
    for elm in explored_maze:
        if elm["x"] == block["x"] and elm["y"] == block["y"]:
            return True
    return False


def get_stats(explored_maze):
    values = {}
    values["total"] = 0
    values["red"] = 0
    values["white"] = 0
    values["blue"] = 0
    values["green"] = 0
    for block in explored_maze:
        values["total"] += 1
        cur_value = block["val"]
        if cur_value == 82:
            values["red"] += 1
        elif cur_value == 32:
            values["white"] += 1
        elif cur_value == 71:
            values["green"] += 1
        elif cur_value == 66:
            values["blue"] += 1
    return values


def print_map(explored_maze, pos):

    x = pos["x"]
    y = pos["y"]

    x_max, x_min, y_max, y_min = find_dimension(explored_maze)
    lenght = x_max - x_min + 1
    width = y_max - y_min + 1

    size = (width, lenght)

    _map = np.zeros(size)

    for i in reversed(range(lenght)):
        for j in reversed(range(width)):
            check = False
            for elm in explored_maze:
                if elm["x"] == i + x_min and elm["y"] == j + y_min:
                    check = True
            if check:
                _map[j, i] = 1
            else:
                _map[j, i] = 0

    for i in range(width + 2):
        print("@", end="")
    print("")
    for i in reversed(range(lenght)):
        print("@", end="")
        for j in reversed(range(width)):
            if i == x - x_min and j == y - y_min:
                print("0", end="")
                # print("0", end = "")
            elif _map[j, i] == 1:
                print(" ", end="")
            else:
                print("#", end="")
        print("@")
    for i in range(width + 2):
        print("@", end="")


def filter_neighbors(neighbors, block):
    filtered = []
    for elm in neighbors:
        if not(elm["x"] != block["x"] and elm["y"] != block["y"]):
            filtered.append(elm)
    available_directions(filtered, block)
    return filtered


def available_directions(neighbors, block):
    print("Aviable direction: ", end="")
    for elm in neighbors:
        if elm["x"] > block["x"]:
            print("up ", end="")
        elif elm["x"] < block["x"]:
            print("down ", end="")
        elif elm["y"] > block["y"]:
            print("left ", end="")
        elif elm["y"] < block["y"]:
            print("right ", end="")
    print("")


def frequency_distribution(explored_maze):
    values = get_stats(explored_maze)
    absFreq = ["red"]*values["red"] + ["green"]*values["green"] + \
        ["white"]*values["white"] + ["blue"]*values["blue"]
    plt.hist(absFreq, density=False)
    plt.show()


def exploration(command):

    explored_maze = []
    _exit = False

    while not _exit:

        res = mazeClient.send_command(command.GET_STATE)
        pos = json.loads(res)
        print(pos)

        elm = {}
        elm["x"] = pos["userX"]
        elm["y"] = pos["userY"]
        elm["val"] = pos["userVal"]
        if is_in_maze(explored_maze, elm) == False:
            explored_maze.append(elm)

        for block in pos["Neighbors"]:
            if is_in_maze(explored_maze, block) == False:
                explored_maze.append(block)

        os.system("clear")
        print("")
        print_map(explored_maze, elm)
        print("")
        values = get_stats(explored_maze)
        print("Total: " + str(values["total"]) + ", red: " + str(values["red"]) + ", green: " + str(
            values["green"]) + ", blue: " + str(values["blue"]) + ", white: " + str(values["white"]))
        filter_neighbors(pos["Neighbors"], elm)
        print("Select option:\nW) Up\nS) Down\nR) Right\nA) Left\nE) Exit\nP) Plot stats\n")
        sel = input()
        if sel == "w" or sel == "W":
            mazeClient.send_command(command.MOVE_UP)
        elif sel == "s" or sel == "S":
            mazeClient.send_command(command.MOVE_DOWN)
        elif sel == "d" or sel == "D":
            mazeClient.send_command(command.MOVE_RIGHT)
        elif sel == "a" or sel == "A":
            mazeClient.send_command(command.MOVE_LEFT)
        elif sel == "e" or sel == "E":
            _exit = True
        elif sel == "p" or sel == "P":
            frequency_distribution(explored_maze)
        else:
            print("Invalid")


if __name__ == '__main__':
    command = mazeClient.Commands
    exploration(command)
