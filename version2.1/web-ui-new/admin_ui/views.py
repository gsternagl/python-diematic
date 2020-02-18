from datetime import datetime
from flask import url_for, redirect, render_template, request
import flask_admin as admin
import flask_login as login
from flask_admin.contrib import sqla
from flask_admin import helpers, expose
from werkzeug.security import generate_password_hash, check_password_hash
from wtforms import PasswordField, validators
from app.models import User
from admin_ui import app, db, login_manager
from .forms import LoginForm, RegistrationForm


# Create customized model view class
class MyModelView(sqla.ModelView):
    column_exclude_list = ('registered_on', 'password')
    form_excluded_columns = ('registered_on', 'password')

    def is_accessible(self):
        return login.current_user.is_authenticated

    def scaffold_form(self):
        form_class = super(MyModelView, self).scaffold_form()

        form_class.password2 = PasswordField(
            'New Password',
            [validators.DataRequired(), \
             validators.EqualTo('confirm', message='Passwords must match')]
        )
        form_class.confirm = PasswordField('Confirm Password')
        
        return form_class

    def on_model_change(self, form, model, is_created):

        if len(model.password2):
            model.password = generate_password_hash(model.password2, 
                                                    method='sha256')



# Create customized index view class that handles login & registration
class MyAdminIndexView(admin.AdminIndexView):

    @expose('/')
    def index(self):
        if not login.current_user.is_authenticated:
            return redirect(url_for('.login_view'))
        return super(MyAdminIndexView, self).index()

    @expose('/login/', methods=('GET', 'POST'))
    def login_view(self):
        # handle user login
        form = LoginForm(request.form)
        if helpers.validate_form_on_submit(form):
            user = form.get_user()
            login.login_user(user)

        if login.current_user.is_authenticated:
            return redirect(url_for('.index'))
        link = '<p>Don\'t have an account? <a href="' + url_for('.register_view') + '">Click here to register.</a></p>'
        self._template_args['form'] = form
        self._template_args['link'] = link
        return super(MyAdminIndexView, self).index()

    @expose('/register/', methods=('GET', 'POST'))
    def register_view(self):
        form = RegistrationForm(request.form)
        if helpers.validate_form_on_submit(form):
            user = User()

            form.populate_obj(user)
            # we hash the users password to avoid saving it as plaintext in the db,
            # remove to use plain text:
            user.password = generate_password_hash(form.password.data, 
                                                   method='sha256')
            user.registered_on = datetime.utcnow()

            db.session.add(user)
            db.session.commit()

            login.login_user(user)
            return redirect(url_for('.index'))
        link = '<p>Already have an account? <a href="' + url_for('.login_view') + '">Click here to log in.</a></p>'
        self._template_args['form'] = form
        self._template_args['link'] = link
        return super(MyAdminIndexView, self).index()

    @expose('/logout/')
    def logout_view(self):
        login.logout_user()
        return redirect(url_for('.index'))


# Flask views
@app.route('/')
def index():
    return render_template('index.html')
