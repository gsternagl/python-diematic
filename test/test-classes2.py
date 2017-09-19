#!/usr/bin/python

class Register(object):
  INTEGER = 1
  REAL    = 2
  BIT     = 3
  __slots__ = ('name', 'set', 'addr', 'type', 'value')

  def __init__(self, name, set, addr, type, value):
    self.name  = name
    self.set   = set
    self.addr  = addr
    self.type  = type
    self.value = value

  def unset(self):
    self.set = None

  def isset(self):
    if self.set is not None:
      return True
    else:
      return False
  
  def setReg(self, val):
    self.set = val
  

  def dumpReg(self):
    print "name: ",  self.name
    print "set: ",   self.set
    print "type: ",  self.type
    print "value: ", self.value

  def getValue(self):
    return self.value

  def setValue(self, val):
    self.value = val

reg = {'Reg_A': None, 'Reg_B': None, 'Reg_C': None }

reg['Reg_A'] = Register('Reg_A', None, 1, Register.INTEGER, 11)
reg['Reg_B'] = Register('Reg_B', None, 2, Register.REAL, 22.22)
reg['Reg_C'] = Register('Reg_C', None, 3, Register.BIT, 0xff)

print "Register A:"
reg['Reg_A'].dumpReg()

print "\nRegister B:"
reg['Reg_B'].setReg(0)
if reg['Reg_B'].isset():
  print "Is set"
else:
  print "Is not set"
reg['Reg_B'].dumpReg()

print "\nRegister C:"
reg['Reg_C'].unset()
reg['Reg_C'].setValue(0xff)
reg['Reg_C'].dumpReg()
