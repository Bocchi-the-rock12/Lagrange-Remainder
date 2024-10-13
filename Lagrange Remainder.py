import matplotlib.pyplot as plt
import sympy as sp
from numpy import linspace


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
    # Ensure that x values are numerical by evaluating them
    try:
        x_numeric = [float(val) if isinstance(val, (int, float)) else float(val.evalf()) for val in x]
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

    # Calculate y values for the polynomial and the remainder
    y_values_poly = [float(polynomial.evalf(subs={"x": val})) for val in x_values]
    y_values_rem = [float(sum(r.evalf(subs={"x": val}) for r in remainder)) for val in x_values]
    y_values_function = [float(function.evalf(subs={"x": val})) for val in x_values]

    # Plot limits
    x_min, x_max = min(x_values), max(x_values)
    y_min = min(min(y_values_poly), min(y_values_function))
    y_max = max(max(y_values_poly), max(y_values_function))
    x_padding = (x_max - x_min) * 0.1
    y_padding = (y_max - y_min) * 0.1
    plt.xlim(x_min - x_padding, x_max + x_padding)
    plt.ylim(y_min - y_padding, y_max + y_padding)

    # Graph plot
    plt.plot(x_values, y_values_poly, label="Interpolating Polynomial", color="blue", linestyle="-")
    plt.plot(x_values, y_values_rem, label="Lagrange Remainder", color="red", linestyle="--")
    plt.plot(x_values, y_values_function, label=f"f(x) = {function}", color="black", linestyle="-")

    plt.gcf().canvas.manager.toolbar.zoom()
    plt.legend()
    plt.show()


def main():
    x = sp.symbols("x")
    function_input = input("Insert a function in terms of x (e.g 2x^3+ 3x^2 - 4x + 3): ")
    # Verification for invalid functions
    try:
        function = sp.sympify(function_input)
    except Exception as e:
        print(f"Invalid function! {e}")
        return
    print(f"Function accepted: f(x) = {function}")
    # Gather x, y data from user
    data_points = int(input("Number of points of interpolated function: "))
    x_data = []
    y_data = []
    for i in range(data_points):
        x_var = input(f"x[{i + 1}]: ")
        try:
            x_val = sp.sympify(x_var)
            x_data.append(sp.N(x_val))
            # Calculate the corresponding y value
            y_val = function.subs(x, x_val)
            # Ensure that y is a real number
            y_val_eval = y_val.evalf()
            y_data.append(sp.N(y_val_eval))
        except (ValueError, SyntaxError) as e:
            print(f"Error: {x_var} is not a valid input. {e}")
            continue
    polynomial = polynomial_interpolation(x_data, y_data)
    error_y_data = Lagrange_remainder(function, x_data)
    graph_plot(x_data, y_data, polynomial, error_y_data, function)


main()