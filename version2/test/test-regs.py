import json

# ModBus Register Types
INTEGER  = 1
REAL10   = 2
BIT      = 3
SET      = 1

diematicReg = { \
        'CTRL':                 [None, 3,   INTEGER,  0, 0, 9999], \
        'HOUR':                 [None, 4,   INTEGER,  0, 0, 23], \
        'MINUTE':               [None, 5,   INTEGER,  0, 0, 59], \
        'WEEKDAY':              [None, 6,   INTEGER,  0, 1, 7], \
        'ALARM':                [None, 465, BIT,      0x0, 0, 0] }



print(json.dumps(diematicReg, indent=4) )

diematicReg['ALARM'][1] = 'Focker'
diematicReg['ALARM'][0] = SET

print(json.dumps(diematicReg, indent=4) )

