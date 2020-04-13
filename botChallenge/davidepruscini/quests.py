# -*- coding: utf-8 -*-
"""
Bot Challenge - Quests framework and useful functions
Author: prushh
"""
from math import pi
from random import randint
from base64 import b64decode
from datetime import datetime

from natural.text import nato


# Number of quests
NUM_QTS = 6


def get_now(time: bool = True) -> str:
    '''
    Return current date.
    '''
    if time:
        return datetime.now().strftime('%Y/%m/%d %H:%M:%S')
    return datetime.now().strftime('%Y/%m/%d')


def create_qts() -> dict:
    '''
    Create a dict of quests with random data.
    '''
    def to_dict(text: str, solution, solved: bool = False) -> dict:
        '''
        Convert quest to dict
        '''
        qts = {
            'text': text,
            'solution': solution,
            'solved': solved
        }
        return qts

    # Prepare parameters for quests
    n = randint(0, 99)
    text = 'PyBootCamp'
    idx = randint(1, 48)
    last = randint(0, 9999)
    date = get_now(time=False)
    b64 = 'SGVsbG8sIFB56K6t57uD6JClIQ==%!(EXTRA int=89)'

    quests = {
        0: to_dict(
            f'Calcola la somma dei multipli di 3 e 5 fino a {last}',
            _quest0(last)),
        1: to_dict(
            f'Calcola la somma dei numeri dispari della serie di fibonacci fino al {n}-esimo',
            _quest1(n)),
        2: to_dict(
            f'Decodifica la stringa: {b64}',
            _quest2(b64)),
        3: to_dict(
            f'Trova la cifra decimale numero {idx} del π',
            _quest3(idx)),
        4: to_dict(
            f'Trova una differente rappresentazione: {date}',
            _quest4(date)),
        5: to_dict(
            f'Conosci qualche alfabeto? Prova a fare lo spelling: {text}',
            _quest5(text))
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

    context.user_data['quests'][n]['attemp'] += 1
    reply += f" Tentativi effettuati: {qts['attemp']}"
    return reply


def get_solved(qts: dict) -> int:
    '''
    Count the number of solved quests.
    '''
    return sum(elm['solved'] is True for elm in qts.values())


def _cast_arg(arg: str):
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


def _quest2(b64: str) -> str:
    '''
    Decode b64 strings.
    '''
    return b64decode(b64).decode('utf-8')


def _quest3(nth: int) -> int:
    '''
    Find the nth digit of pi-greco.
    '''
    idx = nth + 1
    tmp = "%.48f" % pi
    return int(tmp[idx])


def _quest4(date: str) -> int:
    '''
    Date '%Y-%m-%d' to timestamp.
    '''
    return int(datetime.strptime(date, "%Y/%m/%d").timestamp())


def _quest5(text: str) -> str:
    '''
    Transform text using the NATO spelling alphabet.
    '''
    return nato(text)
