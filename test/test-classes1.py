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

reg = []

for count in range(10):
  x = Register('Reg_'+str(count), None, count, Register.INTEGER, 0)
  reg.append(x)

print "\nRegister 0:"
reg[0].dumpReg()
if reg[0].isset():
  print "Is set"
else:
  print "Is not set"

print "\nRegister 1:"
reg[1].setReg(0)
if reg[1].isset():
  print "Is set"
else:
  print "Is not set"

reg[1].dumpReg()
print "\nRegister 2:"
reg[2].unset()
reg[2].setValue(0.0)
reg[2].dumpReg()
