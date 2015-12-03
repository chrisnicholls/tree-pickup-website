from flask import Flask, request, jsonify
from flaskext.mysql import MySQL
import MySQLdb

mysql = MySQL()
app = Flask(__name__, static_url_path='', static_folder='dist')
app.config.from_pyfile('config.py')
mysql.init_app(app)

@app.route('/')
def index():
    return app.send_static_file('index.html')

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


if __name__ == "__main__":
    app.run()