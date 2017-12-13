#!/usr/bin/env python

import web
import json
import urllib2
from datetime import date, time, datetime

VERSION='2.0'

# Web-app URL-routes
urls = (
  '/param',      'Param',
  '/controller', 'Controller',
  '/',           'Controller'
)

temp = 0
starts = 1
mydate = datetime.today()
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

# Init web.py framework
diematicReg = get_diematic_data()
app = web.application(urls, globals())
render = web.template.render('templates/', base='base')

class Param(object):

    def GET(self):
        global diematicReg
        return render.param_form(diematicReg)

    def POST(self):
        global diematicReg

        form = web.input(submit='', \
                         cons_day_a='',     cons_night_a='', \
                         cons_antiice_a='', steepness_a='', \
                         cons_day_b='',     cons_night_b='', \
                         cons_antiice_b='', steepness_b='', \
                         cons_ecs='',       cons_ecs_night='', \
                         cons_sumwin='') 
        button = form.submit
        if button != '':
          if button=='Set Time':
            print "setting time..."
            # set_time()

          elif button=='Confirm Temp':
            print "setting Circuit A/B temperatures ..."
            #setTemp_A( float(form.cons_day_a), float(form.cons_night_a), float(form.cons_antiice_a) )
            #setTemp_B( float(form.cons_day_b), float(form.cons_night_b), float(form.cons_antiice_b) )

          elif button=='Confirm Steepness':
            print "setting steepness A/B ..."
            #setSteepness( float(form.steepness_a), float(form.steepness_b) )

          elif button=='Confirm WW Temp':
            print "setting WW temperatures ..."
            #setEcsTemp( float(form.cons_ecs),    float(form.cons_ecs_night) )
          elif button=='Confirm Sum/Win Temp':
            print "setting WW temperatures ..."
            #setSumWinTemp( float(form.cons_sumwin) )
          else:
            print "fetching data from diematic..."
            
          diematicReg = get_diematic_data()

        return render.param_form(diematicReg)

class Controller(object):

    def GET(self):
        global diematicReg

        return render.ctrl_form(diematicReg)

    def POST(self):
        global diematicReg

        form = web.input(submit='', mode_heating='', mode_ecs='')
        button = form.submit
        if button=='Refresh':
          print "fetching data from diematic ..."
          diematicReg = get_diematic_data()
        elif button=='OK':
          print "setting Modes ... (currently not implemented)"
        return render.ctrl_form(diematicReg)


if __name__ == "__main__":
    diematicReg = get_diematic_data()
    app.run()
