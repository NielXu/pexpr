import time
import sys
import os
import ast
import expr


CASES = 1000


def test_basic(n, accpet=0.0, hide=False, show_err=True, show_wrong=True, e_length=3, e_min=-5, e_max=5):
    """Automatically generates math expressions(Basic operators only)
    and evaluate the result using `ast.evaluate()` and `ast.build()`.
    Then compare it with the result given by `eval()` in Python.
    Please notice that errors does not mean the calculations are wrong,
    there are cases such as divided by zero that will lead to calculation
    error (Since expressions are randomly generated, it cannot guarantee that
    this kind of cases will not happen).

    `accept` default is 0.0, indicates the accpetable error range

    `hide` default is False, set it to True will hide the test details,
    only showing the result on console

    `show_err` default is True, set it to False will not show list of errors
    of the tests

    `show_wrong` default is True, set it to False will not show list of wrongs
    of the tests

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
            at = ast.evaluate(ast.build(e))
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
    if show_err:
        print("*LIST OF ERROR:")
        if len(er_list) == 0:
            print("------NONE")
        for e in er_list:
            print("------Expression:", e[0], "Status:", e[1])
    if show_wrong:
        print("*LIST OF WRONG:")
        if len(wr_list) == 0:
            print("------NONE")
        for e in wr_list:
            print("------Expression:", e[0], "Expected:", e[1], "Actual:", e[2], "Error:", e[3])
    print("*Accuracy:", (n-len(wr_list))/n)
    print("*******************************")


# ============ eval does not support special math funcions therefore, cannot compare the result =============

# def test_complex(n, accpet=0.0, hide=False, show_err=True, show_wrong=True, e_length=3, e_min=-5, e_max=5):
#     """Automatically generates math expressions(Basic operators only)
#     and evaluate the result using `ast.evaluate()` and `ast.build()`.
#     Then compare it with the result given by `eval()` in Python.
#     Please notice that errors does not mean the calculations are wrong,
#     there are cases such as divided by zero that will lead to calculation
#     error (Since expressions are randomly generated, it cannot guarantee that
#     this kind of cases will not happen).

#     `accept` default is 0.0, indicates the accpetable error range

#     `hide` default is False, set it to True will hide the test details,
#     only showing the result on console

#     `show_err` default is True, set it to False will not show list of errors
#     of the tests

#     `show_wrong` default is True, set it to False will not show list of wrongs
#     of the tests

#     `e_length` default is 3, controls the length of the random generated
#     expressions, recommend is 3.

#     `e_min` default is -5, controls the lower bound of the numbers in the
#     expressions

#     `e_max` default is 5, controls the upper bound of the numbers in the
#     expressions
#     """
#     wr = 0
#     er = 0
#     er_list = []
#     wr_list = []
#     start = time.time()
#     for _ in range(n):
#         try:
#             e = expr.rand_exp(e_length, e_min, e_max, basic_only=False)
#             if not hide:
#                 print("Expression:", e)
#             at = ast.evaluate(ast.build(e).root)
#             ex = eval(e.replace("^","**"))  # Using the evil
#             err = ex - at
#             if isinstance(at, complex):
#                 er_list.append((e, "Complex number"))
#                 if not hide:
#                     print("Status:", "pass, complex number")
#                 continue
#             if not hide:
#                 print("Expected:", ex)
#                 print("Actual:", at)
#                 print("Error:", err)
#             if abs(err) <= accpet:
#                 if not hide:
#                     print("Status:", "OK")
#             else:
#                 wr += 1
#                 wr_list.append((e, ex, at, err))
#                 if not hide:
#                     print("Status:", "Wrong")
#             if not hide:
#                 print("===============")
#         except OverflowError:
#             er += 1
#             er_list.append((e, "Too large"))
#             if not hide:
#                 print("Status:", "Error, number too large")
#         except ZeroDivisionError:
#             er += 1
#             er_list.append((e, "Divided by 0"))
#             if not hide:
#                 print("Status:", "Error, divided by 0")
#     print("Done. Run time: %s seconds" % (time.time() - start))
#     print("*******************************")
#     print("*TOTAL:", n)
#     print("*WRONG:", wr)
#     print("*ERROR:", er)
#     if show_err:
#         print("*LIST OF ERROR:")
#         if len(er_list) == 0:
#             print("------NONE")
#         for e in er_list:
#             print("------Expression:", e[0], "Status:", e[1])
#     if show_wrong:
#         print("*LIST OF WRONG:")
#         if len(wr_list) == 0:
#             print("------NONE")
#         for e in wr_list:
#             print("------Expression:", e[0], "Expected:", e[1], "Actual:", e[2], "Error:", e[3])
#     print("*Accuracy:", (n-len(wr_list))/n)
#     print("*******************************")


test_basic(CASES, hide=True, show_wrong=False, show_err=False)