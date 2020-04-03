# -*- coding: utf-8 -*-
from mazeClient import Commands as command
from mazeClient import send_command
from pynput import keyboard


def on_press(key):
    """
    Listen for input and move if any of 'WASD' is pressed
    Exit if any other key is pressed
    """
    # Not a valid key pressed?
    if not hasattr(key, 'char'):
        return False
    if not key.char in keycode_map:
        return False
    
    # Map keycode to action and execute action
    action = keycode_map[key.char]
    res = send_command(action)

    # Just some print to let user have some feedback
    if action == command.GET_STATE:
        print(res)
    else:
        print(action)


if __name__ == "__main__":
    # Initialize mapping variable
    keycode_map = {
        'w': command.MOVE_UP,
        'a': command.MOVE_LEFT,
        's': command.MOVE_DOWN,
        'd': command.MOVE_RIGHT,
        'e': command.GET_STATE
    }
    
    print("INSTRUCTIONS:\n\tWASD -> Move around the maze;\n\tE -> GET STATE;\n\tAny other Key: QUIT")
    # Collect events until released
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()