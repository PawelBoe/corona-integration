import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.ticker import FuncFormatter as frmt

from models.BaseModel import db
from models.CoronaCases import CoronaCases
from models.DeathsGermany import DeathsGermany
from models.RkiTests import RkiTests


def main():
    corona_cases_germany()
    positives_to_tests_germany()
    total_corona_deaths_germany()

def corona_cases_germany():
    query = CoronaCases\
        .select()\
        .where(CoronaCases.geo_id == "DE")\
        .where(CoronaCases.date_reported >= "2020-02-15")\
        .order_by(CoronaCases.date_reported)

    time = []
    cases = []
    deaths = []
    for item in query:
        time.append(item.date_reported)
        cases.append(item.cases)
        deaths.append(item.deaths)

    t = []
    a = []
    b = []
    window = 4
    stride = 1
    for i in range(0, len(time) - (window-1), stride):
        t.append(time[i+window-1])
        a.append((sum(cases[i:i+window])) / window)
        b.append((sum(deaths[i:i+window])) / window)

    plt.suptitle('New COVID-19 Cases in Germany\n(Source: EU Open Data Portal)')

    ax1 = plt.gca()
    color = 'tab:blue'
    ax1.set_xlabel('Date')
    ax1.set_ylabel('New Cases', color=color)
    ax1.plot(t, a, color=color)
    ax1.tick_params(axis='y', labelcolor=color)
    ax2 = ax1.twinx()
    color = 'tab:red'
    ax2.set_ylabel('New Deaths', color=color)
    ax2.plot(t, b, color=color)
    ax2.tick_params(axis='y', labelcolor=color)
    ax1.set_ylim([0, 7000])
    ax2.set_ylim([0, 350])
    locator = mdates.AutoDateLocator()
    formatter = mdates.ConciseDateFormatter(locator)
    ax1.xaxis.set_major_locator(locator)
    ax1.xaxis.set_major_formatter(formatter)
    ax1.grid(True)

    plt.show()


def positives_to_tests_germany():
    query_tests = RkiTests\
        .select()\
        .order_by(RkiTests.calendar_week)

    time = []
    tests = []
    positives = []
    positives_ratio = []
    
    for item in query_tests:
        time.append(item.calendar_week)
        tests.append(item.tests / 1000)
        positives.append(item.positives / 1000)
        positives_ratio.append((item.positives / item.tests))

    plt.suptitle('COVID-19 tests and positives compared\n(Source: Robert Koch Institute Germany)')

    plt.subplot(2, 1, 1)
    ax1 = plt.gca()
    ax1.grid(True)
    plt.xticks(np.arange(min(time), max(time)+1, 1.0))
    color = 'tab:blue'
    ax1.set_xlabel('Calendar Week')
    ax1.set_ylabel('Tests (in thousands)', color=color)
    ax1.plot(time, tests, color=color)
    ax1.tick_params(axis='y', labelcolor=color)
    ax2 = ax1.twinx()
    color = 'tab:red'
    ax2.set_ylabel('Positives Ratio', color=color)
    ax2.plot(time, positives_ratio, color=color)
    ax2.tick_params(axis='y', labelcolor=color)
    ax1.set_ylim([0, 600])
    ax2.set_ylim([0, 0.30])

    plt.subplot(2, 1, 2)
    ax1 = plt.gca()
    ax1.grid(True)
    plt.xticks(np.arange(min(time), max(time)+1, 1.0))
    color = 'tab:blue'
    ax1.set_xlabel('Calendar Week')
    ax1.set_ylabel('Tests (in thousands)', color=color)
    ax1.plot(time, tests, color=color)
    ax1.tick_params(axis='y', labelcolor=color)
    ax2 = ax1.twinx()
    color = 'tab:red'
    ax2.set_ylabel('Absolute Positives (in thousands)', color=color)
    ax2.plot(time, positives, color=color)
    ax2.tick_params(axis='y', labelcolor=color)
    ax1.set_ylim([0, 600])
    ax2.set_ylim([0, 60])


    plt.show()

    plt.suptitle('COVID-19 tests performed in Germany\n(Sources: EU Open Data Portal, Robert Koch Institute)')


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
    plt.plot(t, b, "-m", label="covid-19 deaths 2020")
    plt.plot(t, c, "-r", label="non-covid-19 deaths 2020")

    plt.xlabel('Date')
    plt.ylabel('Deaths')
    plt.legend(loc="center left")
    plt.show()


if __name__ == '__main__':
    main()
