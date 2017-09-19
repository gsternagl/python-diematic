from Diematic import Diematic

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
  regulator.synchro()

