#!/usr/bin/env python

import web
from datetime import date, time, datetime
from Diematic import Diematic

VERSION='0.9'

urls = (
  '/param',      'Param',
  '/controller', 'Controller',
  '/',           'Controller'
)

temp=0
starts=0
mydate=datetime.today()
connection = { 'type': 'socket', \
               'device': '/dev/ttyAMA0', \
               'baudrate': 9600, \
               'ip_addr': '192.168.178.160', 'ip_port': 20108 }

# Init the Diematic controller connection any synch data

# Init web.py framework
app = web.application(urls, globals())
render = web.template.render('templates/', base='base')
regulator = Diematic(connection, debug=False)
regulator.synchro()

class Param(object):

    def GET(self):
        return render.param_form(regulator.diematicReg)

    def POST(self):
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
            regulator.setTime()

          elif button=='Confirm Temp':
            print "setting Circuit A/B temperatures ..."
            regulator.setTemp_A( float(form.cons_day_a), float(form.cons_night_a), float(form.cons_antiice_a) )
            regulator.setTemp_B( float(form.cons_day_b), float(form.cons_night_b), float(form.cons_antiice_b) )

          elif button=='Confirm Steepness':
            print "setting steepness A/B ..."
            regulator.setSteepness( float(form.steepness_a), float(form.steepness_b) )

          elif button=='Confirm WW Temp':
            print "setting WW temperatures ..."
            regulator.setEcsTemp( float(form.cons_ecs),    float(form.cons_ecs_night) )
          elif button=='Confirm Sum/Win Temp':
            print "setting WW temperatures ..."
            regulator.setSumWinTemp( float(form.cons_sumwin) )
          else:
            print "fetching data from diematic..."
            
          regulator.synchro()

        return render.param_form(regulator.diematicReg)

class Controller(object):

    def GET(self):
        return render.ctrl_form(regulator.diematicReg)

    def POST(self):
        form = web.input(submit='', mode_heating='', mode_ecs='')
        button = form.submit
        if button=='Refresh':
          print "fetching data from diematic ..."
          regulator.synchro()
        elif button=='OK':
          print "setting Modes ... (currently not implemented)"
        return render.ctrl_form(regulator.diematicReg)


if __name__ == "__main__":
    app.run()
