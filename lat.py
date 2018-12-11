import ast
import subprocess
from expr import is_number, is_letter, is_func, is_unary


header = r'''\documentclass{article}
\begin{document}
'''


footer = r'''\end{document}'''


latex_mapper = {
    "/" : lambda x,y : "\\frac{"+x+"}{"+y+"}"
}


special_mapper = {
    "pi" : lambda x : "\\pi"
}


def tolat(a):
    """Convert a AST to latex format code, so that a pdf of the
    given formula can be generated.
    """
    def _eval(n):
        if n is None:
            return ''
        if n.sym in special_mapper:
            return special_mapper[n.sym](n.sym)
        if is_number(n.sym) or (is_letter(n.sym) and not is_func(n.sym)):
            return n.sym
        left = _eval(n.left)
        right = _eval(n.right)
        if n.sym in latex_mapper:
            return latex_mapper[n.sym](left, right)
        elif is_unary(n.sym):
            return n.sym + '(' + _eval(n.right) + ')'
        else:
            return '{'+left + n.sym + right+'}'
    return '$'+_eval(a.root)+'$'


def totex(lat, loc):
    """Convert a snippet of the latex code to a complete latex code by
    adding header and footer. And save the file as .tex format to the
    given location, or create new file if it does not exist. If the
    header and footer were not added, the compile phase will fail.
    """
    code = header + lat + footer
    with open(loc, "w+") as f:
        f.write(code)


def topdf(source, des, rm=False):
    """Compile the .tex file from given source location 
    and save the result to the given file destination.
    If rm is enabled, all files except for the pdf file
    will be removed after the compilation.
    """
    command = ["pdflatex", "-output-directory", des, source]
    subprocess.call(command)
    if rm:
        from os import listdir, remove
        from os.path import isfile, join, splitext, basename
        name = splitext(basename(source))[0]
        print("FILENAME", name)
        for f in listdir(des):
            if isfile(join(des, f)):
                fname, ext = splitext(f)
                print("NAME", fname, "EXTENSION", ext)
                if fname == name and ext != ".pdf":
                    remove(des+"\\"+f)


# a = ast.build("2+pi*sin(x+2)/cos(x^(y+1))")
# latex = tolat(a)
# totex(latex, "F:\\github\\ast\\example.tex")
# topdf("F:\\github\\ast\\example.tex", "F:\\github\\ast\\pdf", True)