import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

from models.BaseModel import db
from models.CoronaCases import CoronaCases
from models.DeathsGermany import DeathsGermany


def main():
    total_corona_deaths_germany()

def total_corona_deaths_germany():
    query = CoronaCases\
        .select(CoronaCases.deaths, CoronaCases.cases, CoronaCases.date_reported, DeathsGermany.deaths)\
        .join(DeathsGermany, attr="total", on=CoronaCases.date_reported == DeathsGermany.date)\
        .where(CoronaCases.geo_id == "DE")\
        .where(DeathsGermany.age_group_start == 0)\
        .where(DeathsGermany.age_group_end == 150)\
        .where(DeathsGermany.date >= "2020-02-01")\
        .order_by(CoronaCases.date_reported)

    time = []
    corona_cases = []
    corona_deaths = []
    total_deaths = []
    for item in query:
        time.append(item.date_reported)
        corona_cases.append(item.cases)
        corona_deaths.append(item.deaths)
        total_deaths.append(item.total.deaths)

    t = []
    x = []
    y = []
    z = []
    window = 2
    stride = 1
    for i in range(0, len(time) - (window-1), stride):
        td = total_deaths
        cd = corona_deaths
        t.append(time[i+window-1])
        x.append((sum(td[i:i+window])) / window)
        y.append((sum(cd[i:i+window])) / window)
        z.append(x[i] - y[i])


    plt.suptitle('Daily Deaths in Germany 2020\n(Sources: EU Open Data Portal, Statistisches Bundesamt)')

    locator = mdates.AutoDateLocator()
    formatter = mdates.ConciseDateFormatter(locator)
    plt.gca().xaxis.set_major_locator(locator)
    plt.gca().xaxis.set_major_formatter(formatter)


    plt.plot(t, x, "-b", label="total deaths")
    plt.plot(t, y, "-g", label="corona deaths")
    plt.plot(t, z, "-r", label="non-corona deaths")

    plt.xlabel('Date')
    plt.ylabel('Deaths')
    plt.legend(loc="center left")
    plt.show()


if __name__ == '__main__':
    main()
