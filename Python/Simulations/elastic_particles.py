import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import random
from random import choices
from itertools import combinations
import matplotlib

pi = np.pi
n = 75 # number of particles
v1 = 10 # initial velocity of each particle
w = 10 # length/width of the box
part_rad = 0.05 # particle radius
time_scale = 0.001 # how much time passes every interval
c = 2 / (v1**2)
cycles = 1000 # number of iterations
t = time_scale * cycles # total time passed

# configure graph
fig, ax = plt.subplots()
x_data, y_data = [], []
ln, = plt.plot([], [], 'ro', markersize=0.5, markerfacecolor='w',
               markeredgewidth=.5, markeredgecolor='k')

# initialize plot
def init():
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    return ln,

# euclidean distance formula
def distance(x1, x2, y1, y2):
    x = x1 - x2
    y = y1 - y2
    d = np.sqrt(x**2 + y**2)
    return d

# assign positons
p = []
for x in range(0, n):
    p.append([random.uniform(part_rad, w - part_rad), random.uniform(part_rad,
             w - part_rad), x])
# assign velocities
v = []
for x in range(0, n):
    a = 2 * pi * random.random()
    v.append([v1 * np.cos(a), v1 * np.sin(a)])

# updates each frame
def update(frame):
    x_data = []
    y_data = []
    for particle in range(0, n):
        p[particle][0] = p[particle][0] + v[particle][0] * time_scale
        p[particle][1] = p[particle][1] + v[particle][1] * time_scale
        if (p[particle][0] > (w - part_rad)):
            p[particle][0] = 2 * w - p[particle][0] - part_rad
            v[particle][0] = - v[particle][0]
        if (p[particle][0] < part_rad):
            p[particle][0] = part_rad - p[particle][0]
            v[particle][0] = - v[particle][0]
        if (p[particle][1] > (w - part_rad)):
            p[particle][1] = 2 * w - p[particle][1] - part_rad
            v[particle][1] = - v[particle][1]
        if (p[particle][1] < part_rad):
            p[particle][1] = part_rad - p[particle][1]
            v[particle][1] = - v[particle][1]
    l = list(combinations(p, 2))
    for x in range(0, len(l)):
        x1 = l[x][0][0]
        x2 = l[x][1][0]
        y1 = l[x][0][1]
        y2 = l[x][1][1]
        index1 = l[x][0][2]
        index2 = l[x][1][2]
        v1 = v[index1]
        v2 = v[index2]
        r_o = distance(x1, x2, y1, y2)
        if (r_o <= 2 * part_rad):
            a = x1
            b = v1[0]
            c = y1
            d = v1[1]
            e = x2
            f = v2[0]
            g = y2
            h = v2[1]
            k = 4 * part_rad ** 2
            t = (2 * a * b + 2 * c * d - 2 * b * e - 2 * a * f + 2 * e * f - 2 *
                 d * g - 2 * c * h + 2 * g * h + np.sqrt((-2 * a * b - 2 * c *
                 d + 2 * b * e + 2 * a * f - 2 * e * f + 2 * d * g + 2 * c * h -
                 2 * g * h)**2 - 4 * (b**2 + d**2 - 2 * b * f + f**2 - 2 * d *
                 h + h**2) *  (a**2 + c**2 - 2 * a * e + e**2 - 2 * c * g + g**
                 2 - k))) / (2 * (b**2 + d**2 - 2 * b * f + f**2 - 2 * d * h +
                 h**2))
            x1_precoll = x1 - v1[0] * t
            x2_precoll = x2 - v2[0] * t
            y1_precoll = y1 - v1[1] * t
            y2_precoll = y2 - v2[1] * t
            r1 = [x1_precoll, y1_precoll]
            r2 = [x2_precoll, y2_precoll]
            dv1 = np.subtract(v1, v2)
            dr1 = np.subtract(r1, r2)
            dr2 = np.subtract(r2, r1)
            dv2 = np.subtract(v2, v1)
            c1 = np.dot(dv1, dr1) / (np.linalg.norm(dr1)**2)
            c2 = np.dot(dv2, dr2) / (np.linalg.norm(dr2)**2)
            reduced_dr1 = np.multiply(c1, dr1)
            reduced_dr2 = np.multiply(c2, dr2)
            v1f = np.subtract(v1, reduced_dr1)
            v2f = np.subtract(v2, reduced_dr2)
            t_post_collision = time_scale - t
            x1f = v1f[0] * t_post_collision + x1_precoll
            y1f = v1f[1] * t_post_collision + y1_precoll
            x2f = v2f[0] * t_post_collision + x2_precoll
            y2f = v2f[1] * t_post_collision + y2_precoll
            p[index1] = [x1f, y1f, index1]
            p[index2] = [x2f, y2f, index2]
            v[index1] = [v1f[0], v1f[1]]
            v[index2] = [v2f[0], v2f[1]]
    for x in range(0, n):
        x_data.append(p[x][0])
        y_data.append(p[x][1])
    ln.set_data(x_data, y_data)
    return ln,
# animates frame
ani = FuncAnimation(fig, update, frames=np.linspace(0, 1000, 1000),
                    init_func=init, blit=True)

#shows graph
plt.show()
