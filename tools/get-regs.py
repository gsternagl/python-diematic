from Diematic import Diematic

def print_r(regs):
  for idx in regs:
    print "Reg[" + idx + "] => " + str(regs[idx][3])

    
if __name__ == '__main__':
  """  connection = { 'type': 'socket', \
                  'device': '/dev/ttyAMA0', \
                  'baudrate': 9600, \
                  'ip_addr': '192.168.178.160', \
                  'ip_port': 20108 }
  """

  connection = { 'type': 'socket', \
                 'device': '/dev/ttyAMA0', \
                 'baudrate': 9600, \
                 'ip_addr': '192.168.178.160', 'ip_port': 20108 }

  regulator = Diematic(connection, debug=True)
  print "getting data ..."
  regulator.synchro()
  print_r(regulator.diematicReg)
  del regulator


