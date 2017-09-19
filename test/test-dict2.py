mode_a = 34

regs = { \
  1:  ('selected' if mode_a == 1 else '', 'ANTIICE'), \
  2:  ('selected' if mode_a == 2 else '', 'PERM NIGHT'), \
  4:  ('selected' if mode_a == 4 else '', 'PERM DAY'), \
  8:  ('selected' if mode_a == 8 else '', 'AUTO'), \
  34: ('selected' if mode_a == 34 else '', 'DEROG NIGHT'), \
  36: ('selected' if mode_a == 36 else '', 'DEROG DAY') }


def print_r(reg):
  for key in sorted(reg):
    print "[" + str(key) + "] => " + str(reg[key])

print_r(regs)
