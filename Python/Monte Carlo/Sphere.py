# This program uses the Monte Carlo method to calculate pi
# by comparing the volumes of the unit sphere and the corresponding
# cube to which the sphere is inscribed.
import numpy as np
import random as r
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


def get_iteration():
    print("How many iterations would you like to perform?")
    n = int(input())
    return n


def assign_array(n):
    array = []
    for a in range(0, n):
        value = r.uniform(-1, 1)
        array.append(value)
    return array


def generate_points(n):
    points = []
    points.append(assign_array(n))
    points.append(assign_array(n))
    points.append(assign_array(n))
    return points


class Point:
    def __init__(self, points, n):
        self.points = points
        self.x = points[0][n]
        self.y = points[1][n]
        self.z = points[2][n]
        self.distance = np.sqrt((self.x**2) + (self.y**2) + (self.z**2))


def inside_sphere(points):
    inside = []
    outside = []
    total = []
    for a in range(0, len(points[0])):
        point_value = Point(points, a)
        if (point_value.distance <= 1):
            inside.append([point_value.x, point_value.y, point_value.z])
        else:
            outside.append([point_value.x, point_value.y, point_value.z])
    total.append(inside)
    total.append(outside)
    return total


def calculate_pi(total):
    inside = len(total[0])
    outside = len(total[1])
    pi = 6 * (inside / (inside + outside))
    print(pi)


def show_points(total):
    in_x = []
    in_y = []
    in_z = []
    out_x = []
    out_z = []
    out_y = []
    out_z = []
    inside = total[0]
    outside = total[1]
    for a in range(0, len(inside)):
        in_x.append(inside[a][0])
        in_y.append(inside[a][1])
        in_z.append(inside[a][2])
    for b in range(0, len(outside)):
        out_x.append(outside[b][0])
        out_y.append(outside[b][1])
        out_z.append(outside[b][2])
    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")
    ax.scatter(in_x, in_y, in_z, c="r", marker="o")
    ax.scatter(out_x, out_y, out_z, c="b", marker="o")
    plt.show()


def main():
    n = get_iteration()
    points = generate_points(n)
    total = inside_sphere(points)
    calculate_pi(total)
    show_points(total)


main()
