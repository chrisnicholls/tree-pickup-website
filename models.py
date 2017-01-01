import hashlib
import base64
from Crypto import Random
from Crypto.Cipher import AES
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class PickupDate(db.Model):
    __tablename__ = 'pickup_date'
    id = db.Column('pickupDateId', db.Integer, primary_key=True, autoincrement=True)
    date = db.Column('pickupDate', db.String(40), nullable=False)
    open_time = db.Column('openTime', db.DateTime, nullable=False)
    close_time = db.Column('closeTime', db.DateTime, nullable=False)

    def __init__(self, date, open_time, close_time):
        self.date = date
        self.open_time = open_time
        self.close_time = close_time


class PickupRecord(db.Model):
    __tablename__ = 'pickup_record'
    id = db.Column('pickupRecordId', db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email_address = db.Column('emailAddress', db.String(120))
    street_number = db.Column('streetNumber', db.String(45), nullable=False)
    street_name = db.Column('streetName', db.String(120), nullable=False)
    neighbourhood = db.Column(db.String(80))
    phone_number = db.Column(db.String(15))
    pickup_date = db.Column('pickupDate', db.String(40), nullable=False)
    money_location = db.Column('moneyLocation', db.String(120), nullable=False)
    other_instructions = db.Column('otherInstructions', db.String(120))
    date_submitted = db.Column('dateSubmitted', db.DateTime, nullable=False)
    source = db.Column(db.String(32), nullable=False, default='web')
    lat = db.Column(db.Float, nullable=True)
    lng = db.Column(db.Float, nullable=True)
    geocode_address = db.Column(db.String(120), nullable=True)

    def __init__(self, name, email_address, street_number, street_name, neighbourhood, phone_number,
                 pickup_date, money_location, other_instructions, date_submitted, source, lat=None,
                 lng=None, geocode_address=None):
            self.name = name
            self.email_address = email_address
            self.street_number = street_number
            self.street_name = street_name
            self.neighbourhood = neighbourhood
            self.phone_number = phone_number
            self.pickup_date = pickup_date
            self.money_location = money_location
            self.other_instructions = other_instructions
            self.date_submitted = date_submitted
            self.source = source
            self.lat = lat
            self.lng = lng
            self.geocode_address = geocode_address


class User(db.Model):
    __tablename__ = 'admin_user'
    id = db.Column('userId', db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column('emailAddress', db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(1024))

    def __init__(self, user_id):
        self.id = user_id

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password

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
    def valid_user(cls, email_address, hashed_password, encryption_key, salt):
        users = User.query.filter(User.email == email_address)

        for user in users:
            password = AESCipher(encryption_key).decrypt(user.password)

            print "decrypted password = %s" % password

            m = hashlib.md5()
            m.update(password)
            m.update(salt)
            expected_hash = m.hexdigest()

            print("hashed_password=%s" % hashed_password)
            print("expected_hash=  %s" % expected_hash)

            if hashed_password == expected_hash:
                return user

        return None


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

