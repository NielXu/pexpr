"""
This module contains functions for expression operations.
"""


import collections
import re


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


basic_opeartors_mapper = {
    "+": lambda x,y : x+y,
    "-": lambda x,y : x-y,
    "*": lambda x,y : x*y,
    "/": lambda x,y : x/y,
    "^": lambda x,y : x**y
}


function_mapper = {
    "max": lambda x,y : max(x, y),
    "min": lambda x,y : min(x, y),
    "sin": None
}


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
    return s in basic_opeartors_mapper


def is_func(s):
    """Return True if its
    """
    pass


def is_digit(s):
    """Return True if given str is a digit, which means it
    is in '0,1,2,3,4,5,6,7,8,9', False otherwise.
    """
    return s in "1234567890"


def is_letter(s):
    """Return True if the given str is a alphabet, which
    means it is in 'a-z,A-Z', False otherwise.
    """
    return s.isalpha()


def tokenize(e):
    """Tokenize the expression and return a list that contains
    all the tokens from start to end. Please notice that ','
    will be ignored. And also, tokenizer will not recongize
    any wrong patterns or errors in the expression.
    """
    index = 0
    eindex = 0
    result = []
    starts, ends = _match_regex(_func_regex(), e)
    while index < len(e):
        if index in starts:
            result.append(e[index: ends[eindex]])
            index = ends[eindex]
            eindex += 1
            continue
        token = e[index]
        if is_digit(token):
            d = ""
            while index < len(e) and is_digit(e[index]):
                d += e[index]
                index += 1
            result.append(d)
            index -= 1
        elif is_letter(token):
            d = ""
            while index < len(e) and is_letter(e[index]):
                d += e[index]
                index += 1
            result.append(d)
            index -= 1
        elif is_symbol(token) or token == "(" or token == ")":
            result.append(token)
        index += 1
    return result


def _func_regex():
    "Construct regex for special math functions"
    regex = "("
    for f in function_mapper:
        if "(" in f:
            index = f.find("(")
            regex += f[:index] + "\\" + f[index:] + "|"
        else:
            regex += f + "|"
    return regex[:-1] + ")"


def _match_regex(r, e):
    "Match the functions regex and return a list of start indices and a list of end indices"
    reg = re.compile(r)
    starts, ends = [], []
    for m in reg.finditer(e):
        starts.append(m.start())
        ends.append(m.end())
    return starts, ends

print(tokenize("sin(1+max(2,3*pi))"))