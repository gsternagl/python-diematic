import json

INTEGER = 0
BYTE = 1
REAL = 2


diematicReg = { \
        'YEAR':   (None, 0,   INTEGER,  2017), \
        'MONTH':  (None, 1,   INTEGER,  12), \
        'DAY':    (None, 2,   INTEGER,  9), \
        }

print(json.dumps(diematicReg, indent=4))
