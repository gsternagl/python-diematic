# -*- coding: utf-8 -*-
import json

BIT = 0
INTEGER = 1
REAL = 2

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
                    "reg_min"  : str(reg[idx][4]), \
                    "reg_max"  : str(reg[idx][5]), \
                } \
            } \
        }
    return json.dumps(a, indent=4)


#s = { "register": { "reg_name": "TEMP", "reg_content": { "reg_set": "None", "reg_addr": 1, "reg_value": "0.7", "reg_min": "-50.0", "reg_max": "150.0", } } } 

s = { "register": \
        { "reg_name": "TEMP", \
          "reg_content": \
          { \
            "reg_set": "None", \
            "reg_addr": 1, \
            "reg_value": 0.7, \
            "reg_min": -50.0, \
            "reg_max": 150.0, \
          } \
        } \
    }


t = { 'TEMP_EXT': (None, 1, REAL, 0.0, -50.0, 150.0), \
      'TEMP_INT': (None, 2, REAL, 20.0, 0.0, 50.0) }

s=''
for idx in t:
    s += myconvert(t, idx) + "\n"
print s

#print(json.dumps(s, indent=4))
#print(t)
#print(json.dumps(t, indent=4))
