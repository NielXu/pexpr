# Intro
`pexpr` is a module that contains tools to convert from expressions to Abstract Syntax Tree. After that, it can be evaluated(if possible), transformed(prefix, infix, postfix) or even converted to Latex code to generate the expression PDF.

# CLI
To quickly calculate a math expression just type in command line:
```
python ast.py "1*2+max(4,5)/3"
```
and the result will be:
```
3.666666666666667
```
To view the tree, enable the view feature:
```
python ast.py "1*2+max(4,5)/3" -v
```
The result will be following:
```
3.666666666666667

       _____(+)_______________
      /                       \
   _(*)_                ______(/)_
  /     \              /          \
(1)     (2)        _(max)_        (3)
                  /       \
                (4)       (5)
```
<b>Note:</b> quotation is required since there are special characters in some cases

For more information, enter:
```
python ast.py -h
```

# Abstract-Syntax-Tree
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

# Tree viewer
To view the tree that created by the `build` function, simply use `view()` function in `ast.py`:
```python
a = build("2^(1+2)*1+3/4+10*2*3")
view(a)
```
the output will be displayed on the console:
```
                               _____________(+)______________
                              /                              \
                       _____(+)_____                    _____(*)_
                      /             \                  /         \
       _____________(*)_           _(/)_           __(*)_        (3)
      /                 \         /     \         /      \
   _(^)_____            (1)     (3)     (4)     (10)     (2)
  /         \
(2)        _(+)_
          /     \
        (1)     (2)
```

# Operations
Here are some symbols and special numbers that AST supports:

### Binary Operations
| Symbol        | Operation           | Example  |
| :-----------: |:-------------|:-----:|
| +     | Addition | 1+1 |
| -     | Subtraction      |  1-2 |
| *     | Multiplication  |    1*1 |
| /     | Division | 1/1 |
| ^     | Power | 1^2 |
| max     | Max value of two numbers | max(1,2) |
| min     | Min value of two numbers | min(1,2) |
|log      | Logarithm given base and exponent| log(2, 1)|

### Unary Operations
| Symbol        | Operation           | Example  |
| :-----------: |:-------------|:-----:|
| sin     | Trig function, sin | sin(0) |
| cos     | Trig function, cos      |  cos(0) |
| tan     | Trig function, tan  |    tan(1) |
| asin     | Inverse trig function, arcsin | asin(1) |
| acos     | Inverse trig function, arccos | acos(1) |
| atan     | Inverse trig function, arctan | atan(1) |
| lg      | Logarithm with base 10 | lg(1) |
| ln      | Logarithm with base e| ln(1)|
| sqrt      | Square root| sqrt(0)|
| abs      | Absolute value| abs(-1)|
| ~      | Negation| ~-5|

Note: Some negative sign(-) will be converted to negation(~) when building AST

### Special Numbers
| Symbol        |
| :-----------: |
| e     |
| pi    |



# TODO
- [x] Document
- [x] Special numbers: e, pi
- [x] Math functions: sin, cos, tan, asin, acos, atan, ln, log, abs
- [ ] Testing
- [ ] LaTeX code
- [ ] Error handling