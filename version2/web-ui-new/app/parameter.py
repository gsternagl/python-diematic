import json
import urllib
import requests
from requests import ConnectionError
from datetime import datetime, date, time


class Parameters:
    REG_VAL = 4
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}

    def __init__(self, diematic_url, \
                 ctrl_date, ctrl_time, ctrl_weekday, \
                 temp_a_day, temp_a_night, temp_a_antiice,\
                 temp_b_day, temp_b_night, temp_b_antiice, \
                 steepness_a, steepness_b, temp_sum_win, \
                 temp_ecs_day, temp_ecs_night, \
                 temp_outside, temp_ecs_meas, temp_boiler_meas, \
                 temp_boiler_calc, temp_boiler_min, temp_boiler_max, \
                 mode_ecs, mode_heating ):

        self.URL              = diematic_url
        self.emulate          = False
        self.ctrl_date        = ctrl_date
        self.ctrl_time        = ctrl_time
        self.ctrl_weekday     = ctrl_weekday
        self.temp_a_day       = temp_a_day
        self.temp_a_night     = temp_a_night
        self.temp_a_antiice   = temp_a_antiice
        self.temp_b_day       = temp_b_day
        self.temp_b_night     = temp_b_night
        self.temp_b_antiice   = temp_b_antiice
        self.steepness_a      = steepness_a
        self.steepness_b      = steepness_b
        self.temp_sum_win     = temp_sum_win
        self.temp_ecs_day     = temp_ecs_day
        self.temp_ecs_night   = temp_ecs_night
        self.temp_outside     = temp_outside
        self.temp_ecs_meas    = temp_ecs_meas
        self.temp_boiler_meas = temp_boiler_meas
        self.temp_boiler_calc = temp_boiler_calc
        self.temp_boiler_min  = temp_boiler_min
        self.temp_boiler_max  = temp_boiler_max
        self.mode_ecs         = mode_ecs
        self.mode_heating     = mode_heating

    def emulate_on(self):
        self.emulate = True

    def update(self):
        if self.emulate:
            pass
        else:
            try:
                resp = requests.get(self.URL, headers=self.headers)
            except ConnectionError:
                print("data connection to diematicd failed")
                return False

            if resp.status_code == 200:
                data = resp.json()
                if data is not None:
                    self.ctrl_date = date(
                        day   = int(data['DAY'][self.REG_VAL]),
                        month = int(data['MONTH'][self.REG_VAL]),
                        year  = 2000 + int(data['YEAR'][self.REG_VAL])
                    )
                    self.ctrl_time = '%02d:%02d' % (
                        int(data['HOUR'][self.REG_VAL]),
                        int(data['MINUTE'][self.REG_VAL])
                    )
                    self.ctrl_weekday   = int(data['WEEKDAY'][self.REG_VAL])
                    self.temp_a_day     = float(data['CONS_DAY_A'][self.REG_VAL])
                    self.temp_a_night   = float(data['CONS_NIGHT_A'][self.REG_VAL])
                    self.temp_a_antiice = float(data['CONS_ANTIICE_A'][self.REG_VAL])
                    self.steepness_a    = float(data['STEEPNESS_A'][self.REG_VAL])

                    self.temp_b_day     = float(data['CONS_DAY_B'][self.REG_VAL])
                    self.temp_b_night   = float(data['CONS_NIGHT_B'][self.REG_VAL])
                    self.temp_b_antiice = float(data['CONS_ANTIICE_B'][self.REG_VAL])
                    self.steepness_b    = float(data['STEEPNESS_B'][self.REG_VAL])

                    self.temp_ecs_day   = float(data['CONS_ECS_DAY'][self.REG_VAL])
                    self.temp_ecs_night = float(data['CONS_ECS_NIGHT'][self.REG_VAL])
                    self.temp_ecs_meas  = float(data['TEMP_ECS'][self.REG_VAL])

                    self.temp_outside   = float(data['TEMP_EXT'][self.REG_VAL])
                    self.temp_sum_win   = float(data['CONS_SUMWIN'][self.REG_VAL])

                    self.temp_boiler_calc = float(data['CONS_BOILER'][self.REG_VAL])
                    self.temp_boiler_meas = float(data['TEMP_BOILER'][self.REG_VAL])
                    self.temp_boiler_min  = float(data['MIN_BOILER'][self.REG_VAL])
                    self.temp_boiler_max  = float(data['MAX_BOILER'][self.REG_VAL])
                    return True

                else:
                    print 'error converting JSON data from diematicd'
            else:
                print 'error reading data from diematicd'

        return False


    def transmit_data(self, data):
        for reg in data:
            d = { reg: [ data[reg] ] }
            data_str = json.dumps(d, indent=4)
            if not self.emulate:
                url = self.URL + '/' + reg
                try:
                    resp = requests.post(url, data=data_str, headers=self.headers)
                    if resp.status_code != 200:
                       print 'Error: ', resp.status_code
                except:
                    print 'Error writing to diematicd'
            else:
                print 'Data=', data_str


    def set_datetime(self):
        data = {
            'DAY':    int(self.ctrl_date.day), \
            'MONTH':  int(self.ctrl_date.month), \
            'YEAR':   int(self.ctrl_date.year - 2000), \
            'HOUR':   int(self.ctrl_time[0:2]), \
            'MINUTE': int(self.ctrl_time[3:5]) \
        }
        self.transmit_data(data)
        return


    def set_temp_heating(self):
        data = {
            'CONS_DAY_A':     float(self.temp_a_day), \
            'CONS_NIGHT_A':   float(self.temp_a_night), \
            'CONS_ANTIICE_A': float(self.temp_a_antiice), \
            'CONS_DAY_B':     float(self.temp_b_day), \
            'CONS_NIGHT_B':   float(self.temp_b_night), \
            'CONS_ANTIICE_B': float(self.temp_b_antiice) \
        }
        self.transmit_data(data)
        return


    def set_temp_sumwin(self):
        data = { \
            'CONS_SUMWIN': float(self.temp_sum_win)
        }
        self.transmit_data(data)
        return


    def set_steepness(self):
        data = {
            'STEEPNESS_A': float(self.steepness_a), \
            'STEEPNESS_B': float(self.steepness_b) \
        }
        self.transmit_data(data)
        return


    def set_temp_ecs(self):
        data = {
            'CONS_ECS_DAY':   float(self.temp_ecs_day), \
            'CONS_ECS_NIGHT': float(self.temp_ecs_night) \
        }
        self.transmit_data(data)
        return


    def set_temp_boiler(self):
        data = {
            'MIN_BOILER': float(self.temp_boiler_min), \
            'MAX_BOILER': float(self.temp_boiler_max) \
        }
        self.transmit_data(data)
        return
