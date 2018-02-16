#!/usr/bin/python

import json
import urllib

REG_NAME    =   0
REG_VAL     =   4
REG_MIN     =   5
REG_MAX     =   6

#{u'TEMP_EXT': [None, 7, 2, False, 2.7, -50.0, 150.0]}

def dump_regs(regs):
    for idx in regs:
        print "Reg[" + idx + "] => " + str(regs[idx][REG_VAL])


hres = urllib.urlopen('http://0.0.0.0:5000/registers')
data = json.loads(hres.read().decode("utf-8"))
print('Multi Registers Dump')
print('--------------------')
dump_regs(data)


#s = json.dumps(data, indent=4)

#print("Type(s)=", type(s))
#print(s)

hres = urllib.urlopen('http://0.0.0.0:5000/registers/TEMP_EXT')
data = json.loads(hres.read().decode("utf-8"))
print('')
print('Single Registers Dump')
print('---------------------')
dump_regs(data)

