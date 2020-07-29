
data_folder = "./data"

file_corona_cases = "corona_cases.csv"
file_deaths_germany = "deaths_germany.xlsx"
csv_file_deaths_germany = "deaths_germany.csv"
file_rki_report = "rki_report.pdf"

path_corona_cases = "{}/{}".format(data_folder, file_corona_cases)
path_deaths_germany = "{}/{}".format(data_folder, file_deaths_germany)
csv_path_deaths_germany = "{}/{}".format(data_folder, csv_file_deaths_germany)
path_rki_report = "{}/{}".format(data_folder, file_rki_report)

backup_path_corona_cases = "{}/backup_{}".format(data_folder, file_corona_cases)
backup_path_deaths_germany = "{}/backup_{}".format(data_folder, file_deaths_germany)
backup_path_rki_report = "{}/backup_{}".format(data_folder, file_rki_report)

link_corona_cases = "https://opendata.ecdc.europa.eu/covid19/casedistribution/csv"
link_deaths_germany = "https://www.destatis.de/DE/Themen/Gesellschaft-Umwelt/Bevoelkerung/Sterbefaelle-Lebenserwartung/Tabellen/sonderauswertung-sterbefaelle.xlsx?__blob=publicationFile"
link_rki_report = "https://www.rki.de/DE/Content/InfAZ/N/Neuartiges_Coronavirus/Situationsberichte/2020-07-29-de.pdf?__blob=publicationFile"

data_sources = [
    (link_corona_cases, path_corona_cases, backup_path_corona_cases),
    (link_deaths_germany, path_deaths_germany, backup_path_deaths_germany),
    (link_rki_report, path_rki_report, backup_path_rki_report)
]
