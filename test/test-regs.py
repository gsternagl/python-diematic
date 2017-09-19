registers = { \
  'reg1': (None, 1, 0xff, 'int'), \
  'reg2': (None, 2, 0xff, 'int'), \
  'reg3': (0,    3, 0xff, 'float'), \
  'reg4': (None, 4, 0xff, 'float'), \
  'reg5': (None, 5, 0xff, 'bit'), \
  'reg6': (None, 6, 0xff, 'bit') }


def reg_isset(reg):
  if reg[0] is None:
    return False
  else:
    return True

def reg_unset(reg, key):
  set = None
  addr  = reg[key][1]
  value = reg[key][2]
  type  = reg[key][3]
  new = { key: (set, addr, value, type) }
  reg[key].update(new)

print "Before Change:"
print "Reg1=None, ", reg_isset(registers['reg1'])
print "Reg3=0, ",    reg_isset(registers['reg3'])

print "\n\nAfter Change:"
reg_unset(registers, 'reg3')
print "Reg1=None, ", reg_isset(registers['reg1'])
print "Reg3=0, ",    reg_isset(registers['reg3'])

