#!/usr/bin/python
from collections import namedtuple

INTEGER = 1
REAL    = 2
BIT     = 3

MyStruct = namedtuple("MyStruct", "set addr type value")
# m = MyStruct(None, 3, INTEGER, 2)


def dumpReg(reg):
  print "set:   ", getattr(reg, "set")
  print "addr:  ", getattr(reg, "addr")
  print "type:  ", getattr(reg, "type")
  print "value: ", getattr(reg, "value")

def isset(reg):
  if getattr(reg, "set") is None:
    return False
  else:
    return True

# doesn't work: namedtuples are immutable
def unset(reg):
  reg.set = None

# doesn't work: namedtuples are immutable
def setReg(reg, val):
  reg.set = val

diematicReg = { 'Reg_A': (), 'Reg_B': (), 'Reg_C': () }

diematicReg['Reg_A'] = MyStruct(None, 1, INTEGER, 22)
diematicReg['Reg_B'] = MyStruct(0,    2, REAL,    33.33)
diematicReg['Reg_C'] = MyStruct(set=None, addr=3, type=BIT, value=1)

dumpReg(diematicReg['Reg_A'])
dumpReg(diematicReg['Reg_B'])
dumpReg(diematicReg['Reg_C'])

setReg(diematicReg['Reg_A'], 0)

if isset(diematicReg['Reg_A']):
  print "Register A is set"
else:
  print "Register A not set"

unset(diematicReg['Reg_A'])

#print getattr(diematicReg['Reg_A'], "set")
#print diematicReg['Reg_B']
#print diematicReg['Reg_C']
#
#print diematicReg['Reg_A']

