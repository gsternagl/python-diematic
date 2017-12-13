import json

# ModBus Register Types
INTEGER  = 1
REAL10   = 2
BIT      = 3

diematicReg = { \
        'CTRL':                 [None, 3,   INTEGER,  0, 0, 9999], \
        'HOUR':                 [None, 4,   INTEGER,  0, 0, 23], \
        'MINUTE':               [None, 5,   INTEGER,  0, 0, 59], \
        'WEEKDAY':              [None, 6,   INTEGER,  0, 1, 7], \
        'ALARM':                [None, 465, BIT,      0x0, 0, 0] }



#for idx in diematicReg:
#    print "IDX=",str(idx)
#    print diematicReg[idx]
print(json.dumps(diematicReg, indent=4) )

#  print r
#  print (json.dumps(r, indent=4))
#  print(reg, diematicReg[reg])
#  print(json.dumps(d, indent=4))
