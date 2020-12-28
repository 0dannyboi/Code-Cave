import numpy as np
import matplotlib.pyplot as plt


x_i = [1, 5]
y_i = [1, 1]
relation = [0.5, 0.5]
r_x = relation[0]
r_y = relation[1]
n_i = 10


def get_difference_vector(x,y,p):
    v = [x[p+1] - x[p], y[p+1] - y[p]]
    return v


def get_relation_point_vector(v):
    r_p_v = [r_x * v[0], r_y * v[1]]
    return r_p_v


def get_perpendicular_vector(r_p_v):
    perp_v = [-r_p_v[1], r_p_v[0]]
    return perp_v


def run_iterations():
    for n in range(0, n_i):
        if (n == 0):
            x = x_i
            y = y_i
        else:
            new_x = []
            new_y = []
            for m in range(0, len(x) - 1):
                v = (get_difference_vector(x, y, m))
                r_p_v = get_relation_point_vector(v)
                perp_v = get_perpendicular_vector(r_p_v)
                x_val = x[m] + perp_v[0] + r_p_v[0]
                y_val = y[m] + perp_v[1] + r_p_v[1]
                new_x.append(x_val)
                new_y.append(y_val)
            for a in range(0, len(new_x)):
                    x.insert(1 + 2 * a, new_x[a])
                    y.insert(1 + 2 * a, new_y[a])
    return x,y


a = run_iterations()
plt.plot(a[0], a[1])
plt.show() 
