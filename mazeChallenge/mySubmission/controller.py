# -*- coding: utf-8 -*-
"""
The Maze Challenge - Controller for interact with MazeEngine
Author: prushh
"""
import argparse

from pynput.keyboard import Key, Listener

from mazeClient import send_command
from mazeClient import Commands as command

from engine import execute, kill
from functions import to_dict, pprint

def flush_input():
    '''
    Flush the keyboard input buffer.
    '''
    try:
        # Windows
        import msvcrt
        while msvcrt.kbhit():
            msvcrt.getch()
    except ImportError:
        # Linux, MacOS
        import sys, termios
        termios.tcflush(sys.stdin, termios.TCIOFLUSH)


def do_action(key):
    '''
    Returns the action to do base on key pressed.
    '''
    act_map = {
        'w': command.MOVE_UP,
        'a': command.MOVE_LEFT,
        's': command.MOVE_DOWN,
        'd': command.MOVE_RIGHT,
        'f': command.GET_STATE,
        'e': command.EXIT
    }

    try:
        # Check if key correspond to an action
        if key.char in act_map.keys():
            action = act_map[key.char]
            if args.debug:
                print(action)
            if key.char == 'e':
                return False
            tmp = send_command(action)
            if key.char == 'f':
                pprint(to_dict(tmp))
    except AttributeError:
        flush_input()


def main():
    pid = execute(args.file_path)
    if pid == -1:
        return 1

    print(
        " - Use WASD keys to move around the maze\n"
        " - Press F for inspect\n"
        " - Press E to exit\n"
    )
    with Listener(on_press=do_action) as listener:
        listener.join()

    kill(pid)
    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Allows the use of WASD keys to move around the maze,"
                    " specify mazeEngine.ext path for parallel execution."
    )
    parser.add_argument(
        'file_path', type=str,
        help='executable file for launch the engine'
    )
    parser.add_argument(
        '-d', '--debug',
        action='store_true',
        help='print commands sent'
    )

    args = parser.parse_args()
    exit(main())
