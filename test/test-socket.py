import socket
import time

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
if sock is not None:
  sock.connect(('192.168.178.160', 20108))
  sock.settimeout(0.010)
  while 1:
    buf = ''
    try:
      buf = sock.recv(512)
    except:
      print "an error occured, never mind"

    if buf is None or buf == "":
      time.sleep(0.010);
    print "read: " + buf.encode('hex') + ', len=' + str(len(buf))

