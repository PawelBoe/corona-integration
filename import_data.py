import argparse
import json
import csv
import datetime
import urllib.request
import pandas as pd

import corona_config as cfg

from models.BaseModel import db
from models.CoronaCases import CoronaCases
from models.DeathsGermany import DeathsGermany
from models.CountryData import CountryData


def safe_cast(val, to_type, default=None):
    try:
        return to_type(val)
    except (ValueError, TypeError):
        return default


def save_backup():

    for s in cfg.data_sources:
        _, current, backup = s
        try:
            with open (current, "rb") as current_file:
                with open(backup, "wb") as backup_file:
                    backup_file.write(current_file.read())
        except Exception as e:
            print("Something went wrong during backup save of {}:".format(current))
            print("{}".format(e))

def load_backup():
    for s in cfg.data_sources:
        _, current, backup = s
        try:
            with open (current, "wb") as current_file:
                with open(backup, "rb") as backup_file:
                    current_file.write(backup_file.read())
        except Exception as e:
            print("Something went wrong during backup laod of {}:".format(current))
            print("{}".format(e))

def download():
    for s in cfg.data_sources:
        link, current, _ = s
        try:
            with urllib.request.urlopen(link) as url_file:
                with open (current, "wb") as output:
                    output.write(url_file.read())
        except Exception as e:
            print("Something went wrong during download {}:".format(current))
            print("{}".format(e))

def create_database():
    create_tables()
    import_corona_cases()
    import_deaths_germany()


def main():
    parser = argparse.ArgumentParser('Create corona cases database')
    parser.add_argument('--download', action='store_true')
    parser.add_argument('--save_backup', action='store_true')
    parser.add_argument('--load_backup', action='store_true')
    parser.add_argument('--create_database', action='store_true')
    args = parser.parse_args()

    if args.download:
        download()
    if args.save_backup:
        save_backup()
    if args.load_backup:
        load_backup()
    if args.create_database:
        create_database()

def create_tables():
    db_models = [
        CoronaCases,
        CountryData,
        DeathsGermany
    ]
    db.drop_tables(db_models)
    db.create_tables(db_models)

def import_corona_cases():
    print("import corona cases table")

    file_name = cfg.path_corona_cases
    with open(file_name, 'r') as file_pointer:
        reader = csv.DictReader(file_pointer, delimiter=',')

        with db.transaction():
            for row in reader:
                CoronaCases.create(
                    date_reported = datetime.datetime.strptime(row["dateRep"], "%d/%m/%Y"),
                    day = safe_cast(row["day"], int, 0),
                    month = safe_cast(row["month"], int, 0),
                    year = safe_cast(row["year"], int, 0),
                    cases = safe_cast(row["cases"], int, 0),
                    deaths = safe_cast(row["deaths"], int, 0),
                    country = row["countriesAndTerritories"],
                    geo_id = row["geoId"],
                    country_code = row["countryterritoryCode"],
                    population = safe_cast(row["popData2018"], int, 0),
                    continent = row["continentExp"]
                )


def import_deaths_germany():
    print("import deaths germany table")

    data_2020_xls = pd.read_excel(cfg.path_deaths_germany, "D_2020_Tage", header=8, index_col=0, nrows=13)
    data_2019_xls = pd.read_excel(cfg.path_deaths_germany, "D_2019_Tage", header=8, index_col=0, nrows=13)
    data_2018_xls = pd.read_excel(cfg.path_deaths_germany, "D_2018_Tage", header=8, index_col=0, nrows=13)
    data_2017_xls = pd.read_excel(cfg.path_deaths_germany, "D_2017_Tage", header=8, index_col=0, nrows=13)
    data_2016_xls = pd.read_excel(cfg.path_deaths_germany, "D_2016_Tage", header=8, index_col=0, nrows=13)

    years = [
        data_2020_xls,
        data_2019_xls,
        data_2018_xls,
        data_2017_xls,
        data_2016_xls
    ]

    with db.transaction():
        for year in years:
            year = year.T
            for age in year.columns:
                for day in year.index:
                    if not isinstance(day, datetime.date):
                        continue
                    if day == "Insgesamt":
                        continue
                    DeathsGermany.create(
                        date = day,
                        age_group_start = safe_cast(age[:3], int, 0),
                        age_group_end = safe_cast(age[5:8], int, 150),
                        deaths = safe_cast(year[age][day], int, 0)
                    )


if __name__ == '__main__':
    main()
