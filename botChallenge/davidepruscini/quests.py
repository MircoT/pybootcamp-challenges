# -*- coding: utf-8 -*-
"""
Bot Challenge - Quests framework and useful functions
Author: prushh
"""
from random import randint
from base64 import b64decode

# Number of quests
NUM_QTS = 3


def create_qts() -> dict:
    '''
    Create a dict of quests with random data.
    '''

    # Prepare parameters for quests
    n = randint(0, 99)
    last = randint(0, 9999)
    str_ = 'SGVsbG8sIFB56K6t57uD6JClIQ==%!(EXTRA int=89)'

    quests = {
        0: {'text': f'Calcola la somma dei multipli di 3 e 5 fino a {last}',
            'solution': _quest0(last),
            'solved': False},
        1: {'text': f'Calcola la somma dei numeri dispari della serie di fibonacci fino al {n}-esimo',
            'solution': _quest1(n),
            'solved': False},
        2: {'text': 'Decodifica la stringa: SGVsbG8sIFB56K6t57uD6JClIQ==%!(EXTRA int=21)',
            'solution': _quest2(str_),
            'solved': False}
    }

    return quests


def check_choice(qts: dict, n: int) -> str:
    '''
    Check if the question can be answered.
    '''
    if qts[n]['solved']:
        return "Hai già completato questa quest..."

    for idx in range(0, n):
        if not qts[idx]['solved']:
            return "Devi completare la quest precedente..."
    return qts[n]['text']


def check_qts(context, n: int) -> str:
    '''
    Check if the answer is correct.
    '''
    reply = "Risposta non corretta..."
    if 'quests' not in context.user_data.keys():
        return reply

    qts = context.user_data['quests'][n]
    if qts['solved']:
        return reply

    args = " ".join(context.args)
    if _cast_arg(args) == qts['solution']:
        context.user_data['quests'][n]['solved'] = True
        return "Risposta corretta! Quest completata!"
    return reply


def get_solved(qts: dict) -> int:
    '''
    Count the number of solved quests.
    '''
    return sum(elm['solved'] is True for elm in qts.values())


def _cast_arg(arg: str) -> int:
    '''
    Returns the correct type for arg.
    '''
    def is_int(tmp) -> bool:
        '''Try int casting.'''
        try:
            int(tmp)
            return True
        except ValueError:
            return False

    if is_int(arg):
        return int(arg)
    return arg


def _quest0(last: int) -> int:
    '''
    Calculate the sum of multiples of 3 and 5 to the last.
    '''
    sum_ = 0
    for elm in range(last):
        if elm % 3 == 0 or elm % 5 == 0:
            sum_ += elm

    return sum_


def _quest1(n: int) -> int:
    '''
    Calculate the sum of the odd numbers in the series
    of fibonacci up to the nth.
    '''
    n += 2
    sum_ = -1

    a, b = 0, 1
    while n > 0:
        if a % 2 != 0:
            sum_ += a
        a, b = b, a + b
        n -= 1

    return sum_


def _quest2(str_: str) -> str:
    '''
    Decode b64 strings.
    '''
    return b64decode(str_).decode('utf-8')
