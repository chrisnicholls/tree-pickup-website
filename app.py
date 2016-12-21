from flask import Flask, request, jsonify, send_file, make_response, redirect, flash
from flask_login import LoginManager, login_required, login_user
import pandas as pd
from io import BytesIO
from functools import wraps, update_wrapper
from datetime import datetime
import os
from models import db, PickupRecord, User, PickupDate
from sqlalchemy import func, cast, DATE

from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

app = Flask(__name__, static_url_path='', static_folder='dist')
app.config.from_object(os.environ['APP_SETTINGS'])
app.secret_key = os.urandom(24)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.debug = True
login_manager = LoginManager()

db.init_app(app)
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


def nocache(view):
    @wraps(view)
    def no_cache(*args, **kwargs):
        response = make_response(view(*args, **kwargs))
        response.headers['Last-Modified'] = datetime.now()
        response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '-1'
        return response

    return update_wrapper(no_cache, view)


@app.route('/')
def index():
    return app.send_static_file('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        key = app.config['ENCRYPTION_KEY']

        print request.form
        user = User.valid_user(request.form['email'], request.form['password'], key, request.form['s'])
        print user

        if user is not None:
            login_user(user)
            flash('Logged in')
            next = request.args.get('next')
            return redirect(next)

    return app.send_static_file('login.html')


@app.route('/admin/')
@login_required
def admin():
    return app.send_static_file('admin/index.html')


@app.route('/api/hello')
def hello():
    return "Hello World!"


@app.route('/api/pickup', methods=['POST'])
def new_record():
    print request.form
    name = request.form['name']
    street_number = request.form['streetNumber']
    street_name = request.form['streetName']
    phone = request.form['phone']
    neighbourhood = request.form['neighbourhood']
    pickup_date = request.form['pickupDate']
    payment = request.form['payment']
    other_instructions = request.form['otherInstructions']
    email_address = request.form['email']
    source = request.form['source']

    pr = PickupRecord(name, email_address, street_number, street_name, neighbourhood, phone,
                      pickup_date, payment, other_instructions, datetime.now(), source)

    db.session.add(pr)
    db.session.commit()

    return "success"


@app.route('/api/pickupDates', methods=['GET'])
def get_pickup_dates():
    pickup_dates = PickupDate.query.filter(PickupDate.open_time < datetime.now()) \
        .filter(PickupDate.close_time > datetime.now())

    d = {"dates": []}

    for pickup_date in pickup_dates:
        d["dates"].append(pickup_date.date)

    return jsonify(d)


@app.route('/admin/download', methods=['GET'])
@nocache
@login_required
def get_pickup_records():
    query = PickupRecord.query

    df = pd.read_sql(query.statement, query.session.bind)

    io = BytesIO()

    # Use a temp filename to keep pandas happy.
    writer = pd.ExcelWriter(io, engine='openpyxl')

    df = df.drop('pickupRecordId', 1)

    # Write the data frame to the StringIO object.
    df.to_excel(writer, sheet_name='Sheet1', index=False)
    writer.save()

    io.seek(0)

    return send_file(io, attachment_filename='pickups.xlsx', as_attachment=True)

@app.route('/admin/chartData', methods=['GET'])
@nocache
@login_required
def get_chart_data():
    # query = ("select count(*),source,DATE(CONVERT_TZ(dateSubmitted, 'GMT', '-04:00')) as d from PickupRecord group by d,source")

    d = cast(PickupRecord.date_submitted, DATE).label('d')
    counts = db.session.query(func.count('*'), d, PickupRecord.source).select_from(PickupRecord).group_by(d, PickupRecord.source).all()

    data = {}

    sources = set()

    for row in counts:
        date = str(row[2])
        source = row[1]
        count = row[0]

        if date not in data:
            data[date] = {}

        data[date][source] = count

        sources.add(source)

    options = dict()
    options['xAxis'] = sorted(data.keys())
    options['series'] = []

    for source in sources:
        counts = []
        for date in options['xAxis']:
            if source in data[date]:
                counts.append(data[date][source])
            else:
                counts.append(0)

        options['series'].append({'name': source, 'data': counts})

    return jsonify(options)


if __name__ == "__main__":
    app.run()
