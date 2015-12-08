class User():
    def __init__(self, id):
        self.id = id

    def get(self, user_id):
        # TODO: implement user model
        if user_id == 1:
            return User(1)

        return None

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
        return '<User %r>' % (self.nickname)