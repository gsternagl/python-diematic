#!/usr/bin/python

import json
import requests
import os
from time import sleep
from datetime import datetime

REG_NAME    =   0
REG_VAL     =   4
REG_MIN     =   5
REG_MAX     =   6
DELAY       =  30
TEMP_LOG    = './temp.txt'

URL = 'http://0.0.0.0:5000/registers'
headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}

def dump_regs(regs, f_handle):
    thedate = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    val_str = str(regs['TEMP_EXT'][REG_VAL]) + ' ' + \
              str(regs['TEMP_ECS'][REG_VAL]) + ' ' + \
              str(regs['TEMP_BOILER'][REG_VAL])
    f_handle.write(thedate + ' ' + val_str + '\n')
    f_handle.flush()
        
logfile = open(TEMP_LOG, 'w')

while True:
    resp = requests.get(URL, headers=headers)
    if resp.status_code == 200:
        data = resp.json()
        if data is not None:
            dump_regs(data, logfile)
        else:
            print 'Error: data couldn\'t be read'
            break
    else:
        print 'Error: response:' + str(resp.status_code) 
        break
    sleep(DELAY)

logfile.close()


