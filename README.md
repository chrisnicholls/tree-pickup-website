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
Create a heroku app
```bash
(scouts)cnicholls@cnicholls-ltm3 tree-pickup-website (master)*$ heroku create scouts-tree-pickup-stage
Creating ⬢ scouts-tree-pickup-stage... done
https://scouts-tree-pickup-setup.herokuapp.com/ | https://git.heroku.com/scouts-tree-pickup-stage.git
```

Add a remote for this app (to have separate apps for staging and prod - I called it setup just for examples for this doc)
```bash
git remote add stage git@heroku.com:scouts-tree-pickup-setup.git
```

Set config vars on heroku
```bash
(scouts)cnicholls@cnicholls-ltm3 tree-pickup-website (master)*$ heroku config:set APP_SETTINGS=config.Config --remote stage
Setting APP_SETTINGS and restarting ⬢ scouts-tree-pickup-setup... done, v3
APP_SETTINGS: config.Config
```

Provision a DB (this example uses the free hobby-dev)
```bash
(scouts)cnicholls@cnicholls-ltm3 tree-pickup-website (master)*$ heroku addons:create heroku-postgresql:hobby-dev --app scouts-tree-pickup-stage
Creating heroku-postgresql:hobby-dev on ⬢ scouts-tree-pickup-stage... free
Database has been created and is available
 ! This database is empty. If upgrading, you can transfer
 ! data from another database with pg:copy
Created postgresql-clean-16945 as DATABASE_URL
Use heroku addons:docs heroku-postgresql to view documentation
```

Double check config vars that DATABASE_URL is set
```bash
(scouts)cnicholls@cnicholls-ltm3 tree-pickup-website (master)*$ heroku config --app scouts-tree-pickup-stage
=== scouts-tree-pickup-stage Config Vars
APP_SETTINGS: config.Config
DATABASE_URL: postgres://aglfiinfyfgvyu:ffff25509541ba4a527c568ee6aad67ffffdf2ac3622c0bd60342e5089511d75@ec2-54-163-234-140.compute-1.amazonaws.com:5432/d2ldetuclffff
```

Push the code
```bash
scouts)cnicholls@cnicholls-ltm3 tree-pickup-website (master)*$ git push stage master
Counting objects: 203, done.
Delta compression using up to 8 threads.
Compressing objects: 100% (102/102), done.
Writing objects: 100% (203/203), 1.02 MiB | 0 bytes/s, done.
Total 203 (delta 91), reused 175 (delta 85)
remote: Compressing source files... done.

...

remote: -----> Discovering process types
remote:        Procfile declares types -> web
remote: 
remote: -----> Compressing...
remote:        Done: 76.9M
remote: -----> Launching...
remote:        Released v5
remote:        https://scouts-tree-pickup-setup.herokuapp.com/ deployed to Heroku
remote: 
remote: Verifying deploy... done.
To git@heroku.com:scouts-tree-pickup-setup.git
 * [new branch]      master -> master
```

Set up the db tables
```bash
(scouts)cnicholls@cnicholls-ltm3 tree-pickup-website (master)*$ heroku run python manage.py db upgrade --app scouts-tree-pickup-stage
Running python manage.py db upgrade on ⬢ scouts-tree-pickup-stage... up, run.5991 (Free)
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
(scouts)cnicholls@cnicholls-ltm3 tree-pickup-website (master)*$ heroku run python manage.py seed --app scouts-tree-pickup-stage
Running python manage.py seed on ⬢ scouts-tree-pickup-stage... up, run.2930 (Free)
```

All set! Try it out by going to 
https://scouts-tree-pickup-stage.herokuapp.com

## Add Admin User
