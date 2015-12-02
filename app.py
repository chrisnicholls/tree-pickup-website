from flask import Flask, request, jsonify
from flaskext.mysql import MySQL
import MySQLdb

mysql = MySQL()
app = Flask(__name__, static_url_path='', static_folder='dist')
app.config['MYSQL_DATABASE_USER'] = 'user'
app.config['MYSQL_DATABASE_PASSWORD'] = 'pass'
app.config['MYSQL_DATABASE_DB'] = 'PickupRecord'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/api/hello')
def hello():
    return "Hello World!"

@app.route('/api/pickup', methods=['POST'])
def new_record():
    name = MySQLdb.escape_string(request.form['name'])
    print name
    print request.form
    return "success"

@app.route('/api/pickupDates', methods=['GET'])
def get_pickup_dates():
    # TODO: fetch these from the DB
    d = {'dates': ['January 2, 2016', 'January 9, 2016']}
    return jsonify(d)


if __name__ == "__main__":
    app.run()