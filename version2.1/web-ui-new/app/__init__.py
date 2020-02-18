"""This is the main file for the diematic web ui."""
from datetime import datetime, timedelta
from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
import config
from .parameter import Parameters

app = Flask(__name__)
Bootstrap(app)

app.config.from_object('config')
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@app.before_request
def make_session_permanent():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=5)

params = Parameters(
    diematic_url='http://{}:{}/registers'.format(
        app.config['DIEMATICD_HOST'],
        app.config['DIEMATICD_PORT']
    ),
    ctrl_date=datetime.today(),   # this is currently mapped to DateField
    ctrl_time=datetime.today().strftime('%H:%M'),
    ctrl_weekday=datetime.today().isoweekday(),
    temp_a_day=21.0,
    temp_a_night=18.0,
    temp_a_antiice=6.0,
    temp_b_day=21.0,
    temp_b_night=18.0,
    temp_b_antiice=6.0,
    steepness_a=1.7,
    steepness_b=2.0,
    temp_sum_win=15.0,
    temp_ecs_day=45.0,
    temp_ecs_night=40.0,
    temp_outside=0.0,
    temp_ecs_meas=55.0,
    temp_boiler_meas=81.0,
    temp_boiler_calc=82.0,
    temp_boiler_min=30.0,
    temp_boiler_max=80.0,
    mode_heating=3,   # value idx 3 in select field list = AUTO
    mode_ecs=0,   # value idx 0 in select field list = AUTO
)

if app.config['DIEMATICD_EMULATION']:
    params.emulate_on()

from app import views, models

if __name__ == '__main__':
    app.run(port=5001, debug=app.config['DEBUG'])
