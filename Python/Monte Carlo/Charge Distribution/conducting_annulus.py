# This simulation models the surface charge density of a conducting annulus
# The technical descriptions of the algorithm can be found in the 
# project description.
# Danny F, Jan 2021


import numpy as np
import matplotlib.pyplot as plt
import scipy.special as sp


pi = np.pi # pi
sigma = 1 #initial uniform charge density
r = 1 # radius
i_r = 0.1  #inner radius
n_rings = 70 # number of annuli
dr = (r - i_r) / n_rings # initial width of each annuli
dq = 0.0001 #charge of each particle
boundaries = list(np.arange(i_r, r + dr / 10, dr)) #endpoints of annuli
charges = [] # number of charges on each annuli
global coq # center of charge of each annuli
coq = []
n_i = 50 # number of iterations
absolute_charges = [] #numerical value of charges on each annuli
x = np.arange(0, r, 0.001) # used for plotting the theoretical model


def assign_abs_charges(): # assigns amount charge on each annuli
    for a in range(1, len(boundaries)):
        r2 = boundaries[a]
        r1 = boundaries[a - 1]
        da = pi * (r2 ** 2 - r1 ** 2)
        absolute_charges.append((da * sigma))
    return absolute_charges
    

def assign_charges(): # assigns the number of charged particles on an annulus
    for a in range(1, len(boundaries)):
        r2 = boundaries[a]
        r1 = boundaries[a - 1]
        da = pi * (r2 ** 2 - r1 ** 2)
        charges.append(int(da * sigma / dq))
    return charges


def center_of_charge(absolute_charges): # determines the center of charge of each annulus
    for b in range(1, n_rings + 1):
        r1 = boundaries[b - 1]
        r2 = boundaries[b]
        q = absolute_charges[b - 1]
        q_m = sigma * (2 / 3) * pi * (r2 ** 3 - r1 ** 3)
        cq = q_m / q
        #cq = (2 * (1 - 3 * b + 3 * b ** 2) * r) / (n_rings * (6 * b - 3))
        coq.append(cq)
    return coq


def point_force(n): # calculates the outward force that the particles on an
    rad = coq[n]    # annulus exert on eachother
    q = absolute_charges[n]
    n_p = charges[n]
    val1 = (q ** 2) / (n_p * (rad ** 2) * (2 ** (3 / 2)))
    val2 = 0
    for i in range(1, n_p):
        val2 = val2 + 1 / (np.sqrt(1 - np.cos(2 * pi * i / n_p)))
    v = val1 * val2
    return v



def ring_force(n, m): #the force between two different annuli
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


def f_prime(a, b): #derivative of ring force with respect to radial position
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


def inner_force(n): # force exerted on annulus due to annuli located within it
    f = 0
    for a in range(0, n):
        f = f + ring_force(n, a)
    return f


def outer_force(n): # force on an annulus due to annuli outside of it
    f = 0
    for a in range(n + 1, n_rings):
        f = f + ring_force(n, a)
    return f



def inner_f_prime(n): # derivative of inner force w/rt radial position
    fp = 0
    for a in range(0, n):
        fp = fp + f_prime(n, a)
    return fp


def outer_f_prime(n): # derivative of outer force w/rt radial position
    fp = 0
    for a in range(n + 1, n_rings):
        fp = fp + f_prime(n, a)
    return fp


def solve(p): # estimates the equilibrium position for a single annulus
    x = coq[p]
    fo = inner_force(p) + outer_force(p) + point_force(p)
    fp = inner_f_prime(p) + outer_f_prime(p)
    sol2 = (fp * x -  fo) / fp
    return sol2


def moving_boundaries(coq): # finds the boundaries of all of the annuli
    mb = [r]
    for a in range(n_rings - 1, 0, -1):
        l = len(mb)
        x = coq[a]
        r2 = mb[0]
        val = 0.25 * (3 * x - 2 * r2 + np.sqrt(3) * np.sqrt(3 * x ** 2 + 4 * x * r2 - 4 * r2 ** 2))
        mb.insert(0, val)
    mb.insert(0, i_r)
    return mb


def calculate_area(mb): # finds the areas of all of the annuli
    areas = []
    for a in range(0, n_rings):
        val = pi * (mb[a + 1] ** 2 - mb[a] ** 2)
        #if (val == 0):
            #val = pi * 0.00001
        areas.append(val)
    return areas


def loop(): # assigns initial conditions and runs each iteration
    absolute_charges = assign_abs_charges()
    charges = assign_charges()
    coq = center_of_charge(absolute_charges)
    print(coq)
    ncoq = coq
    for it in range(0, n_i):
        for a in range(1, n_rings - 1):
            ncoq[a] = solve(a)
        coq = ncoq
        coq[n_rings - 1] = r
    mb = moving_boundaries(coq)
    areas = calculate_area(mb)
    array = np.divide(absolute_charges, areas)
    plt.scatter(coq, array, s=5, c="r", 
                label="Calculated Charge Surface Charge Density")
    plt.plot(x, 1/(2 * np.sqrt(1 - x ** 2)), label="Model for Disk")
    plt.ylim(0, 10)
    plt.xlim(0, r)
    plt.xlabel("Distance from center (m)")
    plt.ylabel("Charge density C * m ^ -2 ")
    plt.legend()
    plt.show()


loop() # the heart of the program!
