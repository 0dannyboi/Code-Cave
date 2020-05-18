import random
import numpy as np
from matplotlib import pyplot as plt


def get_number():
    print("Please enter the number of iterations you'd like to perform.")
    number = int(input())
    return number


def generate_arrays(number):
    x_values = []
    y_values = []
    for x in range(0, number):
        a = random.random()
        x_values.append(a)
    for x in range(0, number):
        b = random.random()
        y_values.append(b)
    points = []
    for x in range(0, number):
        points.append([x_values[x], y_values[x]])
    return points


def calculate_pi(points):
    inside = []
    outside = []
    for x in range(0, len(points)):
        if (np.sqrt((points[x][0])**2 + (points[x][1])**2) <= 1):
            inside.append(points[x])
        else:
            outside.append(points[x])
    inner = len(inside)
    outter = len(outside)
    total = inner + outter
    pi = 4 * (inner / total)
    return pi


def x_array(points):
    x_values = []
    for x in range(0, len(points)):
        ex = points[x][0]
        x_values.append(ex)
    return x_values


def y_array(points):
    y_values = []
    for x in range(0, len(points)):
        why = points[x][1]
        y_values.append(why)
    return y_values


def generate_graph(x_values, y_values, pi):
    x_in = []
    y_in = []
    x_out = []
    y_out = []
    for x in range(0, len(x_values)):
        if (np.sqrt((x_values[x])**2 + (y_values[x]**2)) <= 1):
            x_in.append(x_values[x])
            y_in.append(y_values[x])
        else:
            x_out.append(x_values[x])
            y_out.append(y_values[x])
    plt.scatter(x_in, y_in, color="r")
    plt.scatter(x_out, y_out, color="g")
    plt.xlabel = ("x")
    plt.ylabel("y")
    plt.show


def main():
    number = get_number()
    points = generate_arrays(number)
    pi = calculate_pi(points)
    x_values = x_array(points)
    y_values = y_array(points)
    print(pi)
    print(len(x_values))
    generate_graph(x_values, y_values, pi)

main()
