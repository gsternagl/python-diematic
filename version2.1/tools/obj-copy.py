import copy

INTEGER  = 1
REAL10   = 2
BIT      = 3

def print_r(regs):
  for idx in sorted(regs):
    print "Reg[" + idx + "] => " + str(regs[idx][3])

diematicReg = { \
        'CTRL':                 (None, 3,   INTEGER,  0), \
        'HOUR':                 (None, 4,   INTEGER,  0), \
        'MINUTE':               (None, 5,   INTEGER,  0), \
        'WEEKDAY':              (None, 6,   INTEGER,  0), \
        'TEMP_EXT':             (None, 7,   REAL10,   0.0), \
        'CONS_SUMWIN':          (None, 8,   REAL10,   0.0), \
        'NB_DAY_ANTIICE':       (None, 13,  INTEGER,  0), \
        'CONS_DAY_A':           (None, 14,  REAL10,   0.0), \
        'CONS_NIGHT_A':         (None, 15,  REAL10,   0.0), \
        'CONS_ANTIICE_A':       (None, 16,  REAL10,   0.0), \
        'MODE_A':               (None, 17,  BIT,      0x0), \
        'TEMP_AMB_A':           (None, 18,  REAL10,   0.0), \
        'STEEPNESS_A':          (None, 20,  REAL10,   0.0), \
        'TCALC_A':              (None, 21,  REAL10,   0.0), \
        'CONS_DAY_B':           (None, 23,  REAL10,   0.0), \
        'CONS_NIGHT_B':         (None, 24,  REAL10,   0.0), \
        'CONS_ANTIICE_B':       (None, 25,  REAL10,   0.0), \
        'STEEPNESS_B':          (None, 29,  REAL10,   0.0), \
        'CONS_ECS':             (None, 59,  REAL10,   0.0), \
        'TEMP_ECS':             (None, 62,  REAL10,   0.0), \
        'CONS_BOILER':          (None, 74,  REAL10,   0.0), \
        'TEMP_BOILER':          (None, 75,  REAL10,   0.0), \
        'BASE_ECS':             (None, 89,  BIT,      0x0), \
        'CONS_ECS_NIGHT':       (None, 96,  REAL10,   0.0), \
        'DAY':                  (None, 108, INTEGER,  0), \
        'MONTH':                (None, 109, INTEGER,  0), \
        'YEAR':                 (None, 110, INTEGER,  0), \
        'WATER_PRESSURE':       (None, 456, REAL10,   0.0), \
        'ALARM':                (None, 465, BIT,      0x0)}


print_r(diematicReg)
print("")
print("")

foobar = diematicReg.copy()
print_r(foobar)

