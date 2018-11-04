class node():
    def __init__(self, sym, parent, left=None, right=None):
        self.sym = sym
        self.parent = parent
        self.left = left
        self.right = right


class astree():
    def __init__(self):
        self.root = None
        self.cur = None
    
    def add(self, sym):
        if self.root is None:
            self.root = node(sym, None)
            self.cur = self.root
        else:
            if self.symbol(sym):
                if self.symbol(self.root.sym) and self.order(sym, self.root.sym) == 1:
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
    
    def evaluate(self):
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
            else:
                return left / right
        return eva(self.root)
    
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
        return sym in ["+", "-", "*", "/"]
    
    def order(self, sym1, sym2):
        """
        Return 1 if symbol_1 > symbol_2
        Return 0 if symbol_1 = symbol_2
        Return -1 if synbol_1 < symbol_2
        """
        t = {"+":1, "-":1, "*":2, "/":2}
        return t[sym1] - t[sym2]

s = "1*2/3"
a = astree()
for i in s:
    a.add(i)

print(a.evaluate())