# -*- coding: utf-8 -*-
"""
The Maze Challenge - Useful functions
Author: prushh
"""
import json

from mazeClient import send_command


def get_response(action: str) -> bytes:
    '''
    Returns the engine response.
    '''
    return send_command(action)


def to_dict(data: bytes) -> dict:
    '''
    Decode bytes to ASCII and returns a dict.
    '''
    return json.loads(data.decode('ascii'))


def pprint(data: dict, tab=2):
    '''
    Pretty print for dict, default indent value is two.
    '''
    print(json.dumps(data, indent=tab))
