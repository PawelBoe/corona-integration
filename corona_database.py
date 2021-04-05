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
from models.CoronaCasesWeekly import CoronaCasesWeekly
from models.DeathsGermany import DeathsGermany
from models.CountryData import CountryData
from models.RkiTests import RkiTests
from models.DiviBeds import DiviBeds


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
    import_corona_cases_weekly()
    import_deaths_germany()
    import_rki_report_manual()
    import_beds_germany()


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
        CoronaCasesWeekly,
        CountryData,
        DeathsGermany,
        RkiTests,
        DiviBeds
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

def import_corona_cases_weekly():
    print("import corona cases weekly table")

    file_name = cfg.path_corona_cases_weekly
    with open(file_name, 'r') as file_pointer:
        reader = csv.DictReader(file_pointer, delimiter=',')

        with db.transaction():
            for row in reader:
                year_week = row["year_week"]
                date = datetime.datetime.strptime(year_week + "-1", "%Y-%W-%w")
                year, week, day = date.isocalendar()

                entry, created = CoronaCasesWeekly.get_or_create(
                    date_reported = date,
                    year = safe_cast(year, int, 0),
                    week = safe_cast(week, int, 0),
                    country_code = row["country_code"],
                    population = safe_cast(row["population"], int, 0),
                    continent = row["continent"],
                    defaults = {"deaths" : 0, "cases" : 0}
                )

                if row["indicator"] == "cases":
                    entry.cases = safe_cast(row["weekly_count"], int, 0)
                elif row["indicator"] == "deaths":
                    entry.deaths = safe_cast(row["weekly_count"], int, 0)

                entry.save()

def import_deaths_germany():
    print("import deaths germany table")

    data_xls = pd.read_excel(cfg.path_deaths_germany, "D_2016_2021_Tage", header=8, index_col=0, nrows=13, engine="openpyxl")

    with db.transaction():
        for year in data_xls.index:
            for day in data_xls.columns:
                if day == "Insgesamt":
                    continue

                try:
                    month = day.split(".")[1]
                    d = day.split(".")[0]
                    datum = "{}-{}-{}".format(year, month, d)
                    deaths = safe_cast(data_xls[day][year], int, 0)
                except:
                    continue
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

    file_name = cfg.csv_path_tests_germany
    with open(file_name, 'r') as file_pointer:
        reader = csv.DictReader(file_pointer, delimiter=',')

        with db.transaction():
            for row in reader:
                RkiTests.create(
                    calendar_week = safe_cast(row["week"], int, 0),
                    tests = safe_cast(row["test_count"], int, 0),
                    positives = safe_cast(row["positives_count"], int, 0),
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
        for row in new_rows:
            RkiTests.create(
                calendar_week = safe_cast(row[0], int, 0),
                tests = safe_cast(row[1], int, 0),
                positives = safe_cast(row[2], int, 0),
                # ignore percentage column
                participating_laboratories = safe_cast(row[4], int, 0)
            )

def import_beds_germany():
    print("import beds germany")

    file_name = cfg.csv_path_beds_germany
    with open(file_name, 'r') as file_pointer:
        reader = csv.DictReader(file_pointer, delimiter=',')

        with db.transaction():
            for row in reader:
                DiviBeds.create(
                    date = datetime.datetime.strptime(row["date"], "%Y-%m-%d"),
                    used_beds = safe_cast(row["used_beds_total"], int, 0),
                    corona_beds = safe_cast(row["used_beds_corona"], int, 0),
                    free_beds = safe_cast(row["free_beds"], int, 0),
                    emergency_beds = safe_cast(row["emergency_beds"], int, 0),
                )

if __name__ == '__main__':
    main()
