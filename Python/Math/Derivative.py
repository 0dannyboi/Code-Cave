import numpy as np
import matplotlib.pyplot as plt


resolution = 8000
x_min = 0
x_max = 10
dx = (x_max - x_min) / resolution


x = np.linspace(x_min - (1 / resolution ), x_max + (1/ resolution), resolution)
y = np.log(x)
d = []


def differentiate():
    for b in range(1, len(y) - 1):
        d.append((y[b + 1] - y[b - 1]) / (2 * dx))
    return d


d = differentiate()
fig, (ax1, ax2) = plt.subplots(1,2)
ax1.plot(x[1:len(x) - 1], y[1:len(x) - 1])
ax2.plot(x[1:len(x) - 1], d)
ax2.set_ylim(0,10)
ax1.title.set_text("f(x) = ln(x)")
ax2.title.set_text("f'(x) = 1/x")
plt.show()
