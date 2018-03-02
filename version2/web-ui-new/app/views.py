"""views.py module."""
from __future__ import print_function
from datetime import datetime, timedelta
from time import sleep

from werkzeug.datastructures import MultiDict
from werkzeug.security import check_password_hash

from flask_login import login_user, login_required, logout_user, current_user
from flask import request, flash, url_for, redirect, \
     render_template, session, g as global_buffer


import numpy as np
import peakutils

from app import app, db, login_manager, params
from .parameter import Parameters
from .charts import Chart

from .models import User
from .forms import LoginForm, RegistrationForm, ControllerForm, \
                   ChartForm, ParameterForm, SettingsForm
from .settings import MySettings

timespans = ['1h', '2h', '6h', '12h', '1d', '7d']
hourtable = {'1h': 1, '2h': 2, '6h': 6, '12h': 12, '1d': 24, '7d': 24*7}

# global variables to remember last mask setting in ChartForm
show_gaps = False
timespan = '1h'

def display_form_errors(form):
    """helper function which display form field errors."""

    for fieldname, errors in form.errors.items():
        for error in errors:
            err_str = 'Error in field <' + fieldname + '>: ' + error
            flash(err_str, 'error')


@login_manager.user_loader
def load_user(user_id):
    """helper function for user authentication."""

    return User.query.get(int(user_id))


@app.before_request
def before_request():
    """helper function for session mgmt."""

    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=5)
    session.modified = True
    global_buffer.user = current_user

#@app.route('/register', methods=['GET', 'POST'])
#def register():
#    form = RegistrationForm(request.form)
#    if request.method == 'POST':
#        if form.validate():
#            existing_user = User.query.filter_by(login=form.login.data).first()
#            if existing_user is None:
#                hashpass = generate_password_hash(form.password.data, method='sha256')
#                user = User(form.login.data, hashpass, form.email.data)
#                db.session.add(user)
#                db.session.commit()
#                login_user(user)
#                flash('user registered and logged in', 'warning')
#            else:
#                flash('user already exists!', 'error')
#                return redirect(url_for('register'))
#        else:
#            display_form_errors(form)
#    return render_template('register.html', form=form)


@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    """check and log user in."""

    if current_user.is_authenticated == True:
        return redirect(url_for('controller'))

    form = LoginForm(request.form)
    if request.method == 'POST'and form.validate():
        check_user = User.query.filter_by(login=form.login.data).first()
        if check_user:
            if check_password_hash(check_user.password, form.password.data):
                login_user(check_user)
                return redirect(url_for('controller'))

    return render_template('login.html', form=form)


@app.route('/logout', methods=['GET'])
@login_required
def logout():
    """log the user out."""

    logout_user()
    return redirect(url_for('login'))

@app.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    """settings route => Start the settings view."""

    mysettings = MySettings(app)
    form = SettingsForm(request.form, obj=mysettings)

    if request.method == 'POST' and form.validate():
        mysettings.update(
            app,
            form.influxdb_host.data,
            form.influxdb_port.data,
            form.influxdb_db.data,
            form.influxdb_table.data,
            form.influxdb_user.data,
            form.influxdb_pw.data,
            form.diematicd_host.data,
            form.diematicd_port.data
        )
        return redirect(url_for('controller'))

    return render_template('settings.html', form=form, user=current_user)

@app.route('/charts', methods=['GET', 'POST'])
@login_required
def charts():
    """charts route => start charts form."""

    global show_gaps
    global timespan

    form = ChartForm(
        request.form,
        graph_type=timespans.index(timespan),
        graph_gaps=show_gaps
    )

    if request.method == 'POST':
        if form.submit_button.data:
            timespan = timespans[int(form.graph_type.data)]
            show_gaps = form.graph_gaps.data
        else:
            flash('Unknown Event', 'error')

    chart = Chart(app)
    data_values1, data_values2, data_values3, data_labels = \
        chart.get_data(timespan, show_gaps)

    cb = np.array(data_values3)
    peaks = peakutils.indexes(cb, thres=0.02 / max(cb), min_dist=5)

    starts_total = len(peaks)
    starts_per_h = int(round(float(starts_total) / \
                             float(hourtable[timespan]), 0))

    return render_template(
        'charts.html',
        form=form,
        user=current_user,
        values1=data_values1,
        values2=data_values2,
        values3=data_values3,
        labels=data_labels,
        burner_total=starts_total,
        burner_ph=starts_per_h,
    )

@app.route('/controller', methods=['GET', 'POST'])
@login_required
def controller():
    """controller route => start the controller form."""

    params.update()

    form = ControllerForm(
        request.form,
        obj=params
    )
    if request.method == 'POST' and form.validate():
        if form.submit_button.data:
            print("mode_heating=" + form.mode_heating.data)
            print("mode_ecs=" + form.mode_ecs.data)
            flash('Data posted')
        elif form.refresh_button.data:
            # enforce to reload the form by redirect and call 'GET' requests
            return redirect(url_for('controller'))
        else:
            display_form_errors(form)

    return render_template('controller.html', form=form, user=current_user)


@app.route('/parameters', methods=['GET', 'POST'])
@login_required
def parameters():
    """parameters route => start parameters form."""

    params.update()
    # print('reached params.update')

    form = ParameterForm(
        request.form,
        obj=params
    )

    if request.method == 'POST' and form.validate():
        if form.sync_time.data:
            params.ctrl_date = datetime.now()
            params.ctrl_time = datetime.today().strftime('%H:%M')
            params.ctrl_weekday = datetime.today().isoweekday()
            form.ctrl_date.process(
                MultiDict(
                    [('ctrl_date', params.ctrl_date.strftime(form.ctrl_date.format))]
                )
            )
            form.ctrl_time.process_data(params.ctrl_time)
            form.ctrl_weekday.process(
                MultiDict(
                    [('ctrl_weekday', params.ctrl_weekday)]
                )
            )
            params.ctrl_date = form.ctrl_date.data
            params.ctrl_time = form.ctrl_time.data
            params.weekday = form.ctrl_weekday.data
            params.set_datetime()
            flash('Time synched')

        elif form.set_time.data:
            params.ctrl_date = form.ctrl_date.data
            params.ctrl_time = form.ctrl_time.data
            params.weekday = form.ctrl_weekday.data
            params.set_datetime()
            flash('set time called')

        elif form.set_temp.data:
            params.temp_a_day = form.temp_a_day.data
            params.temp_a_night = form.temp_a_night.data
            params.temp_a_antiice = form.temp_a_antiice.data

            params.temp_b_day = form.temp_b_day.data
            params.temp_b_night = form.temp_b_night.data
            params.temp_b_antiice = form.temp_b_antiice.data
            params.set_temp_heating()
            flash('set temperatures called')

        elif form.set_steepness.data:
            params.steepness_a = form.steepness_a.data
            params.steepness_b = form.steepness_b.data
            params.set_steepness()
            flash('set steepness called')

        elif form.set_sumwin.data:
            params.temp_sum_win = form.temp_sum_win.data
            params.set_temp_sumwin()
            flash('set sum/win temp')

        elif form.set_ecs.data:
            params.temp_ecs_day = form.temp_ecs_day.data
            params.temp_ecs_night = form.temp_ecs_night.data
            params.set_temp_ecs()
            flash('set warmwater temp')

        elif form.set_boiler.data:
            params.temp_boiler_min = form.temp_boiler_min.data
            params.temp_boiler_min = form.temp_boiler_min.data
            params.set_temp_boiler()
            flash('set boiler temp')

        elif form.refresh_button.data:
            # enforce to reload the form by redirect and call 'GET' requests
            return redirect(url_for('parameters'))
        else:
            flash('whats going on here', 'error')
    else:
        display_form_errors(form)

    return render_template('parameters.html', form=form, params=params, user=current_user)
