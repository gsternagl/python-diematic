import os
basedir = os.path.abspath(os.path.dirname(__file__))

PROPAGATE_EXCEPTIONS = False

#DEBUG = False
FLASK_DEBUG = True

# DiematicD settings
DIEMATICD_EMULATION = False
#DIEMATICD_EMULATION = True
#DIEMATICD_HOST = '192.168.178.21'
DIEMATICD_PORT      = 5000
DIEMATICD_LOGFILE   = 'diematicd.log'

# Type of Connection to RS485 Interface: socket or serial
CONN_TYPE           = 'socket'

# TCP_RS485 Converter device
USR_TCP232_24_IP    = '192.168.178.160'
USR_TCP232_24_PORT  = 20108

# RS485 Interface
RS485_DEVICE        = '/dev/ttyAMA0'
RS485_BAUDRATE      = 9600

DIEMATIC_DEBUG      = False
