# corona-integration
Integration of different COVID-19 virus related datasets into a single database. Contains different statistics and viualizations which are mostly focused on Germany and Europe.

I have created these scripts to quickly query raw COVID-19 data using sql and to be able to run my own statistics on it. I am doing this out of own curiosity. If this helps anyone, please feel free to use this as a start for your own analysis.


## Getting started
To install the required packages run the following commands:

`python3 -m venv ./venv;`
`source venv/bin/activate;`
`pip install -r requirements.txt;`


## Creating the database
If you follow these steps you will find a `data.sqlite` file in the `/data` folder which will contain all the integrated datasets in its tables. Once the original data sources change you can re-run the download and create commands to update the database. Some data sources are directly present in the ´/sources´ folder because an automated download is more cumbersome for me than to manually pull these sets into this repository.

### Downloading the datasets
`python corona_database.py --download;`

### Creating backups
`python corona_database.py --save_backup;`

### Loading backups
`python corona_database.py --load_backup;`

### Integrating tables into database
`python corona_database.py --create_database;`


## Database schema
Fields in Table: `corona_cases` (obsolete, only till 14. December 2020)
* date reported
* day
* month
* year
* cases
* deaths
* country
* geo id
* country code
* population
* continent
* processed (time of insertion into database)

Fields in Table: `corona_cases_weekly` (new, since 14. December 2020)
* year
* week
* cases
* deaths
* country code
* population
* continent
* processed (time of insertion into database)

Fields in Table: `deaths_germany`
* date
* age group start (lower age limit, e.g. 30 years)
* age group end (upper age limit, e.g. 50 years)
* deaths
* processed (time of insertion into database)

Fields in Table `rki_tests`
* calendar week
* tests
* positives
* participating laboratories
* processed (time of insertion into database)

Fields in Table `divi_beds`
* date
* free beds
* emergency beds
* used beds (all patients)
* used beds (corona patients)
* processed (time of insertion into database)


## Sources
The integrated sources so far consist of:
* the total number of COVID-19 cases reported worlwide daily (obsolete), comming from the EU Open Data Portal (https://data.europa.eu/euodp/en/data/dataset/covid-19-coronavirus-data) 
* the total number of COVID-19 cases reported worlwide weekly, comming from the EU Open Data Portal (https://data.europa.eu/euodp/en/data/dataset/covid-19-coronavirus-data-weekly-from-17-december-2020) 
* the total number of all cause deaths in Germany, reported by the Statistisches Bundesamt (https://www.destatis.de/DE/Themen/Gesellschaft-Umwelt/Bevoelkerung/Sterbefaelle-Lebenserwartung/Tabellen/sonderauswertung-sterbefaelle.html)
* the total number of performed COVID-19 tests in Germany, reported by the Robert Koch Institute (https://www.rki.de/DE/Content/InfAZ/N/Neuartiges_Coronavirus/Testzahl.html)
* the total number of used intensive care beds in germany, reported by the DIVI-Intensivregister in Germany (https://www.intensivregister.de)

The ´/sources´ folder contains data from the aforementioned open/free sources that was manually integrated from pdf and csv files because automated retreival was more cumbersome for me.


## Results

### Total deaths in relation to COVID-19 deaths in germany
The source code can be found in the function `total_corona_deaths_germany` in `corona_analysis.py`. Because of the registration delay of deaths at the Statistisches Bundesamt the data is not up to date (behind by about 3-5 Weeks). This curve is smoothed by averaging each day with the day before (sliding window smoothing with a window size of 2 and a stride of 1).

**Note**: The death toll underlies daily (and yearly) fluctuations. Statistically significant conclusions regarding overlap of deaths due to COVID-19 and deaths that would have occured anyway cannot be drawn based on this graph.

![](results/corona_total_deaths_germany.png)

This curve shows the new covid-19 data that is now provided weekly by the EU Open Data Portal. That is why the covid-19 samples appear less frequently than the total death toll data and thus look less detailed. The years overlap in this graph, which is why the samples of previous years repeat at the outskirts of the year scale.
![](results/corona_total_deaths_germany_weekly.png)

### Total intensive care bed usage in relation to COVID-19 bed usage
The source code can be found in the function `intensive_care_beds_germany` in `corona_analysis.py`. The measurement starts off at the 20th of April, when the corona related bed usage was at its peak. Earlier values in the graph are more inaccurate since fewer intensive care facilities where participating in the data collection.

**Note**: One can see that even though the covid-19 related bed usage goes up, no total incerase in intensive care is observed. This is a strange contrast to the expected behavior, which would be an increase in intensive care patients and a constant bed usage by non-covid-19 patients (due to the excess of free bed capacity in Germany). Actually there is a decrease in non-covid-19 patients which suggests a hidden overlab between these two groups (non-covid-19 and covid-19 patients).

![](results/intensive_care_beds_germany.png)

### COVID-19 positives compared to total tests
The source code can be found in the function `positives_to_tests_germany` in `corona_analysis.py`. This curve shows the weekly total tests taken in relation to the positive results.

![](results/test_positive_ratio_germany.png)

### New COVID-19 cases/deaths per week in germany
The source code can be found in the function `corona_cases_germany` in `corona_analysis.py`. This curve shows the weekly sum of cases and deaths in germany.

**Note**: One can see that (if scaled to match) the COVID-19 cases and the deaths are correlated by a delay of about 10 to 15 days.

![](results/corona_new_cases_germany.png)
