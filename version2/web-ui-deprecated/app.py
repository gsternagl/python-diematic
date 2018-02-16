#!/usr/bin/env python
from flask import Flask, render_template, request
import json
import urllib2
import datetime
from wtforms import Form, BooleanField, StringField, DecimalField, \
                    DateTimeField, SelectField, validators

VERSION='2.0'
REG_VAL=4

app    = Flask(__name__)
app.secret_key = 'development_key'

temp   = 0
starts = 1
mydate = datetime.date.today()

API_SERVER = 'http://127.0.0.1:5000'

# get Diematic register content from API-server (json-format)
def get_diematic_data():

    s = API_SERVER + '/registers'
    request = urllib2.Request(s)
    request.add_header('Content-Type', 'application/json')

    try:
        response = urllib2.urlopen(request, timeout=10)
        resp_str = response.read()
    except:
        print "problem reading from URL"
        return {}

    # print "response str=", resp_str

    if len(resp_str) > 0:
        try:
            data = json.loads(resp_str)
            print "got data"
        except:
            print "error decoding data"
            return {}

        if data is not None and data != {}:
            return data
        else:
            print "couldn't read proper data"
            return {}
    else:
        print "no proper response"
        return {}

class ParameterForm(Form):
    date = DateTimeField('Date',  format='%d/%m/%Y')
    cons_day_a     = DecimalField('Temp Day A', default=0.0)
    cons_day_b     = DecimalField('Temp Day B', default=0.0)
    cons_night_a   = DecimalField('Temp Night A', default=0.0)
    cons_night_b   = DecimalField('Temp Night B', default=0.0)
    cons_antiice_a = DecimalField('Temp Anti-Ice A', default=0.0)
    cons_antiice_b = DecimalField('Temp Anti-Ice B', default=0.0)
    steepness_a    = DecimalField('Steepness A', default=0.0)
    steepness_b    = DecimalField('Steepness B', default=0.0)
    cons_sumwin    = DecimalField('Temp Sum/Win', default=0.0)
    cons_ecs       = DecimalField('Temp WW Day', default=0.0)
    cons_ecs_night = DecimalField('Temp WW Night', default=0.0)

class ControllerForm(Form):
    global diematicReg

    weekdays = [('1', 'Monday'), ('2', 'Tuesday'), ('3', 'Wednesday'),\
                ('4', 'Thursday'), ('5', 'Friday'), ('6', 'Saturday'), \
                ('7', 'Sunday') ]
    weekday     = SelectField  ('Weekday', choices = weekdays)
    date        = DateTimeField('Date',  format='%d/%m/%Y')
    time        = DateTimeField('Time',  format='%H:%M')
    temp_ext    = DecimalField('Temp Outside', default=0.0, render_kw={'readonly': True})
    temp_ecs    = DecimalField('Temp WW', default=0.0, render_kw={'readonly': True})
    temp_boiler = DecimalField('Temp Boiler', default=0.0, render_kw={'readonly': True})
    anti_ice    = DecimalField('Duration Anti-ice', default=0.0)
    modes_heat  = SelectField ('Mode Heating', choices=[('1', 'AUTO'), \
                                                        ('2', 'ANTI-ICE'), \
                                                        ('3', 'PERM NIGHT'),\
                                                        ('4', 'PERM DAY'), \
                                                        ('5', 'DEROG NIGHT'),\
                                                        ('6', 'DEROG DAY') ])

    modes_ecs  = SelectField('Mode Warmwater', choices=[('1', 'AUTO'), \
                                                        ('2', 'PERM DAY'), \
                                                        ('3', 'PERM NIGHT') ])

@app.route('/param', methods=['GET', 'POST'])
def param():
    global diematicReg

    date_p = datetime.date(year=2000+int(diematicReg['YEAR'][REG_VAL]), \
                month=int(diematicReg['MONTH'][REG_VAL]), \
                day = int(diematicReg['DAY'][REG_VAL]) )
    c_da_p =  float(diematicReg['CONS_DAY_A'][REG_VAL])
    c_db_p =  float(diematicReg['CONS_DAY_B'][REG_VAL])
    c_na_p =  float(diematicReg['CONS_NIGHT_A'][REG_VAL])
    c_nb_p =  float(diematicReg['CONS_NIGHT_B'][REG_VAL])
    c_aa_p =  float(diematicReg['CONS_ANTIICE_A'][REG_VAL])
    c_ab_p =  float(diematicReg['CONS_ANTIICE_B'][REG_VAL])
    c_sa_p =  float(diematicReg['STEEPNESS_A'][REG_VAL])
    c_sb_p =  float(diematicReg['STEEPNESS_B'][REG_VAL])
    t_sum_p = float(diematicReg['CONS_SUMWIN'][REG_VAL])
    c_ed_p =  float(diematicReg['CONS_ECS'][REG_VAL])
    c_en_p =  float(diematicReg['CONS_ECS_NIGHT'][REG_VAL])

    form = ParameterForm(request.form, date=date_p, \
                           cons_day_a=c_da_p, cons_day_b=c_db_p, \
                           cons_night_a=c_na_p, cons_night_b=c_nb_p, \
                           cons_antiice_a=c_aa_p, cons_antiice_b=c_ab_p, \
                           steepness_a=c_sa_p, steepness_b=c_sb_p, \
                           cons_sumwin=t_sum_p, cons_ecs=c_ed_p, \
                           cons_ecs_night=c_en_p)

    return render_template('param_page.html', form=form, data=diematicReg)

@app.route('/', methods=['GET', 'POST'])
def ctrl():
    global diematicReg

    date_p = datetime.date(year  = 2000+int(diematicReg['YEAR'][REG_VAL]), \
                           month = int(diematicReg['MONTH'][REG_VAL]), \
                           day   = int(diematicReg['DAY'][REG_VAL]) )
    time_p = datetime.time(hour  = int(diematicReg['HOUR'][REG_VAL]), \
                           minute= int(diematicReg['MINUTE'][REG_VAL]) )
    t_e_p = float(diematicReg['TEMP_EXT'][REG_VAL])
    t_w_p = float(diematicReg['TEMP_ECS'][REG_VAL])
    t_b_p = float(diematicReg['TEMP_BOILER'][REG_VAL])
    t_a_p = float(diematicReg['NB_DAY_ANTIICE'][REG_VAL])

    form = ControllerForm(request.form, date=date_p, time=time_p, \
                          temp_ext=t_e_p, temp_ecs=t_w_p, \
                          temp_boiler=t_b_p, anti_ice=t_a_p)

    if request.method == 'POST' and form.validate():
        # do nothing
        print "OK"

    return render_template('ctrl_page.html', form=form, data=diematicReg)

if __name__ == "__main__":
    diematicReg = get_diematic_data()
    app.run(host='0.0.0.0', port=8080, debug=True)
