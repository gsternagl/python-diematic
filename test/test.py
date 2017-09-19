#!/usr/bin/python

INTEGER = 1
REAL    = 2
BIT     = 3

diematicReg = { 'Reg_A': (), 'Reg_B': (), 'Reg_C': () }

diematicReg['Reg_A'] = (INTEGER, 22, 0)
diematicReg['Reg_B'] = (REAL, 33.33, 1)
diematicReg['Reg_C'] = (BIT, 0xff, None)

print diematicReg['Reg_A']
print diematicReg['Reg_B']
print diematicReg['Reg_C']

