from diematic import Diematic

def print_r(regs):
  for idx in regs:
    print("Reg[" + idx + "] => " + str(regs[idx][Diematic.REG_VAL]))

class my_logger:
    def error(self, s):
        print("ERROR:%s" % s)

    def debug(self, s):
        print("DEBUG:%s" % s)


    
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

#  my_l = my_logger()
  my_l = None
  regulator = Diematic(connection, debug=True, logger=my_l)
  print("getting data ...")
  regulator.synchro()
  print_r(regulator.diematicReg)
  del regulator


