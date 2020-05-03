import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

from models.BaseModel import db
from models.CoronaCases import CoronaCases
from models.DeathsGermany import DeathsGermany


def main():
    result = CoronaCases.select().where(CoronaCases.geo_id == "UK")

    time = []
    cases = []
    deaths = []
    for item in result:
        time.append(item.date_reported)
        cases.append(item.cases)
        deaths.append(item.deaths)

    plt.plot(time, deaths)

    plt.xlabel('time')
    plt.ylabel('cases')
    plt.show()




if __name__ == '__main__':
    main()
