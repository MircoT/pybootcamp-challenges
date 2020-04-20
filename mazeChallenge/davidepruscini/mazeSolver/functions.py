# -*- coding: utf-8 -*-
"""
The Maze Challenge - Useful functions
Author: prushh
"""
import gzip
import json
import pickle

from .mazeClient import send_command


def get_pickle_obj(colors_xy: dict) -> dict:
    '''
    Check the old pickle file and compare it
    to the current color distribution.
    '''
    old_data = {}
    name_file = 'previous_maze.pickle'

    try:
        with gzip.open(name_file, 'rb') as handle:
            old_data = pickle.load(handle)
    except FileNotFoundError:
        pass
    if old_data == colors_xy:
        old_data = {}
        print("Color frequency distribution not saved, same as the previous one...")
    else:
        print("Save XY color frequency distribution to pickle file...")
        with gzip.open(name_file, 'wb') as handle:
            pickle.dump(colors_xy, handle, protocol=pickle.HIGHEST_PROTOCOL)

    return old_data


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
