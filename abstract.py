"""
This module contains the abstract level of the syntax tree,
it is real abstract syntax tree
"""
import re
import binarytree
from queue import Queue


class AbstractTree():
    def __init__(self, connects_mapper, function_mapper,associativity, root=None):
        """
        connects_mapper: A map of connectives

        function_mapper: A map of functions


        associativity: The associativity of the expression, this
        is not the same as the one in connective. This defines the
        whole rule of building tree.

        root=None: Root of the tree
        """
        self.root = root
        self.cur = None
        self.associativity = associativity
        self.connects_mapper = connects_mapper
        self.function_mapper = function_mapper
    
    def copy(self):
        a = AbstractTree(self.connects_mapper, self.function_mapper, self.associativity)
        a.root = clone(self.root)
        return a
    
    def bfs(self):
        """
        Travel the tree in `breadth first search` way, which is from left to
        right and level by level. And return a list that contains the symbols.
        """
        q = Queue()
        q.put(self.root)
        s = []
        while q.qsize() > 0:
            node = q.get()
            s.append(node.sym)
            if node.left is not None:
                q.put(node.left)
            if node.right is not None:
                q.put(node.right)
        return s

    def add(self, sym):
        if self.associativity == 'left':
            self._left_append(sym)
        elif self.associativity == 'right':
            self._right_append(sym)
    
    def _left_append(self, sym):
        pass
    
    def _right_append(self, sym):
        if self.root is None:
            self.root = AbstractNode(sym)
            self.cur = self.root
        else:
            if self.is_connect_func(sym) or self.is_func(sym):
                if self.cur.right is None:
                    self.cur.right = AbstractNode(sym, self.cur)
                    self.cur = self.cur.right
                elif self.cur.left is None and not self.is_unary(self.cur.sym):
                    self.cur.left = AbstractNode(sym, self.cur)
                    self.cur = self.cur.left
                else:
                    temp = self.cur
                    while self.cur is not None and (self.cur.left is not None or self.is_unary(self.cur.sym)):
                        self.cur = self.cur.parent
                    if self.cur is None:
                        n = AbstractNode(sym)
                        n.right = self.root
                        self.root.parent = n
                        self.root = n
                        self.cur = temp
                    else:
                        self.cur.left = AbstractNode(sym, self.cur)
                        self.cur = self.cur.left
            else:
                if self.cur.right is None:
                    self.cur.right = AbstractNode(sym, self.cur)
                elif self.cur.left is None and not self.is_unary(self.cur.sym):
                    self.cur.left = AbstractNode(sym, self.cur)
                else:
                    while self.cur.left is not None or self.is_unary(self.cur.sym):
                        self.cur = self.cur.parent
                    self.cur.left = AbstractNode(sym, self.cur)
    
    def is_unary(self, sym):
        """
        Return True if symbol means unary function, False otherwise
        """
        if sym not in self.function_mapper:
            return False
        return self.function_mapper[sym].is_unary
    
    def is_func(self, sym):
        return sym in self.function_mapper
    
    def is_connect_func(self, sym):
        return sym in self.connects_mapper or sym in self.function_mapper


class AbstractToken():
    def __init__(self, sym, is_value=False, is_func=False,
                    is_oper=False,
                    is_leftb=False, is_rightb=False):
        self.sym = sym
        self.is_value = is_value
        self.is_func = is_func
        self.is_oper = is_oper
        self.is_leftb = is_leftb
        self.is_rightb = is_rightb
    
    def __str__(self):
        return "AbstractToken(sym=" + str(self.sym) +\
                    ", is_func=" + str(self.is_func) +\
                    ", is_value=" + str(self.is_value) +\
                    ", is_oper=" + str(self.is_oper) +\
                    ", is_leftb=" + str(self.is_leftb) +\
                    ", is_rightb=" + str(self.is_rightb) +\
                    ")"
    
    def __repr__(self):
        return self.__str__()


class AbstractNode():
    def __init__(self, sym, parent=None, left=None, right=None):
        self.sym = sym
        self.left = left
        self.right = right
        self.parent = parent
    
    def is_leaf(self):
        return self.left is None and self.right is None
    
    def copy(self):
        return AbstractNode(self.sym, self.parent, self.left, self.right)


class Connective():
    """
    Connectives between nodes. The tree will be built based on the
    precedence of the connective, therefore, it is important to make
    sure the precedence is correct.

    Associativity: 'left' or 'right'

    is_unary: True if it is unary connective, such as '-5' in math

    is_binary: True if it is binary connective, such as '1+1' in math

    call=None: The lambda, it can be understanded as how this connective
    calculate, default is None, which means this connective can not be
    used in calculation
    """
    def __init__(self, symbol, precedence, associativity,
                    is_unary, is_binary, call=None):
        self.symbol = symbol
        self.precedence = precedence
        self.associativity = associativity
        self.is_unary = is_unary
        self.is_binary = is_binary


class Function():
    """
    Function is a function in expression. For example, in  math, max(a,b)
    is a binary function which return the greater number, sin(x) is a function
    that return the trig value.

    is_unary: True if it is unary function, such as sin(0) in math

    is_binary: True if it is a binary function, such as max(1, 2) in math

    call=None: The lambda, it can be understanded as how this function
    calculate, default is None, which means this function can not be
    used in calculation
    """
    def __init__(self, symbol, is_unary, is_binary, call=None):
        self.symbol = symbol
        self.is_unary = is_unary
        self.is_binary = is_binary


class Domain():
    """
    Domain of the expression, for example, in math, the domain is all real
    numbers. In boolean expression, the domain is either True or False.
    getDomain() method provide handy domain such as real numbers.

    d=real: Domain of the expression, default is 'real', which represents
    real numbers. It can also be a list, all elements inside the list will
    represent the domain
    """
    def __init__(self, d='real'):
        self.domain = d
    
    def in_domain(self, v):
        """
        Test if the given value is in the domain, return True if yes, False
        otherwise. Please notice that all values are represented by str format
        """
        if self.domain == 'real':
            return self._is_real(v)
        else:
            return v in self.domain

    def _is_real(self, v):
        "Internal use, return True if given str is value"
        try:
            float(v)
            return True
        except ValueError:
            return False


class AbstractBuilder():
    """
    This class help users to build up the abstract trees
    """
    def __init__(self, associativity,d=Domain()):
        self.function_mapper = {}
        self.domain = d
        self.associativity = associativity
        self.connects_mapper = {}
    
    def add_connect(self, con):
        self.connects_mapper[con.symbol] = con
    
    def add_func(self, func):
        self.function_mapper[func.symbol] = func
    
    def build(self, e):
        """
        Build the Abstract tree by given expression, this method
        should be called when every connectives had been setup
        """
        e = e.replace(" ", "")
        p = self._post(e)
        tree = AbstractTree(self.connects_mapper, self.function_mapper, self.associativity)
        while len(p) > 0:
            tree.add(p.pop())
        return tree
    
    def _post(self, e):
        tokens = self._tokenize(e)
        q = []
        op = []
        index = 0
        while index < len(tokens):
            token = tokens[index]
            if token.is_value:
                q.append(token)
            if token.is_leftb:
                op.append(token)
            elif token.is_oper:
                if len(op) > 0:
                    while len(op) > 0 and (op[-1].is_func or (op[-1].sym != "(" and self._has_precedence(op[-1].sym, token.sym))):
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
    
    def _has_precedence(self, a, b):
        return ((b.associativity == 'right' and
             a.precedence > b.precedence) or
            (b.associativity == 'left' and
             a.precedence >= b.precedence))

    def _tokenize(self, e):
        index = 0
        eindex = 0
        result = []
        starts, ends = self._match_regex(self._func_regex(), e)
        while index < len(e):
            if index in starts:
                result.append(AbstractToken(e[index: ends[eindex]], is_func=True))
                index = ends[eindex]
                eindex += 1
                continue
            t = e[index]
            if self.domain.in_domain(t):
                t, index = self._sub_val(index, e)
                result.append(t)
            elif t == "(":
                result.append(AbstractToken(t, is_leftb=True))
            elif t == ")":
                result.append(AbstractToken(t, is_rightb=True))
            elif self.is_connect(t):
                result.append(AbstractToken(t, is_oper=True))
            index += 1
        return result
    
    def is_connect(self, c):
        return c in self.connects_mapper

    def _sub_val(self, index, e, prev=""):
        d = prev
        while index < len(e) and self.domain.in_domain(e[index]):
            d += e[index]
            index += 1
        index-=1
        return AbstractToken(d, is_value=True), index
    
    def _func_regex(self):
        "Construct regex for special math functions"
        regex = "("
        for f in self.function_mapper:
            if "(" in f:
                index = f.find("(")
                regex += f[:index] + "\\" + f[index:] + "|"
            else:
                regex += f + "|"
        return regex[:-1] + ")"
    
    def _match_regex(self, r, e):
        "Match the functions regex and return a list of start indices and a list of end indices"
        reg = re.compile(r)
        starts, ends = [], []
        for m in reg.finditer(e):
            starts.append(m.start())
            ends.append(m.end())
        return starts, ends


def _extend_tree(a, n, md):
    if n is None:
        return
    if n.left is None and _at_level(n, a) != md:
        n.left = AbstractNode(None)
    if n.right is None and _at_level(n, a) != md:
        n.right = AbstractNode(None)
    _extend_tree(a, n.left, md)
    _extend_tree(a, n.right, md)


def _at_level(n, tree):
    levels = []
    _level_traversal_node(tree.root, 0, levels)
    for index in range(len(levels)):
        if n in levels[index]:
            return index+1
    return -1


def _level_traversal_node(root, level, tlist):
    if root is None:
        return

    if level >= len(tlist):
        l = []
        tlist.append(l)
    tlist[level].append(root)
    _level_traversal_node(root.left, level+1, tlist)
    _level_traversal_node(root.right, level+1, tlist)


def max_depth(n):
    return _max_depth(n.root)

def _max_depth(n):
    if n is None:
        return 0
    left = _max_depth(n.left)
    right = _max_depth(n.right)
    return max(left, right) + 1

def view(tree):
    "View the AST on console"
    a = tree.copy()
    _extend_tree(a, a.root, max_depth(a))
    print(binarytree.build(a.bfs()))


def clone(n):
    """
    Start clonning from the given node and until all the nodes
    are cloned
    """
    if n is None:
        return  
    node = n.copy()
    node.left = clone(n.left)
    node.right = clone(n.right)
    return node


fun = Function("abc", True, False, call=lambda x:x+2)
mul = Connective("*", 2, 'right', False, True, call=lambda x,y:x*y)
builder = AbstractBuilder('right')
builder.add_connect(mul)
builder.add_func(fun)

a = builder.build("abc(2*3)")
view(a)