"""
This module contains `astree` which can add node onto. Abstract Syntax Tree
only supports basic operators. Use `build` to generate a correct AST by a
math expression.
"""


from queue import Queue
import collections
import sys


class node():
    def __init__(self, sym, parent=None, left=None, right=None):
        self.sym = sym
        self.left = left
        self.parent = parent
        self.right = right


class astree():
    """
    Abstract Syntax Tree is a tree representation of an expression.
    Please notice that this tree only accpets basic operators +,-,*,/
    and the nodes will be inserted in POSTFIX order.

    If one wants to construct AST with infix expression, please convert
    it using `postfix` method first, and then pop elements from the stack
    in order to add them into the tree. Or use `build` directly, which
    supports more functions such as parathensis and so on.
    
    After constructing the tree completely, one can use `preorder`, `inorder`
    and `postorder` to convert the expression to prefix, infix and postfix format.
    """
    def __init__(self):
        self.root = None
        self.cur = None
    
    def add(self, sym):
        if self.root is None:
            self.root = node(sym, None)
            self.cur = self.root
        else:
            if is_symbol(sym):
                if self.cur.right is None:
                    self.cur.right = node(sym, self.cur)
                    self.cur = self.cur.right
                elif self.cur.left is None:
                    self.cur.left = node(sym, self.cur)
                    self.cur = self.cur.left
                else:
                    while self.cur.left is not None:
                        self.cur = self.cur.parent
                    self.cur.left = node(sym, self.cur)
                    self.cur = self.cur.left
            else:
                if self.cur.right is None:
                    self.cur.right = node(sym, self.cur)
                elif self.cur.left is None:
                    self.cur.left = node(sym, self.cur)
                else:
                    while self.cur.left is not None:
                        self.cur = self.cur.parent
                    self.cur.left = node(sym, self.cur)

    
    def evaluate(self):
        """
        Evaluate the result of the AST, and return the value as `float`.
        """
        return evaluate(self.root)
    
    def bfs(self):
        q = Queue()
        q.put(self.root)
        s = ""
        while q.qsize() > 0:
            node = q.get()
            s += node.sym
            if node.left is not None:
                q.put(node.left)
            if node.right is not None:
                q.put(node.right)
        print(s)
    
    def inorder(self):
        def travel(node):
            if node is not None:
                travel(node.left)
                print(node.sym, end=" ")
                travel(node.right)
        print()
        travel(self.root)
    
    def preorder(self):
        def travel(node):
            if node is not None:
                print(node.sym, end=" ")
                travel(node.left)
                travel(node.right)
        print()
        travel(self.root)
    
    def postorder(self):
        def travel(node):
            if node is not None:
                travel(node.left)
                travel(node.right)
                print(node.sym, end=" ")
        print()
        travel(self.root)
    
    def symbol(self, sym):
        return sym in ["+", "-", "*", "/", "^"]


Op = collections.namedtuple('Op', [
    'precedence',
    'associativity'])

RIGHT, LEFT = 0,1

OPS = {
    '^': Op(precedence=4, associativity=RIGHT),
    '*': Op(precedence=3, associativity=LEFT),
    '/': Op(precedence=3, associativity=LEFT),
    '+': Op(precedence=2, associativity=LEFT),
    '-': Op(precedence=2, associativity=LEFT)}

def has_precedence(a, b):
    return ((OPS[b].associativity == RIGHT and
             OPS[a].precedence > OPS[b].precedence) or
            (OPS[b].associativity == LEFT and
             OPS[a].precedence >= OPS[b].precedence))


def evaluate(node):
    if node is None:
        return 0
    if not is_symbol(node.sym):
        return float(node.sym)
    left = evaluate(node.left)
    right = evaluate(node.right)
    # check which operation to apply 
    if node.sym == '+': 
        return left + right  
    elif node.sym == '-': 
        return left - right 
    elif node.sym == '*': 
        return left * right
    elif node.sym == "^":
        return left ** right 
    else:
        return left / right


def is_symbol(s):
    return s in "+-*/^"


def is_digit(s):
    return s in "1234567890"


def postfix(e):
    "Convert infix expression to postfix expression"
    index = 0
    q = []
    op = []
    while index < len(e):
        token = e[index]
        print(token)
        if is_digit(token):
            d = ""
            while index < len(e) and is_digit(e[index]):
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


def build(e):
    """Build a `astree` by given INFIX expression. Infix
    expression means expressions that placed operators
    between numbers, such as `1+1`.
    """
    e = e.replace(" ", "")
    p = postfix(e)
    ast = astree()
    while len(p) > 0:
        ast.add(p.pop())
    return ast


e = "3^(1+2)/4+3*(6^(4-1))+99"
print(build(e).evaluate())