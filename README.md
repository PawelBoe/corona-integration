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

### Importing tables into database
`python import_data.py --create_database`


## Database schema
TODO


## Sources
TODO

