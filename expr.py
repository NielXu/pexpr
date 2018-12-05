"""
This module contains functions for expression operations.
"""


import random
import collections
import re
import math


_Op = collections.namedtuple('Op', [
    'precedence',
    'associativity'])


_RIGHT, _LEFT = 0,1


_OPS = {
    '^': _Op(precedence=4, associativity=_RIGHT),
    '*': _Op(precedence=3, associativity=_LEFT),
    '/': _Op(precedence=3, associativity=_LEFT),
    '+': _Op(precedence=2, associativity=_LEFT),
    '-': _Op(precedence=2, associativity=_LEFT),
    '~': _Op(precedence=2, associativity=_LEFT)
}


# Symbols contains every operators and math functions
symbols = {

}


# operators_mapper contains basic operators: +-*/^
opeartors_mapper = {
    "+": lambda x,y : x+y,
    "-": lambda x,y : x-y,
    "*": lambda x,y : x*y,
    "/": lambda x,y : x/y,
    "^": lambda x,y : x**y
}
symbols.update(opeartors_mapper)


# function_mapper contains both binary math functions and unary math functions
function_mapper = {

}


# binary_function_mapper contains functions that require two values
binary_function_mapper = {
    "max": lambda x,y : max(x, y),
    "min": lambda x,y : min(x, y),
    "log": lambda x,y : math.log(x,y)
}
function_mapper.update(binary_function_mapper)


# unary_function_mapper contains functions that require only one value
unary_function_mapper = {
    # TRIG
    "sin": lambda x : math.sin(x),
    "cos": lambda x : math.cos(x),
    "tan": lambda x : math.tan(x),
    "asin":lambda x : math.asin(x),
    "acos":lambda x : math.acos(x),
    "atan":lambda x : math.atan(x),

    # LOG
    "lg":  lambda x : math.log10(x),
    "ln":  lambda x : math.log(x),

    # USEFUL
    "sqrt":lambda x : math.sqrt(x),
    "abs": lambda x : abs(x),

    "~": lambda x : -x
}
function_mapper.update(unary_function_mapper)
symbols.update(function_mapper)


special_number = {
    "e":  math.e,
    "pi": math.pi
}


class token():
    def __init__(self, sym, is_num=False, is_func=False,
                    is_dummy=False, is_oper=False,
                    is_leftb=False, is_rightb=False):
        self.sym = sym
        self.is_num = is_num
        self.is_func = is_func
        self.is_dummy = is_dummy
        self.is_oper = is_oper
        self.is_leftb = is_leftb
        self.is_rightb = is_rightb
    
    def __str__(self):
        return "token(sym=" + str(self.sym) +\
                    ", is_func=" + str(self.is_func) +\
                    ", is_num=" + str(self.is_num) +\
                    ", is_dummy=" + str(self.is_dummy) +\
                    ", is_oper=" + str(self.is_oper) +\
                    ", is_leftb=" + str(self.is_leftb) +\
                    ", is_rightb=" + str(self.is_rightb) +\
                    ")"
    
    def __repr__(self):
        return self.__str__()


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
    tokens = tokenize(e)
    q = []
    op = []
    index = 0
    while index < len(tokens):
        token = tokens[index]
        if token.is_num or token.is_dummy:
            q.append(token)
        if token.is_leftb:
            op.append(token)
        elif token.is_oper:
            if len(op) > 0:
                while len(op) > 0 and (op[-1].is_func or (op[-1].sym != "(" and has_precedence(op[-1].sym, token.sym))):
                    q.append(op.pop())
                op.append(token)
            else:
                op.append(token)
        elif token.is_rightb:
            while len(op) > 0 and op[-1].sym != "(":
                q.append(op.pop())
            op.pop()
        elif token.is_func:
            op.append(token)
        index += 1
    while len(op) > 0:
        q.append(op.pop())
    return [x.sym for x in q]


def is_symbol(s):
    """Return True if given str is a symbol, which means
    it is in '+,-,*,/,^', False otherwise.
    """
    return s in opeartors_mapper


def is_evaluable(s):
    """Return True if the given expression is evaluable,
    False otherwise.
    """
    tokens = tokenize(s)
    for token in tokens:
        if token.is_dummy and token.sym not in special_number:
            return False
    return True


def is_unary(s):
    """Return True if given str is a unary operator, which means
    it is in 'sin, cos, tan, acos, asin, atan, log, ln, abs` and
    so on, False otherwise.
    """
    return s in unary_function_mapper


def is_func(s):
    """Return True if given str is a function operator, no matter
    binary or unary, False otherwise.
    """
    return s in function_mapper


def is_digit(s):
    """Return True if given str is a digit, which means it
    is in '0,1,2,3,4,5,6,7,8,9', False otherwise.
    """
    return s in "1234567890."


def is_number(s):
    """Return True if given str is a number, different from
    `is_digit`, this function will check the complete string
    """
    try:
        float(s)
        return True
    except ValueError:
        return False


def is_letter(s):
    """Return True if the given str is a alphabet, which
    means it is in 'a-z,A-Z', False otherwise.
    """
    return s.isalpha()


def is_special_number(s):
    """Return True if the given str is a special number,
    for example, pi, e, False otherwise.
    """
    return s in special_number


def rand_exp(n, low, high, basic_only=True, int_only=True):
    """Generate a random expressions with random operators, math
    functions and numbers. And the numbers in the expression are
    restricted by the given n value
    """
    if basic_only:
        return _gen_rand_exp_oper(1, n, low, high, int_only)
    else:
        return _gen_rand_exp(1, n, low, high, int_only)


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
            result.append(token(e[index: ends[eindex]], is_func=True))
            index = ends[eindex]
            eindex += 1
            continue
        t = e[index]
        if is_digit(t):
            t, index = _sub_num(index, e)
            result.append(t)
        elif is_letter(t):
            t, index = _sub_dummy(index, e)
            result.append(t)
        elif t == "(":
            result.append(token(t, is_leftb=True))
        elif t == ")":
            result.append(token(t, is_rightb=True))
        elif is_symbol(t):
            if t == "-":
                if index > 0:
                    prev, next_t = e[index-1], e[index+1]
                    if is_digit(prev) or is_letter(prev) or prev == ")":
                        result.append(token(t, is_oper=True))
                    elif index + 1 in starts:
                        result.append(token("~", is_oper=True))
                    elif is_digit(next_t):
                        index += 1
                        t, index = _sub_num(index, e, "-")
                        result.append(t)
                    elif is_letter(next_t):
                        index += 1
                        t, index = _sub_dummy(index, e, "-")
                        result.append(t)
                    else:
                        result.append(token("~", is_oper=True))
                else:
                    next_t = e[index+1]
                    if is_digit(next_t):
                        index += 1
                        t, index = _sub_num(index, e, "-")
                        result.append(t)
                    elif index + 1 in starts:
                        result.append(token("~", is_oper=True))
                    elif is_letter(next_t):
                        index += 1
                        t, index = _sub_dummy(index, e, "-")
                        result.append(t)
                    else:
                        result.append(token("~", is_oper=True))
            elif t == "^":
                if len(result) >= 1:
                    prev = result[-1]
                    if (prev.is_num or prev.is_dummy) and prev.sym[0] == "-":
                        result[-1] = token("~", is_oper=True)
                        result.append(token(prev.sym[1:], is_num=prev.is_num, is_dummy=prev.is_dummy))
                result.append(token(t, is_oper=True))
            else:
                result.append(token(t, is_oper=True))
        index += 1
    return result


def _gen_rand_exp_oper(n, m, low, high, int_only):
    "Generate expression with basic operators only"
    rand = random.choice(list(opeartors_mapper.keys()))
    rand_a = str(random.randint(low, high)) if int_only else str(random.uniform(low, high))
    rand_b = str(random.randint(low, high)) if int_only else str(random.uniform(low, high))
    if n == m:
        return "("+rand_a+rand+rand_b+")"
    else:
        dec = random.randint(0, 2)
        if dec == 0:
            return "("+_gen_rand_exp_oper(n+1, m, low, high, int_only)+ rand + _gen_rand_exp_oper(n+1, m, low, high, int_only)+")"
        elif dec == 1:
            return "("+rand_a + rand + _gen_rand_exp_oper(n+1, m, low, high, int_only)+")"
        else:
            return "("+_gen_rand_exp_oper(n+1, m, low, high, int_only)+ rand + rand_b+")"


def _gen_rand_exp(n, m, low, high, int_only):
    rand = random.choice(list(symbols.keys()))
    if is_func(rand):
        if is_unary(rand):
            if n == m:
                rand_number = str(random.randint(low, high)) if int_only else str(random.uniform(low, high))
                return rand+"("+rand_number+")"
            else:
                return rand+"("+_gen_rand_exp(n+1, m, low, high, int_only)+")"
        else:
            rand_a = str(random.randint(low, high)) if int_only else str(random.uniform(low, high))
            rand_b = str(random.randint(low, high)) if int_only else str(random.uniform(low, high))
            if n == m:
                return rand+"("+rand_a+","+rand_b+")"
            else:
                dec = random.randint(0, 2)
                if dec == 0:
                    return rand + "("+_gen_rand_exp(n+1, m, low, high, int_only)+ "," + _gen_rand_exp(n+1, m, low, high, int_only)+")"
                elif dec == 1:
                    return rand + "("+rand_a + "," + _gen_rand_exp(n+1, m, low, high, int_only)+")"
                else:
                    return rand + "("+_gen_rand_exp(n+1, m, low, high, int_only)+ "," + rand_b+")"
    else:
        rand_a = str(random.randint(low, high)) if int_only else str(random.uniform(low, high))
        rand_b = str(random.randint(low, high)) if int_only else str(random.uniform(low, high))
        if n == m:
            return "("+rand_a + rand + rand_b+")"
        else:
            dec = random.randint(0, 2)
            if dec == 0:
                return "("+_gen_rand_exp(n+1, m, low, high, int_only)+ rand + _gen_rand_exp(n+1, m, low, high, int_only)+")"
            elif dec == 1:
                return "("+rand_a + rand + _gen_rand_exp(n+1, m, low, high, int_only)+")"
            else:
                return "("+_gen_rand_exp(n+1, m, low, high, int_only)+ rand + rand_b+")"


def _sub_dummy(index, e, prev=""):
    d = prev
    while index < len(e) and is_letter(e[index]):
        d += e[index]
        index += 1
    index -= 1
    return token(d, is_dummy=True), index


def _sub_num(index, e, prev=""):
    d = prev
    while index < len(e) and (is_digit(e[index]) or e[index] == "."):
        d += e[index]
        index += 1
    index -= 1
    return token(d, is_num=True), index


def _sub_func(index, e, prev):
    d = prev
    while index < len(e) and is_digit(e[index]):
        d += e[index]
        index += 1
    index -= 1
    return token(d, is_func=True), index


def _func_regex():
    "Construct regex for special math functions"
    regex = "("
    for f in function_mapper:
        if "(" in f:
            index = f.find("(")
            regex += f[:index] + "\\" + f[index:] + "|"
        else:
            regex += f + "|"
    for f in unary_function_mapper:
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
