"""
This module contains functions for expression operations.
"""


import collections


_Op = collections.namedtuple('Op', [
    'precedence',
    'associativity'])


_RIGHT, _LEFT = 0,1


_OPS = {
    '^': _Op(precedence=4, associativity=_RIGHT),
    '*': _Op(precedence=3, associativity=_LEFT),
    '/': _Op(precedence=3, associativity=_LEFT),
    '+': _Op(precedence=2, associativity=_LEFT),
    '-': _Op(precedence=2, associativity=_LEFT)}


def has_precedence(a, b):
    """Compare two opeartors a and b.
    1. If b is right associativity and has lower precedence than a, return True
    2. If b is left associativity and has lower or same precedence with a, return True
    3. Otherwise, return False
    """
    return ((_OPS[b].associativity == _RIGHT and
             _OPS[a].precedence > _OPS[b].precedence) or
            (_OPS[b].associativity == _LEFT and
             _OPS[a].precedence >= _OPS[b].precedence))


def postfix(e):
    """Convert infix expression to postfix expression and return
    a list that contains all the tokens in postfix order.
    """
    index = 0
    q = []
    op = []
    while index < len(e):
        token = e[index]
        if is_digit(token):
            d = ""
            while index < len(e) and is_digit(e[index]):
                d += e[index]
                index += 1
            q.append(d)
            index -= 1
        elif is_letter(token):
            d = ""
            while index < len(e) and is_letter(e[index]):
                d += e[index]
                index += 1
            q.append(d)
            index -= 1
        elif token == "(":
            op.append(token)
        elif is_symbol(token):
            if len(op) > 0:
                while len(op) > 0 and op[-1] != "(" and has_precedence(op[-1], token):
                    q.append(op.pop())
                op.append(token)
            else:
                op.append(token)
        elif token == ")":
            while len(op) > 0 and op[-1] != "(":
                q.append(op.pop())
            op.pop()
        index += 1
    while len(op) > 0:
        q.append(op.pop())
    return q


def is_symbol(s):
    """Return True if given str is a symbol, which means
    it is in '+,-,*,/,^', False otherwise.
    """
    return s in "+-*/^"


def is_digit(s):
    """Return True if given str is a digit, which means it
    is in '0,1,2,3,4,5,6,7,8,9', False otherwise.
    """
    return s in "1234567890"

def is_letter(s):
    return s.isalpha()