#!/usr/bin/python

import json
import requests

REG_NAME    =   0
REG_VAL     =   4
REG_MIN     =   5
REG_MAX     =   6

url = 'http://0.0.0.0:5000/registers/HOUR'
headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}

def dump_regs(regs):
    for idx in regs:
        print "Reg[" + idx + "] => " + str(regs[idx][REG_VAL])


def dump_reg_names(regs):
    for idx in regs:
        print idx

data = { "HOUR": [ 20 ] }
resp = requests.post(url, data=json.dumps(data), headers=headers)
if resp.status_code == 200:
    print 'Successful'
else:
    print 'Error setting register, response=', str(resp.status_code)

# check whether it has been set
resp = requests.get(url, headers=headers)
if resp.status_code == 200:
    data = resp.json()
    if data is not None:
        dump_regs(data)
    else:
        print 'Cannot decode data'
else:
    print 'Error getting register, response=', str(resp.status_code)


