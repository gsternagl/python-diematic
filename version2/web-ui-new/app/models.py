from app import db

class User(db.Model):
    __tablename__ = 'users'
    id       = db.Column('user_id', db.Integer, primary_key=True)
    username = db.Column('username', db.String(20), unique=True, index=True)
    email    = db.Column(db.String(30), nullable=False)
    password = db.Column(db.String, nullable=False)
    registered_on = db.Column('registered_on', db.DateTime)

    def __init__(self, username, password, email):
        self.username = username
        self.email    = email
        self.password = password
        self.registered_on = datetime.utcnow()
        print "user created"

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

    def __repr__(self):
        return '<User %r>' % (self.username)
