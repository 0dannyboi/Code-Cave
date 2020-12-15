import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
import matplotlib.animation as animation

l = 10 # length of rod
h = 2 # width of rod

t1 = 40.0 # initial internal temp
t2 = 10.0 # final temperature of rod, external temperature

low = min(t1, t2) # find low and high for color map
high = max(t1, t2)

number_of_frames = 100 # how many frames in animation
n = 20 # number of sums of Fourier series
divx = 80 # number of divisions ("pixels") in for x
pi = np.pi
divy = int(divx * ((h / l))) # number of divisions ("pixels") of y 

alpha = 0.86 ** 2 # thermal conductivity (this is aluminum's)


def u(x, y, dt): # calculate temperature based on location and time
    x1 = x * l / divx
    y1 = y * h / divy
    tot = t2
    for m in range(1, (n + 1)):
        tot_2 = 0
        for k in range(1, (n + 1)):
            x_const = k * pi / l
            y_const = m * pi / h
            expo = np.exp(-1 * alpha * (x_const ** 2 + y_const ** 2) * dt)
            b = np.sin(x_const * x1) * np.sin(y_const * y1) * expo
            tot_2 = tot_2 + 4 * ((t1 - t2) / ((k * m) * pi ** 2)) *
            (1 - (- 1) ** m) * (1 - (-1) ** k) * b
        tot = tot + tot_2
    return tot


def generate_data(dt): # array of temperature values for a certain time, dt
    table = []
    for y in range(0, divy):
        x_row = []
        for x in range(0, divx):
            val = u(x, y, dt)
            if (val > 37):
                val = 37
            x_row.append(val)
        table.append(x_row)
    return table


def clean_data(table): # fixes temperature anomolies on the boundary
    tab = []
    for p in range(1, len(table)):
        tab.append(table[p][1::])
    return tab


fig, ax = plt.subplots() # initializing the animation frames
tab = generate_data(0)
tab = clean_data(tab)
img = ax.imshow(tab, cmap='hot', interpolation='nearest', vmin=low, vmax=high,
                extent=[0, l, 0, h])
plt.title("Temperature (" + u"\u00b0" + "C) in Bar at t = " + str(0) + "s")
plt.xlabel("x position (cm)")
plt.ylabel("y position (cm)")
plt.xticks(np.arange(0, l + 1))
plt.colorbar(img)


def update(i): # creates each frame
    table = generate_data(float(i / number_of_frames))
    tab = clean_data(table)
    img = img = ax.imshow(tab, cmap='hot', interpolation='nearest', vmin=low,
                          vmax=high, extent=[0, l, 0, h])
    plt.title("Temperature (" + u"\u00b0" + "C) in Bar at t = " +
              str(i / number_of_frames) + "s")
    return fig,

ani = animation.FuncAnimation(fig, update, frames=number_of_frames, interval=20) # runs the animation
ani.save("heatbar4.mp4", fps=24) # configurable options to save animation
