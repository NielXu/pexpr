"""
This module contains the abstract level of the syntax tree,
it is real abstract syntax tree
"""


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

    is_unary_func: True if it is a unary special function, such as 'sin(x)'

    is_binary_func: True if it is a binary special function, such as 'max(1, 2)'
    """
    def __init__(self, symbol, precedence, associativity,
                    is_unary, is_binary,
                    is_unary_func, is_binary_func):
        self.symbol = symbol
        self.precedence = precedence
        self.associativity = associativity
        self.is_unary = is_unary
        self.is_binary = is_binary
        self.is_unary_func = is_unary_func
        self.is_binary_func = is_binary_func
