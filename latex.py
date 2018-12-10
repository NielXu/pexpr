import ast
from expr import is_number, is_letter, is_func, is_unary


latex_mapper = {
    "/" : lambda x,y : "\\frac{"+x+"}{"+y+"}"
}


special_mapper = {
    "pi" : lambda x : "\\pi"
}


def tolatex(a):
    def _eval(n):
        if n is None:
            return ""
        if n.sym in special_mapper:
            return special_mapper[n.sym](n.sym)
        if is_number(n.sym) or (is_letter(n.sym) and not is_func(n.sym)):
            return n.sym
        left = _eval(n.left)
        right = _eval(n.right)
        if n.sym in latex_mapper:
            return latex_mapper[n.sym](left, right)
        elif is_unary(n.sym):
            return n.sym + "(" + _eval(n.right) + ")"
        else:
            return "{"+left + n.sym + right+"}"
    return _eval(a.root)


a = ast.build("2+pi*sin(x+2)/cos(x^(y+1))")
print(tolatex(a))