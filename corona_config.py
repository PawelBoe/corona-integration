
data_folder = "./data"
sources_folder = "./sources"

file_corona_cases = "corona_cases.csv"
file_corona_cases_weekly = "corona_cases_weekly.csv"
file_deaths_germany = "deaths_germany.xlsx"
csv_file_deaths_germany = "deaths_germany.csv"
csv_file_tests_germany = "rki_tests.csv"
csv_file_beds_germany = "divi_beds.csv"

path_corona_cases = "{}/{}".format(data_folder, file_corona_cases)
path_corona_cases_weekly = "{}/{}".format(data_folder, file_corona_cases_weekly)
path_deaths_germany = "{}/{}".format(data_folder, file_deaths_germany)
csv_path_deaths_germany = "{}/{}".format(data_folder, csv_file_deaths_germany)
csv_path_tests_germany = "{}/{}".format(sources_folder, csv_file_tests_germany)
csv_path_beds_germany = "{}/{}".format(sources_folder, csv_file_beds_germany)

backup_path_corona_cases = "{}/backup_{}".format(data_folder, file_corona_cases)
backup_path_corona_cases_weekly = "{}/backup_{}".format(data_folder, file_corona_cases_weekly)
backup_path_deaths_germany = "{}/backup_{}".format(data_folder, file_deaths_germany)

link_corona_cases = "https://opendata.ecdc.europa.eu/covid19/casedistribution/csv"
link_corona_cases_weekly = "https://opendata.ecdc.europa.eu/covid19/nationalcasedeath/csv"
link_deaths_germany = "https://www.destatis.de/DE/Themen/Gesellschaft-Umwelt/Bevoelkerung/Sterbefaelle-Lebenserwartung/Tabellen/sonderauswertung-sterbefaelle.xlsx?__blob=publicationFile"

data_sources = [
    (link_corona_cases, path_corona_cases, backup_path_corona_cases),
    (link_corona_cases_weekly, path_corona_cases_weekly, backup_path_corona_cases_weekly),
    (link_deaths_germany, path_deaths_germany, backup_path_deaths_germany),
]
