import os
from datetime import datetime

from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from sqlalchemy import func, cast, DATE

from app import app, db
from models import PickupDate,User,PickupRecord,AESCipher

app.config.from_object(os.environ['APP_SETTINGS'])

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)


@manager.command
def seed():
    pd = PickupDate('Saturday, January 7, 2017', datetime(2016, 12, 19), datetime(2017, 1, 5))
    db.session.add(pd)
    db.session.commit()

    pd = PickupDate('Saturday, January 14, 2017', datetime(2016, 12, 19), datetime(2017, 1, 12))
    db.session.add(pd)
    db.session.commit()

@manager.command
def seed_users():
    '''
    u = User('Chris Nicholls', 'chrisjohnnicholls@gmail.com',
             'i2HI5DJJRgvPp8XU3/ZJDdfVtUkJSdZ+MJ7ECeeVlyQAnDNStjsvEhASgNA74ajB')

    db.session.add(u)
    db.session.commit()
    '''

    u = User('Doug Prosser', 'doug.prosser@amecfw.com',
             'VmtMt4oCVrk30brNJqPU5Hqxr1fOgEDFzvb8pqssNKvvd16RqTjvfRhMJI1b6qw5')
    db.session.add(u)
    db.session.commit()


@manager.command
def dates():
    pickup_dates = PickupDate.query.filter(PickupDate.open_time < datetime.now()) \
        .filter(PickupDate.close_time > datetime.now())

    d = {"dates": []}

    for pickup_date in pickup_dates:
        d["dates"].append(pickup_date.date)

    print d


@manager.command
def chart():
    d = cast(PickupRecord.date_submitted.astimezone(), DATE).label('d')
    b = db.session.query(func.count('*'), d, PickupRecord.source).select_from(PickupRecord).group_by(d, PickupRecord.source).all()
    print b

    for row in b:
        print type(row)
        print row[1]


@manager.command
def add_user(name, email, password):
    encrypted_password = AESCipher(app.config['ENCRYPTION_KEY']).encrypt(password)

    print 'name=%s, email=%s, password=%s' %(name, email, encrypted_password)

    u = User(name, email, encrypted_password)
    db.session.add(u)
    db.session.commit()


if __name__ == '__main__':
    manager.run()

