"""forms.py the main module with the definition of the Flask Forms."""
from __future__ import print_function
from flask_wtf import FlaskForm as Form
from wtforms import StringField, DecimalField, IntegerField, \
                    DateField, SelectField, SubmitField, PasswordField, \
                    BooleanField, validators
from wtforms.validators import ValidationError


class SettingsForm(Form):
    """This Form contains all the app settings."""
    influxdb_host = StringField('InfluxDB hostname/IP-address')
    influxdb_port = IntegerField('InfluxDB portnumber')
    influxdb_db = StringField('InfluxDB database name')
    influxdb_table = StringField('InfluxDB table name')
    influxdb_user = StringField('InfluxDB user name')
    influxdb_pw = StringField('InfluxDB password')

    diematicd_host = StringField('DiematicD hostname/IP-address')
    diematicd_port = IntegerField('DiematicD portnumber')
    submit_button = SubmitField('Submit')

class ControllerForm(Form):
    """This Form displays all Diematic III controller parameters."""
    ctrl_date = DateField('Diematic-Date', format='%d.%m.%Y', render_kw={'readonly': True})
    ctrl_time = StringField('Diematic-Time', render_kw={'readonly': True})
    ctrl_weekday = IntegerField('Weekday', render_kw={'readonly': True})
    temp_outside = DecimalField('Temp-Outside', render_kw={'readonly': True})
    temp_ecs_meas = DecimalField('Temp Water measured', render_kw={'readonly': True})
    temp_boiler_meas = DecimalField('Temp Boiler measured', render_kw={'readonly': True})
    temp_boiler_calc = DecimalField('Temp Boiler calculated', render_kw={'readonly': True})
    mode_heating = SelectField(
        'Mode Heating',
        coerce=int,
        choices=[
            (0, 'ANTI-ICE'),
            (1, 'PERM-NIGHT'),
            (2, 'PERM-DAY'),
            (3, 'AUTO'),
            (4, 'DEROG-NIGHT'),
            (5, 'DEROG-DAY')
        ],
        default=3
    )
    mode_ecs = SelectField(
        'Mode Warmwater',
        coerce=int,
        choices=[
            (0, 'AUTO'),
            (1, 'PERM'),
            (2, 'TEMP')],
        default=0
    )
    refresh_button = SubmitField('Refresh')
    submit_button = SubmitField('Submit')

def validate_time(form, field):
    """help function which validates time field inputs."""
    buff = field.data
    if len(buff) == 5:
        if buff[2] == ':' and \
           buff[0] in '012' and \
           buff[1] in '0123456789' and \
           buff[3] in '012345' and \
           buff[4] in '0123456789':
            hour = int(buff[0])*10 + int(buff[1])
            minute = int(buff[3])*10 + int(buff[4])
            if hour < 24 and minute < 60:
                pass
            else:
                raise ValidationError('Time field must be in the form ' + \
                                      'HH:MM, H=00..23, MM=00..59')
        else:
            raise ValidationError('Time field must be in the form ' + \
                                  'HH:MM, H=00..23, MM=00..59')
    else:
        raise ValidationError('Time field must be in the form ' + \
                              'HH:MM, H=00..23, MM=00..59')

class ChartForm(Form):
    """The Form which contains the temperature charts."""
    graph_type = SelectField(
        'Select Timespan',
        choices=[(0, 'last hour'),
                 (1, 'last 2 hours'),
                 (2, 'last 6 hours'),
                 (3, 'last 12 hours'),
                 (4, 'last 24 hours'),
                 (5, 'last week')],
        default=1
    )
    graph_gaps = BooleanField('Show Gaps')
    burner_starts1 = DecimalField('Burner Starts in period')
    burner_starts2 = DecimalField('Burner Starts per hour')

    submit_button = SubmitField('Refresh')

class ParameterForm(Form):
    """All known Diematic III parameters can be display/changed here."""
    ctrl_date = DateField('Diematic-Date', format='%d.%m.%Y')
    ctrl_time = StringField('Diematic-Time', [validate_time])
    ctrl_weekday = IntegerField(
        'Weekday',
        [validators.NumberRange(min=0, max=7)]
    )

    # Submit Buttons for setting temperatures
    set_time = SubmitField('Set Time')
    sync_time = SubmitField('Sync Time to now')

    # Section Temperature Circuit A
    temp_a_day = DecimalField(
        'Temp Day',
        [
            validators.Required(),
            validators.NumberRange(min=10.0, max=30.0)
        ],
        places=1,
    )
    temp_a_night = DecimalField(
        'Temp Night',
        [
            validators.Required(),
            validators.NumberRange(min=5.0, max=30.0)
        ],
        places=1,
    )
    temp_a_antiice = DecimalField(
        'Temp Anti-Ice',
        [
            validators.Required(),
            validators.NumberRange(min=5.0, max=20.0)
        ],
        places=1,
    )
    # Section Temperature Circuit B
    temp_b_day = DecimalField(
        'Temp Day',
        [
            validators.Required(),
            validators.NumberRange(min=10.0, max=30.0)
        ],
        places=1,
    )
    temp_b_night = DecimalField(
        'Temp Night',
        [
            validators.Required(),
            validators.NumberRange(min=5.0, max=30.0)
        ],
        places=1,
    )
    temp_b_antiice = DecimalField(
        'Temp Anti-Ice',
        [
            validators.Required(),
            validators.NumberRange(min=5.0, max=20.0)
        ],
        places=1,
    )

    # Submit Button for setting temperatures
    set_temp = SubmitField('Set Temperatures')

    # Section Heating Steepness Circuit A/B
    steepness_a = DecimalField(
        'Steepness Factor A',
        [
            validators.Required(),
            validators.NumberRange(min=0.0, max=4.0)
        ],
        places=1,
    )

    steepness_b = DecimalField(
        'Steepness Factor B',
        [
            validators.Required(),
            validators.NumberRange(min=0.0, max=4.0)
        ],
        places=1,
    )

    # Submit Button for setting steepness
    set_steepness = SubmitField('Set Steepness')

    # Section Summer/Winter Auto Temp
    temp_sum_win = DecimalField(
        'Temp Summer/Winter',
        [
            validators.Required(),
            validators.NumberRange(min=15.0, max=30.5)
        ],
        places=1,
    )
    set_sumwin = SubmitField('Set Sum/Win Temp')

    # Section Warmwater
    temp_ecs_day = DecimalField(
        'Temp Day',
        [
            validators.Required(),
            validators.NumberRange(min=10.0, max=80.0)
        ],
        places=1,
    )
    temp_ecs_night = DecimalField(
        'Temp Night',
        [
            validators.Required(),
            validators.NumberRange(min=10.0, max=80.0)
        ],
        places=1,
    )

    # Buttons
    set_ecs = SubmitField('Set Warmwater Temp')

    temp_boiler_min = DecimalField(
        'Boiler Minimum',
        [
            validators.Required(),
            validators.NumberRange(min=30.0, max=50.0)
        ],
        places=1,
    )
    temp_boiler_max = DecimalField(
        'Boiler Maximum',
        [
            validators.Required(),
            validators.NumberRange(min=50.0, max=90.0)
        ],
        places=1,
    )

    # Buttons
    set_boiler = SubmitField('Set Boiler Temp')

    refresh_button = SubmitField('Refresh')

class RegistrationForm(Form):
    """The user registration Form."""
    login = StringField(
        'Username', [
            validators.Required(),
            validators.Length(min=4, max=20)
        ]
    )
    password = PasswordField(
        'New Password', [
            validators.Length(min=8, max=20)
        ]
    )
    confirm = PasswordField(
        'Repeat Password', [
            validators.Required(),
            validators.EqualTo('password', message='Passwords must match')
        ]
    )
    email = StringField('Email', [validators.Length(max=30)])

class LoginForm(Form):
    """The Login Form."""
    login = StringField(
        'Username', [
            validators.Required(),
            validators.Length(min=4, max=20)
        ]
    )
    password = PasswordField(
        'New Password', [
            validators.Length(min=8, max=20)
        ]
    )
