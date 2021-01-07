import numpy as np
import matplotlib.pyplot as plt
import scipy.special as sp


# ths program shows that the force of a ring of charge on itself varies
# with the inverse of the square of the increase in the radius of the ring
# the ring is approximated by a a number of discrete, equally charged points
r = 1 #radius
pi = np.pi
n_points = 2000 #number of points
d_theta = 2 * pi / (n_points - 1) 
theta = np.arange(0, 2 * pi + d_theta / 2, d_theta)
n_r = 200 # number of radii
d_r = 0.001
r_s = np.arange(0, n_r * d_r, d_r).tolist()[1:]
dq = 20 / n_points # charge on each point (charge / n_points)


def calc_force():
    force = []
    for b in (r_s):
        f = 0
        r_p = [b, 0]
        for d in (theta):
            r_q = [b * np.cos(d), b * np.sin(d)]
            if (r_q == r_p):
                f = f + 0
            else:
                rad = np.subtract(r_p, r_q)
                norm = np.linalg.norm(rad)
                f = f + n_points * (dq ** 2) * rad[0] / (norm ** 3)
        force.append(f)
    return force


a1 = calc_force()
r_s_2 = np.multiply(r_s, r_s).tolist()
val = np.multiply(r_s_2, a1).tolist()
plt.plot(r_s, val)
plt.show()

