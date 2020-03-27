# -*- coding: utf-8 -*-
import mazeClient
from getch import getch


def get_arrow_key():
    # We are not interested in first two values

    first_ch = ord(getch())

    if first_ch == 113:
        return command.EXIT
    if first_ch != 27:
        return None
    if ord(getch()) != 91:
        return None

    input_char = ord(getch())

    if input_char == 65:
        return command.MOVE_UP
    elif input_char == 66:
        return command.MOVE_DOWN
    elif input_char == 67:
        return command.MOVE_RIGHT
    elif input_char == 68:
        return command.MOVE_LEFT
    return None


def main():
    while True:
        action = get_arrow_key()
        mazeClient.send_command(action)
        if action == command.EXIT:
            break


if __name__ == "__main__":
    command = mazeClient.Commands
    main()
