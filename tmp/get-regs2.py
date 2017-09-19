from Diematic import Diematic

def print_r(regs):
  for idx in regs:
    print "Reg[" + idx + "] => " + str(regs[idx][3])

    
if __name__ == '__main__':
  """
  connection = { 'type': 'serial', \
                  'device': '/dev/ttyAMA0', \
                  'baudrate': 9600, \
                  'ip_addr': '', \
                  'ip_port': 0 }
  """

  connection = { 'type': 'socket', \
                 'device': '/dev/ttyAMA0', \
                 'baudrate': 9600, \
                 'ip_addr': '192.168.178.160', 'ip_port': 20108 }

  regulator = Diematic(connection, debug=True)
  print "getting data ..."
  regulator.synchro(1,    64)
  regulator.synchro(64,   64)
  regulator.synchro(128,  64)
  regulator.synchro(192, 64)

  del regulator


