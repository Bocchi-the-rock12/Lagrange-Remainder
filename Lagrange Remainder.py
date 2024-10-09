import matplotlib.pyplot as plt
import sympy as sp
from numpy import linspace
import random

def l_func(x_values, k, degree):
   l = 1
   x = sp.symbols("x")
   for i in range(degree + 1):
       if i != k:
           # L parameters
           l *= (x - x_values[i]) / (x_values[k] - x_values[i])
   return l


def polynomial_interpolation(x_var, y, degree):
   p = 0
   for k in range(degree + 1):
       # Lagrange Polynomial
       p += y[k] * l_func(x_var, k, degree)
   return sp.simplify(p)


def Lagrange_error_formula(x_var, y_var, degree):
    x = sp.symbols("x")
    error_formula = 1
    for b in range(degree + 1):
        derivative = sp.diff(polynomial_interpolation(x_var, y_var, degree), x, degree)
        error_formula *= derivative * random.choice(x_var)
    error_formula / sp.factorial(degree - 1)
    print(error_formula)
    return error_formula


def main():
    x_data_set = []
    y_data_set = []
    print("Lagrange Polynomial Remainder Error")
    n = int(input("> "))
    for z in range(n + 1):
        # Get x, y data from user
        xi, yi = map(int, input("(x, y): ").split(","))
        x_data_set.append(xi)
        y_data_set.append(yi)
    Lagrange_error_formula(x_data_set, y_data_set, n)

main()
