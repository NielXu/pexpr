"""
This module contains `astree` which can add node onto. Abstract Syntax Tree
only supports basic operators. Use `build` to generate a correct AST by a
math expression.
"""


from queue import Queue
from expr import is_symbol, is_digit, postfix
import sys


class node():
    "A node in the AST"
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
        "Evaluate the result of the AST, and return the value as `float`."
        return evaluate(self.root)
    
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
    
    def inorder(self):
        """
        Travel the tree by `in-order` way, and return a list that contains
        the symbols.
        """
        def travel(node):
            if node is not None:
                travel(node.left)
                print(node.sym, end=" ")
                travel(node.right)
        print()
        travel(self.root)
    
    def preorder(self):
        """
        Travel the tree by `pre-order` way, and return a list that contains
        the symbols.
        """
        def travel(node):
            if node is not None:
                print(node.sym, end=" ")
                travel(node.left)
                travel(node.right)
        print()
        travel(self.root)
    
    def postorder(self):
        """
        Travel the tree by `post-order` way, and return a list that contains
        the symbols.
        """
        def travel(node):
            if node is not None:
                travel(node.left)
                travel(node.right)
                print(node.sym, end=" ")
        print()
        travel(self.root)


def evaluate(node):
    """
    Evaluate the result of a AST by a given node. Please
    notice that not all AST can be evaluated. Only the
    tree that contains valid numbers or symbols can be
    evaluated.
    """
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


def build(e):
    """
    Build and return a `astree` by given INFIX expression. Infix
    expression means expressions that placed operators between
    numbers, such as `1+1`.

    This function not only support math expressions, but
    also support expressions in general, for example `a+b`.
    However, only math expressions can be evaluated.

    Support operators:
    ------
    Basic:
        + - * / ^ ( )
    Functions:
        sin, cos, tan, ln, log, abs
    Special numbers:
        pi, e
    """
    e = e.replace(" ", "")
    p = postfix(e)
    ast = astree()
    while len(p) > 0:
        ast.add(p.pop())
    return ast


def main():
    if len(sys.argv) > 0:
        for e in sys.argv[1:]:
            print(build(e).evaluate())
            print(build(e).bfs())


if __name__ == '__main__':
    main()