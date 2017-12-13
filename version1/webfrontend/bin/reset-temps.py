from Diematic import Diematic

if __name__ == '__main__':
  connection = { 'type': 'socket', \
                 'device': '/dev/ttyAMA0', \
                 'baudrate': 9600, \
                 'ip_addr': '192.168.178.160', 'ip_port': 20108 }

  regulator = Diematic(connection, debug=False)
  regulator.setTemp_A(23.0, 17.0, 6.0)
  regulator.setTemp_B(19.0, 17.0, 6.0)
  regulator.setSteepness_A(1.6)
  regulator.setSteepness_B(0.7)
  regulator.setEcsTemp(45.0, 10.0)

  regulator.synchro()

