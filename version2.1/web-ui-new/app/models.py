from datetime import datetime
from app import db

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column('user_id', db.Integer, primary_key=True)
    login = db.Column('login', db.String(20), unique=True, 
                      index=True, nullable=False)
    email = db.Column(db.String(30), nullable=False)
    password = db.Column(db.String, nullable=False)
    registered_on = db.Column('registered_on', db.DateTime)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    def __repr__(self):
        return '<User %r>' % (self.login)

    def __unicode__(self):
        return self.login
