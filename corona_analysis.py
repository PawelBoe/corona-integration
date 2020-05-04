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
    query_2020 = CoronaCases\
        .select(CoronaCases.deaths, CoronaCases.cases, CoronaCases.date_reported, DeathsGermany.deaths)\
        .join(DeathsGermany, attr="total", on=CoronaCases.date_reported == DeathsGermany.date)\
        .where(CoronaCases.geo_id == "DE")\
        .where(DeathsGermany.age_group_start == 0)\
        .where(DeathsGermany.age_group_end == 150)\
        .where(DeathsGermany.date >= "2020-01-01")\
        .order_by(DeathsGermany.date)

    query_2019 = DeathsGermany\
        .select()\
        .where(DeathsGermany.age_group_start == 0)\
        .where(DeathsGermany.age_group_end == 150)\
        .where(DeathsGermany.date >= "2019-01-01")\
        .order_by(DeathsGermany.date)

    query_2018 = DeathsGermany\
        .select()\
        .where(DeathsGermany.age_group_start == 0)\
        .where(DeathsGermany.age_group_end == 150)\
        .where(DeathsGermany.date >= "2018-01-01")\
        .order_by(DeathsGermany.date)

    query_2017 = DeathsGermany\
        .select()\
        .where(DeathsGermany.age_group_start == 0)\
        .where(DeathsGermany.age_group_end == 150)\
        .where(DeathsGermany.date >= "2017-01-01")\
        .order_by(DeathsGermany.date)

    time = []
    corona_cases = []
    corona_deaths = []
    total_deaths_2020 = []
    for item in query_2020:
        time.append(item.date_reported)
        corona_cases.append(item.cases)
        corona_deaths.append(item.deaths)
        total_deaths_2020.append(item.total.deaths)

    total_deaths_2019 = []
    for item in query_2019:
        total_deaths_2019.append(item.deaths)

    total_deaths_2018 = []
    for item in query_2018:
        total_deaths_2018.append(item.deaths)

    total_deaths_2017 = []
    for item in query_2017:
        total_deaths_2017.append(item.deaths)

    t = []
    a = []
    b = []
    c = []
    d = []
    e = []
    f = []
    window = 2
    stride = 1
    for i in range(0, len(time) - (window-1), stride):
        td2020 = total_deaths_2020
        td2019 = total_deaths_2019
        td2018 = total_deaths_2018
        td2017 = total_deaths_2017
        cd = corona_deaths
        t.append(time[i+window-1])
        a.append((sum(td2020[i:i+window])) / window)
        b.append((sum(cd[i:i+window])) / window)
        c.append(a[i] - b[i])
        d.append((sum(td2019[i:i+window])) / window)
        e.append((sum(td2018[i:i+window])) / window)
        f.append((sum(td2017[i:i+window])) / window)

    plt.suptitle('Daily Deaths in Germany\n(Sources: EU Open Data Portal, Statistisches Bundesamt)')

    locator = mdates.AutoDateLocator()
    formatter = mdates.ConciseDateFormatter(locator)
    plt.gca().xaxis.set_major_locator(locator)
    plt.gca().xaxis.set_major_formatter(formatter)
    plt.gca().grid(True)

    plt.plot(t, a, "-b", label="total deaths 2020")
    plt.plot(t, d, ":y", label="total deaths 2019")
    plt.plot(t, e, ":g", label="total deaths 2018")
    plt.plot(t, f, ":c", label="total deaths 2017")
    plt.plot(t, b, "-m", label="corona deaths 2020")
    plt.plot(t, c, "-r", label="non-corona deaths 2020")

    plt.xlabel('Date')
    plt.ylabel('Deaths')
    plt.legend(loc="center left")
    plt.show()


if __name__ == '__main__':
    main()
