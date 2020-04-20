# Echo client program
import socket

_HOST = 'localhost'
_PORT = 34242

__all__ = ['send_command', 'Commands']


class Commands:
    MOVE_UP = "MOVE_UP"
    MOVE_DOWN = "MOVE_DOWN"
    MOVE_RIGHT = "MOVE_RIGHT"
    MOVE_LEFT = "MOVE_LEFT"
    GET_STATE = "GET_STATE"
    EXIT = "EXIT"


class _MazeCommand:
    MOVE_UP = b'moveUp'
    MOVE_DOWN = b'moveDown'
    MOVE_RIGHT = b'moveRight'
    MOVE_LEFT = b'moveLeft'
    GET_STATE = b'state'
    EXIT = b'exit'


def send_command(command: str) -> str:
    if command in vars(_MazeCommand):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            cur_command = getattr(_MazeCommand, command)
            sock.connect((_HOST, _PORT))
            sock.sendall(cur_command + b'\n')
            data = sock.recv(1024)
        return data
    return f'Error: command {command} not valid...'
