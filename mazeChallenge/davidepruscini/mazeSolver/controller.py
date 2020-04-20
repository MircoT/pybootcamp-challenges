# -*- coding: utf-8 -*-
"""
The Maze Challenge - Controller for interact with MazeEngine
Author: prushh
"""
from pynput.keyboard import Listener

from .functions import get_response, pprint, to_dict
from .mazeClient import Commands as command


class Controller:
    '''
    Class that contains methods to use client controller.
    '''

    def __init__(self, debug):
        '''
        Initialize flag for prints debug information,
        creates act_map for key-action association.
        '''
        self.debug = debug
        self.act_map = {
            'w': command.MOVE_UP,
            'a': command.MOVE_LEFT,
            's': command.MOVE_DOWN,
            'd': command.MOVE_RIGHT,
            'f': command.GET_STATE,
            'e': command.EXIT
        }

    def explore_maze(self):
        '''
        Listen for keys pressed.
        '''
        with Listener(on_press=self._on_press) as listener:
            listener.join()

    def _on_press(self, key):
        '''
        Sends the action to do based on key pressed.
        '''
        try:
            # Check if key correspond to an action
            if key.char in self.act_map.keys():
                action = self.act_map[key.char]
                if self.debug:
                    print(action)
                if key.char == 'e':
                    return False
                tmp = get_response(action)
                if key.char == 'f':
                    pprint(to_dict(tmp))
        except AttributeError:
            # Cleans terminal after an illegal key
            self._flush_input()

    def _flush_input(self):
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
            import sys
            import termios
            termios.tcflush(sys.stdin, termios.TCIOFLUSH)
