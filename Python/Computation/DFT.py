import numpy as np
import matplotlib.pyplot as plt


def get_file(): #opens file
    f = open("sin8x.csv","r")
    file = f.read()
    return file


def extract_data(file): #extracts values
    end = []
    start = []
    numb = []
    for x in range(0, len(file)):
        if (file[x] == "\n"):
            end.append(x)
    end.append(len(file))
    start.append(1)
    for x in range(0, len(end) - 1):
        start.append(end[x] + 1)
    for x in range(0, len(end)):
        numb.append(float(file[start[x]:end[x]]))
    return numb


def fourier(numb): #computes discrete fourier transform
    pi = np.pi
    l = (len(numb) * 0.01) / pi
    n = len(numb)
    f = []
    for y in range(0, n):
        count = 0 + 0j
        for k in range(0, n):
            comp = np.exp(((-1j * l * pi) / n) * y * k)
            count = count + numb[k] * comp
        f.append(np.abs(count))
    return f
            
    
def generate_bar_graph(f): #bar graph to visualize peaks of frequencies
    plt.xlim(0, 10)
    plt.bar(np.arange(0, len(f), step=1), f)
    plt.show()


def main():
    file = get_file()
    numb = extract_data(file)
    f = fourier(numb)
    print(f)
    generate_bar_graph(f)


main()
