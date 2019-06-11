"""
This module contains `astree` which can add node onto. Abstract Syntax Tree
only supports basic operators. Use `build` to generate a correct AST by a
math expression.
"""


from queue import Queue
from .excepts import *
from .expr import *
from .lat import *
from .binarytree import build as binarytreebuild
import sys
import os
import textwrap


class node():
    "A node in the AST"
    def __init__(self, sym, parent=None, left=None, right=None):
        self.sym = sym
        self.left = left
        self.parent = parent
        self.right = right
    
    def is_leaf(self):
        """
        Return True if this is a leaf(i.e. with no children),
        False otherwise.
        """
        return self.left is None and self.right is None
    
    def copy(self):
        """
        Make a shallow copy of this node, return a new node that
        have the same members with this node. Please notice that
        the new node's parent and children are not being copied,
        only pointing to them directly.
        """
        return node(self.sym, self.parent, self.left, self.right)


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
    def __init__(self, root=None):
        self.root = root
        self.cur = None
    
    def add(self, sym):
        """
        Adding a new symbol(numbers, operators etc.) into the AST

        @param
        ---
        `sym` Symbol in string
        """
        if self.root is None:
            self.root = node(sym, None)
            self.cur = self.root
        else:
            if is_operator(sym) or is_func(sym):
                if self.cur.right is None:
                    self.cur.right = node(sym, self.cur)
                    self.cur = self.cur.right
                elif self.cur.left is None and not is_unary(self.cur.sym):
                    self.cur.left = node(sym, self.cur)
                    self.cur = self.cur.left
                else:
                    temp = self.cur
                    while self.cur is not None and (self.cur.left is not None or is_unary(self.cur.sym)):
                        self.cur = self.cur.parent
                    if self.cur is None:
                        n = node(sym)
                        n.right = self.root
                        self.root.parent = n
                        self.root = n
                        self.cur = temp
                    else:
                        self.cur.left = node(sym, self.cur)
                        self.cur = self.cur.left
            else:
                if self.cur.right is None:
                    self.cur.right = node(sym, self.cur)
                elif self.cur.left is None and not is_unary(self.cur.sym):
                    self.cur.left = node(sym, self.cur)
                else:
                    while self.cur.left is not None or is_unary(self.cur.sym):
                        self.cur = self.cur.parent
                    self.cur.left = node(sym, self.cur)

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
        li = []
        def travel(node):
            if node is not None:
                travel(node.left)
                li.append(node.sym)
                print(node.sym, end=" ")
                travel(node.right)
        print()
        travel(self.root)
        return li
    
    def preorder(self):
        """
        Travel the tree by `pre-order` way, and return a list that contains
        the symbols.
        """
        li = []
        def travel(node):
            if node is not None:
                print(node.sym, end=" ")
                li.append(node.sym)
                travel(node.left)
                travel(node.right)
        print()
        travel(self.root)
        return li
    
    def postorder(self):
        """
        Travel the tree by `post-order` way, and return a list that contains
        the symbols.
        """
        li = []
        def travel(node):
            if node is not None:
                travel(node.left)
                travel(node.right)
                print(node.sym, end=" ")
                li.append(node.sym)
        print()
        travel(self.root)
        return li
    
    def copy(self):
        """
        Make a deep copy of this AST and return it.
        The new AST will have exactly the same structure with
        this AST, and all nodes are being copied as well. Therefore,
        it is safe to modify the copied AST and it will not affect
        this AST.
        """
        a = astree()
        a.root = _clone(self.root)
        return a


def evaluate(a, vars={}):
    """
    Evaluate the result of the given AST. If the vars
    dict is given, the values for the variables will
    be substituted when evaluating the result. If there
    are variables in the tree but no corresponding values
    are provided, it will raise `EvaluationException`.

    @param
    ---
    `a` The AST

    `vars={}` The variables dict, for example: `{"x": 10, "y": 12}` 
    """
    def _eval(node):
        if node is None:
            return 0
        if is_unary(node.sym):
            return function_mapper[node.sym](_eval(node.right))
        if is_number(node.sym):
            return float(node.sym)
        if is_special_number(node.sym):
            return special_number[node.sym]
        if is_var(node.sym):
            if node.sym in vars:
                return float(vars[node.sym])
            else:
                raise EvaluationException("Undefined variable: " + node.sym)
        left = _eval(node.left)
        right = _eval(node.right)
        return symbols[node.sym](left, right)
    return _eval(a.root)


def build(e):
    """
    Build and return a `astree` by given INFIX expression. Infix
    expression means expressions that placed operators between
    numbers, such as `1+1`.

    This function not only support math expressions, but
    also support expressions in general, for example `a+b`.
    However, only math expressions can be evaluated.

    @param
    ---
    `e` The expression in string format
    """
    e = e.replace(" ", "")
    p = postfix(e)
    ast = astree()
    while len(p) > 0:
        ast.add(p.pop())
    return ast


def level_order(ast):
    """
    Travel the given AST level by level and return a list
    that contains list of nodes at each level, start from
    root to the most bottom.

    @param
    ---
    `ast` The AST
    """
    levels = []
    _level_traversal(ast.root, 0, levels)
    return levels


def max_depth(ast):
    """
    Get the max depth of a given AST.

    @param
    ---
    `ast` The AST
    """
    return _max_depth(ast.root)


def view(ast):
    """
    View the AST on console.

    @param
    ---
    `ast` The AST
    """
    a = ast.copy()
    _extend_tree(a, a.root, max_depth(a))
    print(binarytreebuild(a.bfs()))


def subtrees(a, roots=[], max_depth=None):
    """
    Get all possible subtrees from root, left and then right. It ends if
    max depth is given and the depth is reached, otherwise, it will return all
    subtrees. If roots are given, only the trees that with roots that are inside
    the given list will be returned.

    @param
    ---
    `a` The AST

    `roots=[]` The roots that being used to match subtrees

    `max_depth=None` The maximum depth that this function should reach
    """
    li = []
    _subtree(a.root, 0, 100, li)
    result = []
    for tree in li:
        if len(roots) == 0 or tree.root.sym in roots:
            result.append(tree)
    return result


def _level_traversal(root, level, tlist):
    "Travel the tree level by level and save each level in list"
    if root is None:
        return

    if level >= len(tlist):
        l = []
        tlist.append(l)
    tlist[level].append(root.sym)
    _level_traversal(root.left, level+1, tlist)
    _level_traversal(root.right, level+1, tlist)


def _subtree(root, depth, max_depth, li):
    "Recursion of finding subtrees"
    if root is None or root.is_leaf() or depth == max_depth:
        return
    li.append(astree(root))
    _subtree(root.left, depth+1, max_depth, li)
    _subtree(root.right, depth+1, max_depth, li)


def _max_depth(n):
    "Recursion of finding max depth of the tree"
    if n is None:
        return 0
    left = _max_depth(n.left)
    right = _max_depth(n.right)
    return max(left, right) + 1


def _level_traversal_node(root, level, tlist):
    "Recursion of doing level order traversal"
    if root is None:
        return

    if level >= len(tlist):
        l = []
        tlist.append(l)
    tlist[level].append(root)
    _level_traversal_node(root.left, level+1, tlist)
    _level_traversal_node(root.right, level+1, tlist)


def _clone(n):
    "Recursion that clone the AST, return the root node"
    if n is None:
        return  
    node = n.copy()
    node.left = _clone(n.left)
    node.right = _clone(n.right)
    return node


def _extend_tree(a, n, md):
    "Recursion that extends the AST in order to print on console"
    if n is None:
        return
    if n.left is None and _at_level(n, a) != md:
        n.left = node(None)
    if n.right is None and _at_level(n, a) != md:
        n.right = node(None)
    _extend_tree(a, n.left, md)
    _extend_tree(a, n.right, md)


def _at_level(n, tree):
    "Recursion that tells which level the node is at"
    levels = []
    _level_traversal_node(tree.root, 0, levels)
    for index in range(len(levels)):
        if n in levels[index]:
            return index+1
    return -1


def main():
    "Entrance of the script"
    import argparse
    parser = argparse.ArgumentParser(prog="ast",
        description="Generate and view Abstract-Syntax-Tree",
        epilog=textwrap.dedent('''additional information:
                Please notice that quotations are required since some
                of the symbols are special characters in command line.
                And brackets are also necessary in most of the cases
                since minus sign is a special character as well.'''))
    parser.add_argument("eval",
        help="Evaluate the given expression and display the result if possible",
        metavar="expr",
        nargs="?")
    parser.add_argument("-v", "--view",
        help="View the abstract-syntax-tree that generated by the given expression",
        required=False,
        action="store_true")
    parser.add_argument("-p", "--pdf",
        help="Generate and open the PDF of the math expression",
        required=False,
        action="store_true")
    args = parser.parse_args()
    if args.eval is not None:
        exp = args.eval
        a = build(exp)
        if is_evaluable(exp):
            print(evaluate(a))
        else:
            print("Expression not evaluable: "+exp)
        if args.view:
            view(a)
        if args.pdf:
            temp_path = os.path.dirname(os.path.realpath(__file__))
            quickgen(a, temp_path, "temp", op=True)


if __name__ == "__main__":
    main()
