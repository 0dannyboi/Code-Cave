import numpy as np
import matplotlib.pyplot as plt


n = 400


def a(x, y):
    a_val = 1 / ((n - (2 + x + y)) ** 2)
    return a_val


def b(x, y):
    if (y == x + 1):
        b_val = 0
    else:
        v = y - (x + 1)
        b_val = np.sign(v) * 1 / (v ** 2)
    return b_val


def generate_matrix():
    matrix = []
    line_2 = [1] * (int(n / 2))
    for x in range(0, int(n / 2) - 1):
        line = []
        for y in range(0, int(n/2)):
            a_val = a(x, y)
            b_val = b(x, y)
            val = a_val + b_val
            line.append(val)
        matrix.append(line)
    matrix.append(line_2)
    return matrix


def generate_solution(matrix):
    soln = [0] * int((n / 2) - 1)
    soln.append(0.5)
    x = np.linalg.solve(matrix, soln)
    return x


def main():
    matrix = generate_matrix()
    sol = generate_solution(matrix)
    field = (n - 1) * sol
    field[0] = 2 * field[0]
    field = np.append(field, (np.flip(field)))
    x = np.arange(0, 1 + (1 / (n - 1)), 1 / (n-1))
    plt.plot(x, field)


main()
