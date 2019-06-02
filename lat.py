import ast
import subprocess
import os
from expr import is_number, is_letter, is_func, is_unary


header = r'''\documentclass{standalone}
\begin{document}
'''


footer = r'''\end{document}'''


latex_mapper = {
    "/" : lambda x,y : "\\frac{"+x+"}{"+y+"}"
}


special_mapper = {
    "pi" : lambda x : "\\pi"
}


def genlat(a):
    """
    Convert the given AST to latex code, the result will
    return as string.

    @param
    ---
    `a` The AST
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


def gentex(lat, loc, name):
    """
    Convert a snippet of the latex code to a complete latex code by
    adding header and footer. And save the file as .tex format to the
    given location with given name. The generated file will be `{name}.tex`
    If the file with the same name already exists, it will be overrided.

    @param
    ---
    `lat` The latex code

    `loc` Location of the file will be saved to, must be a directory

    `name` The tex file name, extention does not require
    """
    code = header + lat + footer
    with open(os.path.join(loc, name+".tex"), "w+") as f:
        f.write(code)


def genpdf(source, des, rm=False):
    """
    Compile the .tex file from given source location 
    and save the result to the given destination.
    The result will be a folder contains the compiled
    result, if rm is enabled, all other files will be
    removed after compilation except for .pdf file.
    
    @param
    ---
    `source` The source file(.tex)

    `des` The directory that the folder will be saved to

    `rm=False` Remove files except for .pdf after compilation
    """
    command = ["pdflatex", "-output-directory", des, source]
    subprocess.call(command)
    if rm:
        from os import listdir, remove
        from os.path import isfile, join, splitext, basename
        name = splitext(basename(source))[0]
        for f in listdir(des):
            if isfile(join(des, f)):
                fname, ext = splitext(f)
                if fname == name:
                    if ext == '.aux' or ext == '.log' or ext == ".tex":
                        remove(os.path.join(des, f))


def quickgen(a, des, name, op=False):
    """
    Quickly generate the PDF of the given AST and save
    to the destination with the given name. The destination
    must be a folder. The file name will be `{name}.pdf`.
    This function is the combination of: `genlat`, `gentex`
    and `genpdf`.

    @param
    ---
    `a` The AST

    `des` The pdf file that will be saved to, must be a directory

    `name` The name of the pdf file

    `op=False` Open the file after compilation, use system default PDF viewer
    """
    temp_lat = genlat(a)
    gentex(temp_lat, des, name)
    genpdf(os.path.join(des, name+'.tex'), des, rm=True)
    if op:
        os.startfile(os.path.join(des, name+'.pdf'))
