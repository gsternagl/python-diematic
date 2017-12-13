# -*- coding: utf-8 -*-
import json
from flask import Flask, jsonify

BIT     = 0
INTEGER = 1
REAL10  = 2

regs = { \
        'CTRL':                 (None, 3,   INTEGER,  0), \
        'HOUR':                 (None, 4,   INTEGER,  0), \
        'MINUTE':               (None, 5,   INTEGER,  0), \
        'WEEKDAY':              (None, 6,   INTEGER,  0), \
        'TEMP_EXT':             (None, 7,   REAL10,   0.0), \
        'ALARM':                (None, 465, BIT,      0x0) }

app = Flask(__name__)

def regType(a):
  if a==BIT:
    return "BIT"
  elif a==INTEGER:
    return "INTEGER"
  else:
    return "REAL"

def myconvert(reg, idx):
    a = { "register": \
            { "reg_name": idx, \
                "reg_content": \
                { \
                    "reg_set"  : str(reg[idx][0]), \
                    "reg_addr" : str(reg[idx][1]), \
                    "reg_type" : regType(str(reg[idx][2])), \
                    "reg_value": str(reg[idx][3]), \
                } \
            } \
        }
    s = json.dumps(a, indent=4)
    return s

@app.route('/registers', methods=['GET'])
def get_registers():
    global regs
    s = ''

    for idx in regs:
        s += myconvert(regs, idx) + "\n"

    return s

if __name__ == '__main__':
    app.run()
