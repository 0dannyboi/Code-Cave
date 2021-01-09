import numpy as np
import matplotlib.pyplot as plt
import scipy.special as sp
import time


rp = 5
rq = 10
q_p = 1
q_q = 3
pi = np.pi


def point_forces(n):
    dq = q_q / n
    dqp = q_p / n
    d_theta = 2 * pi / n
    f_t = 0
    p = d_theta / 2
    p_r = [rp, 0]
    f = 0
    for a in range(1, n):
        q_r = [rq * round(np.cos(a * d_theta),6), rq * round(np.sin(a * d_theta), 6)]
        rad = list(np.subtract(p_r, q_r))
        norm = np.linalg.norm(rad)
        f = f + dq * dqp * rad[0] / (norm ** 3)
    f = f * n
    return f


def ring_force():
    s = rp - rq
    a = rp + rq
    four = -4 * (rp * rq) / s ** 2
    val = (1 / (2 * pi)) * q_q * q_p * (2 / (rp * np.abs(s) * a)) * (s * sp.ellipe(four) + a * \
          sp.ellipk(four))
    return val


def main():
    x = list(np.arange(50, 500, 1))
    point_n = []
    #t1_point = time.time()
    for a in (x):
        point_n.append(point_forces(a))
    #t2_point = time.time()
    rf = ring_force()
    #t2_ring = time.time()
    #point_t = t2_point - t1_point
    #ring_t = t2_ring - t2_point
    #print("point " + str(point_t))
    #print("ring " + str(ring_t))
    y2 = list(np.add(rf, np.zeros(len(x))))
    plt.plot(x, point_n)
    plt.plot(x, y2)
    plt.show()

main()
