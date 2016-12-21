# Set Up
## Local
First, install postgres and make sure it's running.

Create a virtual environment and install dependencies (this example uses virtualenvwrapper)
```bash
mkvirtualenv scouts
pip install -r requirements.txt
```

Next, edit the `.env` file if necessary to update the DATABASE_URI. 

Create the database
```bash
(scouts)cnicholls@cnicholls-ltm3 tree-pickup-website (master)*$ psql
psql (9.5.1, server 9.6.1)
WARNING: psql major version 9.5, server major version 9.6.
         Some psql features might not work.
Type "help" for help.

cnicholls=# create database scouts;
CREATE DATABASE
```

Now use flask-migrate to create the tables.
```bash
(scouts)cnicholls@cnicholls-ltm3 tree-pickup-website (master)*$ python manage.py db upgrade
INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
INFO  [alembic.runtime.migration] Running upgrade  -> 0c1a05f45bc9, empty message
INFO  [alembic.runtime.migration] Running upgrade 0c1a05f45bc9 -> 6cd2c17ac72b, empty message
INFO  [alembic.runtime.migration] Running upgrade 6cd2c17ac72b -> 47e310ef85b4, empty message
INFO  [alembic.runtime.migration] Running upgrade 47e310ef85b4 -> 9967e9d52599, empty message
INFO  [alembic.runtime.migration] Running upgrade 9967e9d52599 -> b5e17459ff10, empty message
INFO  [alembic.runtime.migration] Running upgrade b5e17459ff10 -> 22d57adbc78d, empty message
```

Seed the pickup dates
```bash
(scouts)cnicholls@cnicholls-ltm3 tree-pickup-website (master)*$ python manage.py seed
```

Sanity check the dates
```bash
(scouts)cnicholls@cnicholls-ltm3 tree-pickup-website (master)*$ psql scouts
psql (9.5.1, server 9.6.1)
WARNING: psql major version 9.5, server major version 9.6.
         Some psql features might not work.
Type "help" for help.

scouts=# select * from pickup_date ;
 pickupDateId |         pickupDate         |      openTime       |      closeTime      
--------------+----------------------------+---------------------+---------------------
            1 | Saturday, January 7, 2017  | 2016-12-19 00:00:00 | 2017-01-05 00:00:00
            2 | Saturday, January 14, 2017 | 2016-12-19 00:00:00 | 2017-01-12 00:00:00
(2 rows)
```

All set, run the app!
```bash
(scouts)cnicholls@cnicholls-ltm3 tree-pickup-website (master)*$ python app.py
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
 * Restarting with stat
 * Debugger is active!
 * Debugger pin code: 190-810-610
```

## Heroku

## Seed Pickup Dates

## Add Admin User
