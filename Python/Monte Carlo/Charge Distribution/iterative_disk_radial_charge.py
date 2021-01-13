# For this porgram we are taking a new approach
# We will define the charges in the annulus and position them on a ring
# at the center of charge and the number of points there will determine the 
# the charge.

import numpy as np
import matplotlib.pyplot as plt
import scipy.special as sp
#from scipy.optimize import fsolve


pi = np.pi
sigma = 1
r = 1
n_rings = 90 # number of annuli
dr = r / n_rings
dq = 0.0001
boundaries = list(np.arange(0, r + dr / 2, dr))
charges = []
coq = []
n_i = 60
absolute_charges = []


#remember that in n_rings and charges, that the lists go [0, 1, ... n - 1]
# for indices


def assign_abs_charges():
    for a in range(1, len(boundaries)):
        r2 = boundaries[a]
        r1 = boundaries[a - 1]
        da = pi * (r2 ** 2 - r1 ** 2)
        absolute_charges.append((da * sigma))
    return absolute_charges
    


def assign_charges():
    for a in range(1, len(boundaries)):
        r2 = boundaries[a]
        r1 = boundaries[a - 1]
        da = pi * (r2 ** 2 - r1 ** 2)
        #print(da)
        charges.append(int(da * sigma / dq))
    return charges


def center_of_charge():
    for b in range(1, n_rings + 1):
        cq = (2 * (1 - 3 * b + 3 * b ** 2) * r) / (n_rings * (6 * b - 3))
        coq.append(cq)
        #coq = list(np.arange((dr / 2), r + dr / 3, dr))
    #for b in range(1, n_rings + 1):
        #coq.append(b * dr)
    return coq


def point_force(n):
    num = charges[n]
    if (num == 0):
        f = 0
    else:
        rad = coq[n]
        d_theta = 2 * pi / num
        rp = [rad, 0]
        f = 0
        for a in range(1, num):
            rq = [rad * np.cos(a * d_theta), rad * np.sin(a * d_theta)]
            delta = list(np.subtract(rp, rq))
            norm = np.linalg.norm(delta)
            f = f + (dq ** 2) * delta[0] / (norm ** 3)
    return f


def ring_force(n, m):
    if (n == m):
        val = 0
    else:
        qp = charges[n] * dq
        qq = charges[m] * dq
        rp = coq[n]
        rq = coq[m]
        s = rp - rq
        a = rp + rq
        four = -4 * (rp * rq) / s ** 2
        val = (1 / (2 * pi)) * qq * qp * (2 / (rp * np.abs(s) * a)) * (s * sp.ellipe(four) + a * \
              sp.ellipk(four))
    return val


def f_prime(a, b):
    if (a == b):
        val = 0
    else:
        rp = coq[a]
        rq = coq[b]
        qp = charges[a] * dq
        qq = charges[b] * dq
        s = rp - rq
        a = rp + rq
        three = 3 * rp ** 2 - rq ** 2
        four = -4 * (rp * rq) / s ** 2
        val = (1 / (2 * pi)) * - 2 * (three * sp.ellipe(four) + (a ** 2) * \
              sp.ellipk(four)) / ((rp ** 2) * np.abs(s) * (a ** 2))
        val = val * qq * qp
    return val


def inner_force(n):
    f = 0
    for a in range(0, n):
        f = f + ring_force(n, a)
    return f


def inner_f_prime(n):
    fp = 0
    for a in range(0, n):
        fp = fp + f_prime(n, a)
    return fp


def outer_f_prime(n):
    fp = 0
    for a in range(n + 1, n_rings):
        fp = fp + f_prime(n, a)
    return fp


def outer_force(n):
    f = 0
    for a in range(n + 1, n_rings):
        f = f + ring_force(n, a)
    return f


def f_double_prime(a, b):
    rp = coq[a]
    rq = coq[b]
    qp = charges[a] * dq
    qq = charges[b] * dq
    s = rp - rq
    a = rp + rq
    eleven = 11 * (rp ** 4) - 5 * (rp ** 2) * (rq ** 2) + 2 * (rq ** 4)
    two = rp ** 2 - 2 * rq ** 2
    four = -4 * (rp * rq) / s ** 2
    val = (1 / pi) * (eleven * sp.ellipe(four) + (a ** 2) * two * sp.ellipk(four)) \
          / ((rp ** 3) * s * np.abs(s) * (a ** 3))
    val = val * qq * qp
    return val


def inner_f_dprime(n):
    fdp = 0
    for a in range(0, n):
        fdp = fdp + f_double_prime(n, a)
    return fdp


def outer_f_dprime(n):
    fdp = 0
    for a in range(n + 1, n_rings):
        fdp = fdp + f_double_prime(n, a)
    return fdp


def solve(p):
    x = coq[p]
    fo = inner_force(p) + outer_force(p) + point_force(p)
    fp = inner_f_prime(p) + outer_f_prime(p)
    sol2 = (fp * x -  fo) / fp
    return sol2
    

def surface_density(boundaries, charges, coq):
    density = []
    for a in range(0, n_rings):
        r2 = boundaries[a + 1]
        r1 = boundaries[a]
        area = pi * ((r2 ** 2) - (r1 ** 2))
        tot = 0
        for b in range(0, n_rings):
            if (r1 <= coq[b] and coq[b] < r2):
                tot = tot + dq * charges[b]
        density.append(tot / area)
    return density
        


def loop():
    absolute_charges = assign_abs_charges()
    charges = assign_charges()
    coq = center_of_charge()
    c1 = coq.copy()
    ncoq = coq
    for it in range(0, n_i):
        for a in range(1, n_rings - 1):
            ncoq[a] = solve(a)
        coq = ncoq
        coq[n_rings - 1] = r
    d = surface_density(boundaries, absolute_charges, coq)
    plt.plot(coq, absolute_charges)
    plt.show()


loop()

