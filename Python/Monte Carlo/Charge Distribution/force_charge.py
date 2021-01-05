import matplotlib.pyplot as plt
import numpy as np
import scipy.special as sp


sigma = 1 # surface charge density
r = 1
pi = np.pi
n_rings = 120 # number of radius divisions
dr = 1 / (n_rings - 1) #differential of r
dt = 0.001
nt = 10
d = 0.3
p = np.arange(0, r + 0.5 * dr, dr) # positions
n_points = 50
q_tot = sigma * pi * r ** 2


# goal is to plot the force vs radius in disk


def equi_sigma(rad):
    s = q_tot / (4 * pi * r * np.sqrt(r ** 2 - rad ** 2))
    return s


def charge_at_radius():
    dq = []
    for x in range(0, n_rings):
        rad = dr * x
        if (x != (n_rings - 1)):
            q = equi_sigma(rad) * 2 * pi * rad * dr
        else:
            tot_q = sum(dq)
            q = q_tot - tot_q
            print(q)
        dq.append(q)
    return dq


def point_charge(n):
    f = 0
    q = dq[n] / n_points
    dtheta = 2 * pi / (n_points - 1)
    ang = np.arange(0, 2 * pi + 0.5 * dtheta, dtheta)
    r_point = [0, p[n]]
    for a in range(1, len(ang)): #start at one!
        r = np.subtract(r_point, [p[n] * np.cos(ang[a]), p[n] * np.sin(ang[a])]).tolist()
        norm = np.linalg.norm(r)
        f = f + n_points * (q ** 2) * r[1] / (norm ** 3)
    return f
        

def force_ring(n,m):
    qp = dq[n]
    qq = dq[m]
    rp = p[n]
    rq = p[m]
    d = rp ** 2 + rq ** 2
    a = rp + rq
    sq_a = (a) ** 2
    s = (rp - rq)
    four = 4 * (rp * rq) / sq_a
    val = 1 * (1 / (rp * s *  np.sqrt(d))) * np.sqrt(d / sq_a) * \
            (a * sp.ellipeinc(pi / 4, four) + a * \
             sp.ellipeinc(3 * pi / 4, four) + s * \
             (sp.ellipkinc(pi / 4, four) + \
             sp.ellipkinc(3 * pi / 4, four)))
    val = qp * qq * val
    return val


def calculate_force():
    force = []
    for n in range(1, n_rings):
        f = 0
        for m in range(0, n_rings):
            if (n == m):
                f = f + point_charge(n)
            else:
                f = f + force_ring(n,m)
        force.append(f)
    return force
    
dq = charge_at_radius()
force = calculate_force()
x = np.arange(dr, r + dr/2, dr)
#print(force)
plt.plot(x[:-10], force[:-10])
plt.show()
