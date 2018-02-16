#!/usr/bin/python

import json
import requests

REG_NAME    =   0
REG_VAL     =   4
REG_MIN     =   5
REG_MAX     =   6

URL = 'http://0.0.0.0:5000/registers/TEMP_EXT'
headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}

def dump_regs(regs):
    for idx in regs:
        print "Reg[" + idx + "] => " + str(regs[idx][REG_VAL])


def dump_reg_names(regs):
    for idx in regs:
        print idx

resp = requests.get(URL, headers=headers)
if resp.status_code == 200:
    data = resp.json()
    if data is not None:
        dump_regs(data)
    else:
        print 'Error: data couldn\'t be read'
else:
    print 'Error: response:' + str(resp.status_code) 


