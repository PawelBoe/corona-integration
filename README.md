# corona-integration
Integration of different corona virus related datasets into a single database. Contains different statistics and viualizations which are mostly focused on Germany and Europe.

I have created these scripts to quickly query raw corona data using sql and to be able to run my own statistics on it. I am doing this out of own curiosity. If this helps anyone, please feel free to use this as a start for your own analysis.


## Getting started
To install the required packages run the following commands:

`python3 -m venv ./venv`
`source venv/bin/activate`
`pip install -r requirements.txt`


## Creating the database
If you follow these steps you will find a `data.sqlite` file in the `/data` folder which will contain all the integrated datasets in its tables.

### Download the datasets
`python import_data.py --download`

### Creating backups
`python import_data.py --save_backup`

### Loading backups
`python import_data.py --load_backup`

### Integrating tables into database
`python import_data.py --create_database`


## Database schema
Fields in Table: `corona_cases`
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

Fields in Table: `deaths_germany`
* date
* age group start (lower age limit, e.g. 30 years)
* age group end (upper age limit, e.g. 50 years)
* deaths
* processed (time of insertion into database)


## Sources
The integrated sources so far consist of:
* the total COVID-19 cases reported worlwide, comming from the EU Open Data Portal (https://data.europa.eu/euodp/en/data/dataset/covid-19-coronavirus-data) 
* the total all cause deaths reported by the Statistisches Bundesamt in Germany (https://www.destatis.de/DE/Themen/Gesellschaft-Umwelt/Bevoelkerung/Sterbefaelle-Lebenserwartung/Tabellen/sonderauswertung-sterbefaelle.html)
