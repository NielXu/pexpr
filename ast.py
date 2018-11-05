"""
This module contains `astree` which can add node onto. Abstract Syntax Tree
only supports basic operators. Use `build` to generate a correct AST by a
math expression.
"""


from queue import Queue


class node():
    def __init__(self, sym, parent, left=None, right=None):
        self.sym = sym
        self.parent = parent
        self.left = left
        self.right = right


class astree():
    """
    Abstract Syntax Tree that can add node onto. Please
    notice that this AST does not support any operators except for:
    +, -, *, /, ^. To generate a tree with more options, please
    use `build` method.
    """
    def __init__(self):
        self.root = None
        self.cur = None
    
    def add(self, sym):
        if type(sym) == node:
            self._add_node(sym)
        elif self.root is None:
            self.root = node(sym, None)
            self.cur = self.root
        else:
            if self.symbol(sym):
                if self.symbol(self.root.sym) and self.precedence(sym, self.root.sym):
                    n = node(sym, self.cur.parent)
                    self.cur.parent.right = n
                    n.left = self.cur
                else:
                    n = node(sym, None)
                    n.left = self.root
                    self.root = n
            else:
                if self.root.right is None:
                    self.root.right = node(sym, self.root)
                    self.cur = self.root.right
                else:
                    temp = self.root
                    while temp.right is not None:
                        temp = temp.right
                    temp.right = node(sym, temp)
                    self.cur = temp.right
    
    def _add_node(self, n):
        if self.root is None:
            self.root = n
            self.cur = self.root
        else:
            if self.root.right is None:
                self.root.right = n
                self.cur = self.root.right
            else:
                temp = self.root
                while temp.right is not None:
                    temp = temp.right
                temp.right = n
                self.cur = temp.right
    
    def evaluate(self):
        """
        Evaluate the result of the AST, and return the value as `float`.
        """
        def eva(node):
            if node is None:
                return 0
            if not self.symbol(node.sym):
                return float(node.sym)
            left = eva(node.left)
            right = eva(node.right)
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
        return eva(self.root)
    
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
    
    def precedence(self, sym1, sym2):
        """
        Return True if symbol 1 has high precedence than symbol2,
        False otherwise
        """
        t = {"+":1,
             "-":1,
             "*":2,
             "/":2,
             "^":3}
        return t[sym1] > t[sym2]


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


def build(e):
    e = e.replace(" ","")
    ops, val = [], []
    digit = "0123456789"
    symbol = "+-*/^"
    index = 0
    while index < len(e):
        token = e[index]
        if token in digit:
            s = ""
            while index < len(e) and e[index] in digit:
                s += e[index]
                index += 1
            val.append(s)
            index -= 1
        elif token == "(":
            ops.append(token)
        elif token == ")":
            while ops[-1] != "(":
                val.append(operate(ops.pop(), val.pop(), val.pop()))
            ops.pop()
        elif token in symbol:
            while len(ops) != 0 and ops[-1] != "(":
                val.append(operate(ops.pop(), val.pop(), val.pop()))
            ops.append(token)
        index += 1
    while len(ops) > 0:
        val.append(operate(ops.pop(), val.pop(), val.pop()))
    return val.pop()

def operate(op, n1, n2):
        a = astree()
        a.add(n2)
        a.add(op)
        a.add(n1)
        return a.root

# a = astree()
# a.add("2")
# a.add("*")

# b = astree()
# b.add("1")
# b.add("+")
# b.add("3")

# a.add(b.root)
# a.add("*")
# a.add("3")
# a.add("+")
# a.add("2")
# print(a.evaluate())

t = build("  2   * (3 +     1) *(10    -15)")
a = astree()
a.add(t)
print(a.evaluate())