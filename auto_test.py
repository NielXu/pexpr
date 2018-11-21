import expr
import ast
import time


def test(n, accpet=0.0, hide=False, e_length=3, e_min=-5, e_max=5):
    """Automatically generates math expressions(Basic operators only)
    and evaluate the result using `ast.evaluate()` and `ast.build()`.
    Then compare it with the result given by `eval()` in Python.

    `accept` default is 0.0, indicates the accpetable error range

    `hide` default is False, set it to True will hide the test details,
    only showing the result on console

    `e_length` default is 3, controls the length of the random generated
    expressions, recommend is 3.

    `e_min` default is -5, controls the lower bound of the numbers in the
    expressions

    `e_max` default is 5, controls the upper bound of the numbers in the
    expressions
    """
    wr = 0
    er = 0
    er_list = []
    wr_list = []
    start = time.time()
    for _ in range(n):
        try:
            e = expr.rand_exp(e_length, e_min, e_max)
            if not hide:
                print("Expression:", e)
            at = ast.evaluate(ast.build(e).root)
            ex = eval(e.replace("^","**"))  # Using the evil
            err = ex - at
            if isinstance(at, complex):
                er_list.append((e, "Complex number"))
                if not hide:
                    print("Status:", "pass, complex number")
                continue
            if not hide:
                print("Expected:", ex)
                print("Actual:", at)
                print("Error:", err)
            if abs(err) <= accpet:
                if not hide:
                    print("Status:", "OK")
            else:
                wr += 1
                wr_list.append((e, ex, at, err))
                if not hide:
                    print("Status:", "Wrong")
            if not hide:
                print("===============")
        except OverflowError:
            er += 1
            er_list.append((e, "Too large"))
            if not hide:
                print("Status:", "Error, number too large")
        except ZeroDivisionError:
            er += 1
            er_list.append((e, "Divided by 0"))
            if not hide:
                print("Status:", "Error, divided by 0")
    print("Done. Run time: %s seconds" % (time.time() - start))
    print("*******************************")
    print("*TOTAL:", n)
    print("*WRONG:", wr)
    print("*ERROR:", er)
    print("*LIST OF ERROR:")
    if len(er_list) == 0:
        print("------NONE")
    for e in er_list:
        print("------Expression:", e[0], "Status:", e[1])
    print("*LIST OF WRONG:")
    if len(wr_list) == 0:
        print("------NONE")
    for e in wr_list:
        print("------Expression:", e[0], "Expected:", e[1], "Actual:", e[2], "Error:", e[3])
    print("*Accuracy:", (n-len(wr_list))/n)
    print("*******************************")


test(1000, hide=True)