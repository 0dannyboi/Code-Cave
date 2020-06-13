  
# This program looks at the daily COVD cases.
# It displays the cases in a simple plot vs number of days since first caese.
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import urllib.request


def get_data():
    # Access NY Times's GitHub with US cases.
    url = \
        "https://raw.githubusercontent.com/nytimes/covid-19-data/master/us.csv"
    site = urllib.request.urlopen(url).read().decode()
    site = site[18::]
    return site


def find_commas(site):
    # Find the index of the commas in the CSV.
    comma = []
    for x in range(0, len(site)):
        if (site[x] == ","):
            comma.append(x)
    return comma


def get_cases(site, comma):
    # Extract the total daily cases from the CSV.
    cases = []
    for x in range(0, len(comma)):
        if (x % 2 == 0):
            case = site[comma[x] + 1:comma[x + 1]]
            cases.append(case)
    return cases


def new_cases(cases):
    # Convert the total daily cases to new cases.
    new_cases = [1]
    for x in range(1, len(cases)):
        number = int(cases[x]) - int(cases[x - 1])
        new_cases.append(number)
    return new_cases


def display(new_cases, number):
    # Outputs a plot of  the adjusted new cases vs days since initial infection
    y = new_cases
    x = np.arange(0, len(new_cases))
    fig = plt.figure()
    plt.plot(x, y)
    plt.title("Daily New Cases of COVID-19 in US Since Jan 21")
    fig.suptitle("(Naively) Predicted to approach zero around " +
                 str(round(number, 1)) + " days")
    plt.xlabel("Days since Jan 21 2020")
    plt.ylabel("New Cases of COVID-19")


def get_minima_days(new):
    # Finds the x values of local minima.
    minima_days = []
    for x in range(1, len(new) - 1):
        if (new[x - 1] > new[x] and new[x + 1] > new[x]):
            minima_days.append(x)
    return minima_days


def get_minima(new, minima_days):
    # Finds the values of the local minima.
    minima = []
    for x in range(0, len(minima_days)):
        minima.append(new[minima_days[x]])
    return minima


def find_y_prime(minima, minima_days):
    # Finds the ratio of the minima to an initial amound at "peak."
    A = 25354
    y_prime = []
    for x in range(9, len(minima)):
        value = np.log(minima[x] / A)
        y_prime.append(value)
    return y_prime


def find_x_prime(minima_days):
    # Sets 0 to be the minima closest to day of peak cases.
    x_prime = []
    for x in range(9, len(minima_days)):
        value = minima_days[x] - 89
        x_prime.append(value)
    return x_prime


def regress(x_prime, y_prime):
    # Calculates the linear regression of the logarithm.
    from scipy import stats
    slope, intercept, r_value, p_value, std_err = \
        stats.linregress(x_prime, y_prime)
    return slope


def find_zeros(slope):
    # Calculates date of "zero" in model.
    day = (-1 / (slope)) + 5
    number = day + 89 + 21
    print(number)
    return number


def main():
    data = get_data()
    comma = find_commas(data)
    cases = get_cases(data, comma)
    new = new_cases(cases)
    minima_days = get_minima_days(new)
    minima = get_minima(new, minima_days)
    y_prime = find_y_prime(minima, minima_days)
    x_prime = find_x_prime(minima_days)
    slope = regress(x_prime, y_prime)
    number = find_zeros(slope)
    display(new, number)

main()
