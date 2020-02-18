from Diematic import Diematic

def print_r(regs):
  for idx in regs:
    print "Reg[" + idx + "] => " + str(regs[idx][Diematic.REG_VAL])

    
if __name__ == '__main__':

  connection = { 'type': 'socket', \
                 'device': '/dev/ttyAMA0', \
                 'baudrate': 9600, \
                 'ip_addr': '192.168.178.160', 'ip_port': 20108 }

  regulator = Diematic(connection, debug=False)
  print "getting data ..."
  regulator.synchro(1,   63)
  regulator.synchro(64,  63)
  del regulator
