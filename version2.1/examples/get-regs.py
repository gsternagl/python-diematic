#!/usr/bin/python

import json
import urllib
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
d_str = json.dumps(data)
print 'Data String=', d_str
resp = requests.post(url, data=json.dumps(data), headers=headers)
print 'Response=', resp

# check whether it has been set
hres = urllib.urlopen(url)
data = json.loads(hres.read().decode("utf-8"))
dump_regs(data)
dump_reg_names(data)


