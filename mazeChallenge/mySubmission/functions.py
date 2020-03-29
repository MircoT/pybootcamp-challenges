# -*- coding: utf-8 -*-
"""
The Maze Challenge - Useful functions
Author: prushh
"""
import json


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
