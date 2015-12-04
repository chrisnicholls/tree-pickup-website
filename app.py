from flask import Flask, request, jsonify, send_file, make_response
from flaskext.mysql import MySQL
import pandas as pd
import MySQLdb
from io import BytesIO
from functools import wraps, update_wrapper
from datetime import datetime

mysql = MySQL()
app = Flask(__name__, static_url_path='', static_folder='dist')
app.config.from_pyfile('config.py')
app.debug = True
mysql.init_app(app)

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

@app.route('/admin/')
def admin():
    return app.send_static_file('admin/index.html')

@app.route('/api/hello')
def hello():
    return "Hello World!"

@app.route('/api/pickup', methods=['POST'])
def new_record():
    print request.form
    name = MySQLdb.escape_string(request.form['name'])
    street_number = MySQLdb.escape_string(request.form['streetNumber'])
    street_name = MySQLdb.escape_string(request.form['streetName'])
    phone = MySQLdb.escape_string(request.form['phone'])
    neighbourhood = MySQLdb.escape_string(request.form['neighbourhood'])
    pickup_date = MySQLdb.escape_string(request.form['pickupDate'])
    payment = MySQLdb.escape_string(request.form['payment'])
    other_instructions = MySQLdb.escape_string(request.form['otherInstructions'])

    query = ("INSERT INTO PickupRecord "
             "(name, streetNumber, streetName, neighbourhood, phoneNumber, pickupDate, moneyLocation, otherInstructions, dateSubmitted) "
             "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, NOW())")

    args = (name, street_number, street_name, neighbourhood, phone, pickup_date, payment, other_instructions)

    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(query, args)

    conn.commit()
    cursor.close()
    conn.close()

    return "success"

@app.route('/api/pickupDates', methods=['GET'])
def get_pickup_dates():
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute('SELECT pickupDate FROM PickupDate where NOW() > openTime AND NOW() < closeTime')

    d = {"dates": list(cursor)}

    cursor.close()
    conn.commit()

    return jsonify(d)

@app.route('/admin/download', methods=['GET'])
@nocache
def get_pickup_records():
    # TODO: Authentication!
    query = ('SELECT * FROM PickupRecord')

    conn = mysql.connect()

    df = pd.read_sql(query, conn)

    conn.close()

    io = BytesIO()

    # Use a temp filename to keep pandas happy.
    writer = pd.ExcelWriter(io, engine='openpyxl')

    # Write the data frame to the StringIO object.
    df.to_excel(writer, sheet_name='Sheet1')
    writer.save()

    io.seek(0)

    return send_file(io, attachment_filename='pickups.xlsx', as_attachment=True)


if __name__ == "__main__":
    app.run()