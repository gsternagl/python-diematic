registers = { \
  'reg1': (1, 0xff, 'int'), \
  'reg2': (2, 0xff, 'int'), \
  'reg3': (3, 0xff, 'float'), \
  'reg4': (4, 0xff, 'float'), \
  'reg5': (5, 0xff, 'bit'), \
  'reg6': (6, 0xff, 'bit') }

# PHP alike array with "holes" in index
php_array = { \
  1: 'Gerald', \
  2: 'Kim', \
  4: 'Fabio', \
  400: 'Simba', \
  6: 'Alycia' }


def print_r(reg):
  for key in sorted(reg):
    print "[" + str(key) + "] => " + reg[key]

print "PHP-alike Array"
print_r(php_array)
print "updating..."
idx = 400
new = {idx: 'Simbalese'}
php_array.update(new)
print_r(php_array)
print '\n'

idx  = registers.get('reg1')[0];
addr = registers.get('reg1')[1];
type = registers.get('reg1')[2];

print "Unmodified registers"
print "--------------------"

for reg in sorted(registers):
  print "reg: " + str(reg) + " : " + str(registers[reg])

print "\n"
print "Modified registers"
print "------------------"

for reg in sorted(registers):
  idx  = registers[reg][0]
  addr = registers[reg][1]
  type = registers[reg][2]
  addr += 10
  registers.update( {reg : (idx, addr, type)} )
  print "reg: " + str(reg) + " : " + str(registers[reg])

# adding up a "row"
sum_val = sum([x[0] for x in registers.values()])

print "Sum of row[0]=" + str(sum_val)
