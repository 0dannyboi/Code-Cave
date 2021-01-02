import numpy as np
import matplotlib.pyplot as plt


pi = np.pi
r = 1
sigma = 100
n_rings = 30
n_points = 100
a = pi * r ** 2
q_tot = sigma * a
dr = r / (n_rings - 1)
d_theta = 2 * (pi / (n_points - 1))
#n_t = 300
n_t = 50
dt = 0.00006


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
    q_0 = q_dist[0]
    for b in range(0, n_t): # run through each time cycle
        f = 0
        for c in range(1, n_rings - 2, 1): # calculates the force on the test particle in each ring
            f_r = 0
            rad = c * dr
            r_p = [0, -rad]
            q_test = q_dist[c] / n_points
            for d in range(0, n_rings): # goes through every other ring to calculate force
                r_ring = d * dr
                q_q = q_dist[d] / n_points
                for e in range(0, n_points): # goes through each point on ring
                    theta = e * d_theta + phi
                    r_q = [r_ring * np.cos(theta), r_ring * np.sin(theta)]
                    delta_r = np.subtract(r_p, r_q).tolist()
                    norm = np.linalg.norm(delta_r)
                    force = (q_test * q_q) * (1 / norm ** 3) * delta_r[1]
                    f_r = f_r + force
            f = f_r
            dp = np.multiply(f, dt)
            dq = q_dist[c] * (dp / dr)
            #print(q_dist[c])
            #print(dq)
            q_dist[c] = q_dist[c] + dq
            #print(c)
            q_dist[c + 1] = q_dist[c + 1] - dq
    return q_dist
# fix algorithm because charges are "flying off edge"

def calculate_charge_desnity(q_dist):
    charge_density = []
    for m in range(0, n_rings):
        radi = m * dr
        da = pi * (2 * radi * dr + dr ** 2)
        charge_density.append(q_dist[m] / da)
    return charge_density
    

q_dist = loop()
#print(len(q_dist[1::]))
x = np.arange(dr, r + dr / 2, dr)
cd = calculate_charge_desnity(q_dist)
plt.scatter(x, cd[1::])
plt.plot(x, cd[1::])
plt.show()
