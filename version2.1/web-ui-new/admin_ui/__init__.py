import os
from datetime import datetime
from flask import Flask, url_for, redirect, render_template, request
from flask_sqlalchemy import SQLAlchemy
from wtforms import form, fields, PasswordField, validators
import flask_admin as admin
import flask_login as login
from flask_admin.contrib import sqla
from flask_admin import helpers, expose
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import User


# Create Flask application
app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

login_manager = login.LoginManager()
login_manager.init_app(app)

# Create user loader function
@login_manager.user_loader
def load_user(user_id):
        return db.session.query(User).get(user_id)


from admin_ui.views import MyModelView, MyAdminIndexView


# Create admin
admin = admin.Admin(app, 'Diematic Admin', index_view=MyAdminIndexView(), base_template='my_master.html')

    
# Add view
admin.add_view(MyModelView(User, db.session))


if __name__ == '__main__':

    # Build a sample db on the fly, if one does not exist yet.
    app_dir = os.path.realpath(os.path.dirname(__file__))
    database_path = os.path.join(app_dir, app.config['DATABASE_FILE'])
    if not os.path.exists(database_path):
        print "Error: User database doesn't exist"

    # Start app
    app.run(debug=True)
