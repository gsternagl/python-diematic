registers = { \
#  key  :  set,  addr, value, type
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
  reg.update(new)

def reg_set(reg, key, val):
  set = val
  addr  = reg[key][1]
  value = reg[key][2]
  type  = reg[key][3]
  new = { key: (set, addr, value, type) }
  reg.update(new)

def reg_print(reg, key):
  print reg[key][0]
  print reg[key][1]
  print reg[key][2]
  print reg[key][3]

print "Before Change:"
reg_print(registers, 'reg3')

print "\n\nChange 1 (set=True):"
reg_set(registers, 'reg3', True)
reg_print(registers, 'reg3')

print "\n\nChange 2 (unset):"
reg_unset(registers, 'reg3')
reg_print(registers, 'reg3')

