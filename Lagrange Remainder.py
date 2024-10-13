import matplotlib.pyplot as plt
import sympy as sp
from numpy import linspace
import math
from fractions import Fraction


def l_func(x_values, k, x):
    l = 1
    degree = len(x_values) - 1
    for i in range(degree + 1):
        if i != k:
            l *= (x - x_values[i]) / (x_values[k] - x_values[i])
    return l


def polynomial_interpolation(x_values, y_values):
    x = sp.symbols("x")
    p = 0
    degree = len(x_values) - 1
    for k in range(degree + 1):
        p += y_values[k] * l_func(x_values, k, x)
    return p


def Lagrange_remainder(function, x_var):
    x = sp.symbols("x")
    degree = len(x_var) - 1
    fact = sp.factorial(degree + 1)
    error_values = []
    derivative = sp.diff(function, x, degree + 1)
    for m in range(degree + 1):
        product = 1
        for i in range(degree + 1):
            if i != m:
                product *= (x - x_var[i])
        error = (derivative / fact) * product
        error_values.append(error)
    return error_values


def graph_plot(x, y_data, polynomial, remainder, function):
    # Convert x to a number
    try:
        x_numeric = []
        for val in x:
            if isinstance(val, sp.Basic):
                x_numeric.append(float(val.evalf()))
            else:
                x_numeric.append(float(val))
    except Exception as e:
        print(f"Error converting x values to float: {e}")
        return

    # Window set
    plt.figure("Polynomial Interpolation", figsize=(11, 8))
    plt.grid()
    plt.xlabel("X-axis", fontsize=12)
    plt.ylabel("Y-axis", fontsize=12)
    plt.title("Polynomial Interpolation with Lagrange Remainder", fontsize=20)
    plt.axhline(0, color="black", linewidth=2, ls="-")
    plt.axvline(0, color="black", linewidth=2, ls="-")

    # x values for plotting
    x_values = linspace(min(x_numeric), max(x_numeric), 750)

    # Plot the original function
    y_original = [float(function.subs(sp.symbols("x"), val).evalf()) for val in x_values]
    plt.plot(x_values, y_original, label=f"f(x) = {function}", color="black", linewidth=2)

    # Plot the interpolated polynomial
    y_polynomial = [float(polynomial.subs(sp.symbols("x"), val).evalf()) for val in x_values]
    plt.plot(x_values, y_polynomial, label="Interpolated Polynomial", color="blue", linewidth=2)

    # Plot the Lagrange remainder (sum of remainder terms)
    y_remainder = [float(sum([r.subs(sp.symbols("x"), val).evalf() for r in remainder])) for val in x_values]
    plt.plot(x_values, y_remainder, label="Lagrange Remainder", color="red", linewidth=2)

    plt.scatter(x_numeric, [float(val.evalf()) for val in y_data], label="Data Points", color="red", marker="o")
    plt.legend(loc="best")
    plt.show()


def main():
    x = sp.symbols("x")
    function_input = input("Insert a function in terms of x (e.g 2x^3 + 3x^2 - 4x + 3): ")
    try:
        function = sp.sympify(function_input)
    except Exception as e:
        print(f"Invalid function! {e}")
        return
    print(f"Function accepted: f(x) = {function}")

    # Gather x, y data from user
    data_points = int(input("Number of points of interpolated polynomial: "))
    x_data = []
    y_data = []

    for i in range(data_points):
        x_var = input(f"x[{i + 1}]: ")
        # Allows input to be irrational values such as e or pi and fractions
        try:
            if "/" in x_var:
                x_value = float(Fraction(x_var))
            else:
                allowed_names = {"e": math.e, "pi": math.pi, "Fraction": Fraction}
                x_value = eval(x_var, {"__builtins__": None}, allowed_names)

            # Calculate y values
            x_sym = sp.sympify(x_value)
            y_value = function.subs(x, x_sym).evalf()

            x_data.append(x_sym)
            y_data.append(y_value)
        # Evaluate errors
        except (ValueError, SyntaxError) as e:
            print(f"Error: {x_var} is not a valid input. {e}")
            return

    polynomial = polynomial_interpolation(x_data, y_data)
    error_y_data = Lagrange_remainder(function, x_data)
    graph_plot(x_data, y_data, polynomial, error_y_data, function)


main()