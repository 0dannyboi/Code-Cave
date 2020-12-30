import numpy as np
import matplotlib.pyplot as plt


pi = np.pi
r = 1
sigma = 100
n_rings = 50
n_points = 10
a = pi * r ** 2
q_tot = sigma * a
dr = r / (n_rings - 1)
d_theta = 2 * (pi / (n_points - 1))
#n_t = 300
n_t = 1
dt = 0.000001


if (n_points % 4 == 0):
    phi = d_theta / 2
else:
    phi = 0


def initialize():
    q_dist = []
    for x in range(0, n_rings):
        q_dist.append(sigma * 2 * pi * (x * dr) * dr)
    return q_dist


def loop():
    q_dist = initialize()
    for b in range(0, n_t): # run through each time cycle
        f = []
        for c in range(1, n_rings): # calculates the force on the test particle in each ring
            f_r = 0
            rad = c * dr
            r_p = [0, -rad]
            q_test = q_dist[c] / n_points
            for  d in range(0, n_rings): # goes through every other ring to calculate force
                r_ring = d * dr
                q_q = q_dist[d] / n_points
                for e in range(0, n_points): # goes through each point on ring
                    r_q = [r_ring * np.cos(e * d_theta + phi), r_ring * np.sin(e
                           * d_theta + phi)]
                    delta_r = np.subtract(r_p, r_q).tolist()
                    norm = np.linalg.norm(delta_r)
                    force = (q_test * q_q) * (1 / norm ** 3) * delta_r[1]
                    f_r = f_r + force
            f.append(f_r)
    return f
x = np.arange(r / (n_rings), r, (r / (n_rings)))
f = loop()
print(f)
plt.plot(x, f)
plt.show()
print(len(x))
