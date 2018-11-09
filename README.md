# Intro
`pexpr` is a module that contains tools to convert from expressions to Abstract Syntax Tree. After that, it can be evaluated(if possible), transformed(prefix, infix, postfix) or even converted to Latex code to generate the expression PDF.

# AST
To build a AST(Abstract Syntax Tree), the recommend way would be using `build` function in `ast.py`.

For example, `build("1+1")` will be converted to the tree:
```
        +
      /   \
     1     1
```
the same as `build("a+b")`:
```
        +
      /   \
     a     b
```
However, only the first tree can be evaluated since it contains numbers but not variables:
```python
build("1+2").evaluate() # 3.0
```

A tree with parentheses will override the precedence:
```
      3*(1+2)               3*1+2
        *                     +
      /   \                 /   \
     3     +               *     2
         /   \           /   \
        2     1         3     1
```
And the results, of course, are different:
```python
build("3*(1+2)").evaluate()     # 9.0
build("3*1+2").evaluate()       # 5.0
```

# TODO
- [ ] Document
- [ ] Special numbers: e, pi
- [ ] Math functions: sin, cos, tan, asin, acos, atan, ln, log, abs
- [ ] Testing
- [ ] LaTeX code