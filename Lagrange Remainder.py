import matplotlib.pyplot as plt
from sympy import symbols, simplify
from numpy import linspace


def l_func(x_values, k, n):
   l = 1
   x = symbols("x")
   for i in range(n + 1):
       if i != k:
           # L parameters
           l *= (x - x_values[i]) / (x_values[k] - x_values[i])
   return l


def polynomial_interpolation(x_var, y, z):
   p = 0
   for k in range(z + 1):
       # Lagrange Polynomial
       p += y[k] * l_func(x_var, k, z)
   return simplify(p)


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
main()
