import argparse
import json
import csv
import datetime
import urllib.request
import pandas as pd
import pdfplumber
import re

import corona_config as cfg

from models.BaseModel import db
from models.CoronaCases import CoronaCases
from models.DeathsGermany import DeathsGermany
from models.CountryData import CountryData
from models.RkiTests import RkiTests

tests_report =[
        (10, 124716, 3892, 3.12),
        (11, 127457, 7582, 5.95),
        (12, 348619 ,23820, 6.83),
        (13, 361515, 31414, 8.69),
        (14, 408348, 36885, 9.03),
        (15, 380197, 30791, 8.10),
        (16, 331902, 22082, 6.65),
        (17, 363890, 18083, 4.97),
        (18, 326788, 12608, 3.86),
        (19, 403875, 10755, 2.66),
        (20, 432666, 7233, 1.67),
        (21, 353467, 5218, 1.48),
        (22, 405269, 4310, 1.06),
        (23, 340986, 3208, 0.94),
        (24, 327196, 2816, 0.86),
        (25, 388187, 5316, 1.37),
        (26, 467413, 3689, 0.79),
        (27, 507663, 3104, 0.61),
        (28, 510551, 2992, 0.59),
        (29, 538701, 3497, 0.65),
        (30, 574883, 4539, 0.79),
        (31, 586620, 5738, 0.98),
        (32, 736171, 7335, 1.00),
        (33, 891988, 8661, 0.97),
        (34, 1094506, 9233, 0.84),
        (35, 1121214, 8324, 0.74),
        (36, 1099560, 8175, 0.74),
        (37, 1162133, 10025, 0.86),
        (38, 1149171, 13275, 1.16),
        (39, 1168390, 14301, 1.22),
        (40, 1095858, 17964, 1.64),
        ]


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
            user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'

            headers={'User-Agent':user_agent,}

            request=urllib.request.Request(link, None, headers)
            with urllib.request.urlopen(request) as url_file:
                with open (current, "wb") as output:
                    output.write(url_file.read())
        except Exception as e:
            print("Something went wrong during download {}:".format(current))
            print("{}".format(e))

def create_database():
    create_tables()
    import_corona_cases()
    import_deaths_germany()
    import_rki_report_manual()


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
        DeathsGermany,
        RkiTests
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
                    population = safe_cast(row["popData2019"], int, 0),
                    continent = row["continentExp"]
                )


def import_deaths_germany():
    print("import deaths germany table")

    data_xls = pd.read_excel(cfg.path_deaths_germany, "D_2016_2020_Tage", header=8, index_col=0, nrows=13)

    with db.transaction():
        for year in data_xls.index:
            for day in data_xls.columns:
                if day == "Insgesamt":
                    continue

                month = day.split(".")[1]
                d = day.split(".")[0]
                datum = "{}-{}-{}".format(year, month, d)
                deaths = safe_cast(data_xls[day][year], int, 0)
                if deaths == 0:
                    continue

                DeathsGermany.create(
                    date = datum,
                    age_group_start = safe_cast(0, int, 0),
                    age_group_end = safe_cast(150, int, 150),
                    deaths = deaths
                )

def import_rki_report_manual():
    print("import rki report manual")

    with db.transaction():
        for r in tests_report:
            RkiTests.create(
                calendar_week = safe_cast(r[0], int, 0),
                tests = safe_cast(r[1], int, 0),
                positives = safe_cast(r[2], int, 0),
                # ignore percentage column
                participating_laboratories = safe_cast(0, int, 0)
            )

def import_rki_report():
    print("import rki report")

    pattern = "[0-9]{2}  [0-9]{3}.[0-9]{3}  [0-9]+.[0-9]{3}  [0-9]+,[0-9]+  [0-9]+"

    def num(s):
        try:
            return int(s)
        except ValueError:
            return float(s)

    pdf_file = pdfplumber.open(cfg.path_rki_report)
    page = pdf_file.pages[11]
    text = page.extract_text()
    result = re.findall(pattern, text)

    rows = []
    for i in result:
        rows.append(i.split())

    new_rows = []
    for row in rows:
        new_row = []
        for entry in row:
            entry = entry.replace(".", "")
            entry = entry.replace("(", "")
            entry = entry.replace(")", "")
            entry = entry.replace("%", "")
            entry = entry.replace(",", "")
            new_row.append(num(entry))
        new_rows.append(new_row)

    with db.transaction():
        for r in new_rows:
            RkiTests.create(
                calendar_week = safe_cast(r[0], int, 0),
                tests = safe_cast(r[1], int, 0),
                positives = safe_cast(r[2], int, 0),
                # ignore percentage column
                participating_laboratories = safe_cast(r[4], int, 0)
            )


if __name__ == '__main__':
    main()
