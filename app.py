from flask import Flask, request, jsonify, send_file, make_response, redirect, flash
from flaskext.mysql import MySQL
from flask.ext.login import LoginManager, login_required, login_user
import pandas as pd
import MySQLdb
from io import BytesIO
from functools import wraps, update_wrapper
from datetime import datetime
import os
import hashlib
import base64
from Crypto import Random
from Crypto.Cipher import AES

mysql = MySQL()
app = Flask(__name__, static_url_path='', static_folder='dist')
app.config.from_pyfile('config.py')
app.secret_key = os.urandom(24)

app.debug = True
login_manager = LoginManager()

mysql.init_app(app)
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)


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

        print request.form
        user = User.valid_user(request.form['email'], request.form['password'], request.form['s'])
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
    name = MySQLdb.escape_string(request.form['name'])
    street_number = MySQLdb.escape_string(request.form['streetNumber'])
    street_name = MySQLdb.escape_string(request.form['streetName'])
    phone = MySQLdb.escape_string(request.form['phone'])
    neighbourhood = MySQLdb.escape_string(request.form['neighbourhood'])
    pickup_date = MySQLdb.escape_string(request.form['pickupDate'])
    payment = MySQLdb.escape_string(request.form['payment'])
    other_instructions = MySQLdb.escape_string(request.form['otherInstructions'])
    email_address = MySQLdb.escape_string(request.form['email'])

    query = ("INSERT INTO PickupRecord "
             "(name, streetNumber, streetName, neighbourhood, phoneNumber, pickupDate, moneyLocation, otherInstructions, emailAddress, dateSubmitted) "
             "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, NOW())")

    args = (name, street_number, street_name, neighbourhood, phone, pickup_date, payment, other_instructions, email_address)

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
@login_required
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


class User():
    id = None

    def __init__(self, user_id):
        self.id = user_id

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.id)  # python 2
        except NameError:
            return str(self.id)  # python 3

    def __repr__(self):
        return '<User %r>' % (self.id)

    @classmethod
    def get(cls, user_id):
        sql = "select userId from User where userId=%s"
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute(sql, [int(user_id)])

        user = None

        for row in cursor.fetchall():
            user = User(row[0])

        cursor.close()
        conn.close()

        return user

    @classmethod
    def valid_user(cls, email_address, hashed_password, salt):
        sql = "select userId,password from User where emailAddress=%s"

        conn = mysql.connect()
        cursor = conn.cursor()

        escaped = MySQLdb.escape_string(email_address)
        cursor.execute(sql, [escaped])

        user = None

        for row in cursor.fetchall():
            user_id = row[0]
            password = AESCipher(app.config['ENCRYPTION_KEY']).decrypt(row[1])

            print "decrypted password = %s" % password

            m = hashlib.md5()
            m.update(password)
            m.update(salt)
            expected_hash = m.hexdigest()

            print("hashed_password=%s" % hashed_password)
            print("expected_hash=  %s" % expected_hash)

            if hashed_password == expected_hash:
                user = User(user_id)

        cursor.close()
        conn.close()

        return user


class AESCipher(object):

    def __init__(self, key):
        self.bs = 32
        self.key = hashlib.sha256(key.encode()).digest()

    def encrypt(self, raw):
        raw = self._pad(raw)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return base64.b64encode(iv + cipher.encrypt(raw))

    def decrypt(self, enc):
        enc = base64.b64decode(enc)
        iv = enc[:AES.block_size]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return self._unpad(cipher.decrypt(enc[AES.block_size:])).decode('utf-8')

    def _pad(self, s):
        return s + (self.bs - len(s) % self.bs) * chr(self.bs - len(s) % self.bs)

    @staticmethod
    def _unpad(s):
        return s[:-ord(s[len(s)-1:])]

if __name__ == "__main__":
    app.run()