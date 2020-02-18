#!/usr/bin/python

import time
import socket
#import serial

class ModBus:
  NOT_CONNECTED       = -1
  FRAME_OK            = 0
  FRAME_EMPTY         = 1
  READ_ERROR          = 2
  FRAME_ERROR         = 3
  FRAME_LENGTH_ERROR  = 4
  FRAM_TOO_SHORT      = 5
  NOT_ADDRESSED_TO_ME = 6
  NOT_SUPPORTED_FC    = 7
  FRAME_TOO_LONG      = 8
  CRC_ERROR           = 9
  NO_ACK              = 10
  ADDR_ERROR          = 11
  FC_ERROR            = 12

  READ_ANALOG_HOLDING_REGISTERS = 0x03
  WRITE_MULTIPLE_REGISTERS      = 0x10

  FRAME_MIN_LENGTH              = 0x04
  FRAME_MAX_LENGTH              = 0x100
  FRAME_EXTRA_BYTE_ALLOWED      = 0x03

  REQUEST_TO_ANSWER_DELAY_STEP  = 0.02
  REQUEST_TO_ANSWER_MAX_STEP    = 20

  MAX_BYTE_READ                 = 512

  # connection types
  CONN_SERIAL = 1
  CONN_SOCKET = 2

  status = FRAME_OK

  def __init__(self, modBusAddr, conn):
    self.modBusAddr = modBusAddr
    if conn['type'] == 'serial':
      self.conn_type = self.CONN_SERIAL
      self.conn_addr = conn['device']
      self.conn_baud = conn['baudrate']
    else:
      self.conn_type = self.CONN_SOCKET
      self.conn_addr = conn['ip_addr']
      self.conn_port = conn['ip_port']

    self.conn_fp = self.conn_open()
    if self.conn_fp is None:
      self.log = "can't open data connection to diematic"
      return

    self.rxReg = {}
    self.log = "connection established"
    self.status = self.FRAME_OK

  def __del__(self):
    self.conn_fp.close()

  def conn_read(self, size):
    buff = None
    try:
      if self.conn_type == self.CONN_SERIAL:
        buff = self.conn_fp.read(size)
      else:
        buff = self.conn_fp.recv(size)
    except:
      buff = ''

    return buff

  def conn_write(self, buff):
    if self.conn_type == self.CONN_SERIAL:
      sent = self.conn_fp.write(buff)
    else:
      sent = self.conn_fp.send(buff)
    return sent


  def conn_open(self):
    if self.conn_type == self.CONN_SERIAL:
      try:
        ser = serial.Serial(
          port     = self.conn_addr,
          baudrate = self.conn_baud,
          parity   = serial.PARITY_NONE,
          stopbits = serial.STOPBITS_ONE,
          bytesize = serial.EIGHTBITS,
          timeout  = 0.1
        )
      except ValueError, SerialException:
        ser = None
      return ser
    # it's a socket connection
    else:
      try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if sock is not None:
          sock.connect((self.conn_addr, self.conn_port))
          sock.settimeout(0.001)
      except:
        sock = None
      return sock

  def print_r(self, reg):
    s = ''
    for key in sorted(reg):
      s += '    [' + str(key) + '] => '
      s += str(reg[key]) + '\n'
    return s

  def bin2hex(self, buf):
    return buf.encode('hex')

  def slaveRx(self):
    self.log = "Slave RX:\n"
    self.rxReg.clear()
    self.rxBuf = ""
    self.status = self.FRAME_OK

    self.rxBuf = self.conn_read(self.MAX_BYTE_READ)
    self.log += self.bin2hex(self.rxBuf) + " : "

    # check socket result
    if self.rxBuf == None:
      self.log += "READ_ERROR\n"
      self.status = self.READ_ERROR
      return self.status

    # check if buffer is empty
    if self.rxBuf == "":
      self.log += "FRAME_EMPTY\n"
      self.status = self.FRAME_EMPTY
      return self.status

    # check length
    if (len(self.rxBuf) > self.FRAME_MAX_LENGTH) or (len(self.rxBuf)<self.FRAME_MIN_LENGTH):
      self.log += "FRAME_LENGTH_ERROR\n"
      self.status = self.FRAME_LENGTH_ERROR
      return self.status

    # check modBus address
    addr = ord(self.rxBuf[0])
    if (self.modBusAddr != 0) and (addr != self.modBusAddr):
      self.log += "NOT_ADDRESSED_TO_ME\n"
      self.status = self.NOT_ADDRESSED_TO_ME
      return self.status

    # check modBus feature
    fc = ord(self.rxBuf[1])

    # decode WRITE_MULTIPLE_REGISTERS frame
    if fc == self.WRITE_MULTIPLE_REGISTERS:
        # decode register number
        if len(self.rxBuf) < 9:
          self.log += "FRAME_ERROR\n"
          self.status = self.FRAME_ERROR
          return self.status
        regNumber = ord(self.rxBuf[4]) * 0x100 + ord(self.rxBuf[5])

        # check if byte nb is twice register number
        if 2*regNumber != ord(self.rxBuf[6]):
          self.log += "FRAME_ERROR\n"
          self.status = self.FRAME_ERROR
          return self.status

        # calculate frame wait length
        frameLength = 2*regNumber+9
        if frameLength > len(self.rxBuf):
          self.log += "FRAME_TOO_SHORT\n"
          self.status = self.FRAME_TOO_SHORT
          return self.status

        # check frame size
        if (frameLength + self.FRAME_EXTRA_BYTE_ALLOWED) < len(self.rxBuf):
          self.log += "FRAME_TOO_LONG\n"
          self.status = self.FRAME_TOO_LONG
          return self.status

        # check CRC
        crcCalc = self.calcCRC16(self.rxBuf, frameLength-2)
        crc = 0x100 * ord(self.rxBuf[frameLength-1])+ord(self.rxBuf[frameLength-2])
        if crc != crcCalc:
          self.log += "CRC_ERROR\n"
          self.status = self.CRC_ERROR
          return self.status

        # frame is correct, save values and acknowledge
        regAddr = 0x100 * ord(self.rxBuf[2]) + ord(self.rxBuf[3])
        for i in range(0, regNumber):
          idx = regAddr + i
          val = 0x100 * ord(self.rxBuf[2*i+7])+ord(self.rxBuf[2*i+8])
          self.rxReg.update( {idx : val} )

        self.log += "FRAME_OK\n"
        self.log += self.print_r(self.rxReg)
        tx = self.rxBuf[0:6]

        # calculate and add checksum
        crCalc = self.calcCRC16(tx, 6)
        tx += chr(crCalc & 0xff)
        tx += chr((crCalc >> 8) & 0xff)
        tx += chr(0) + chr(0) + chr(0)

        # send acknowledge if slave address is not 0
        if self.modBusAddr != 0:
          result = self.conn_write(tx)
          if result == 0:
            self.log += "slaveRx: acknowledge write failed\n"

        self.status = self.FRAME_OK
        return self.status

    if fc == self.READ_ANALOG_HOLDING_REGISTERS:
        # calculate frame wait length
        frameLength = 8

        # check frame size is not too short for data volume
        if frameLength > len(self.rxBuf):
            self.log += "FRAME_TOO_SHORT\n"
            self.status = self.FRAME_TOO_SHORT
            return self.status

        # check whether frame size is too long for data volume + 3 extra bytes
        if frameLength + self.FRAME_EXTRA_BYTE_ALLOWED < len(self.rxBuf):
            self.log += "FRAME_TOO_LONG\n"
            self.status = self.FRAME_TOO_LONG
            return self.status

        # check crCalc
        crcCalc = self.calcCRC16(self.rxBuf, frameLength-2)
        crc = 0x100 * ord(self.rxBuf[frameLength-1]) + ord(self.rxBuf[frameLength-2])
        if crc != crcCalc:
            self.log += "CRC_ERROR\n"
            self.status = self.CRC_ERROR
            return self.status
        regAddr = 0x100 * ord(self.rxBuf[2]) + ord(self.rxBuf[3])
        regNb = 0x100 * ord(self.rxBuf[4]) + ord(self.rxBuf[5])

        self.log += "FRAME_OK Read :" + str(regAddr) + ":" + str(regNb) + "\n"

        # do not send ACK as there is no data to provide
        self.status = self.FRAME_OK
        return self.status

    else:
        self.log += "NOT_SUPPORTED_FC: >" + hex(fc) + "<\n"
        self.status = self.NOT_SUPPORTED_FC
        return self.status

  def masterRx(self, modBusAddr, regAddr, regNb):
    # init
    self.rxReg.clear()

    # init log
    self.log = "Master RX:" + str(modBusAddr) + ":" + \
                              str(regAddr) + ":" + \
                              str(regNb) + "\n"

    # prepare request frame
    tx = chr(modBusAddr) + chr(self.READ_ANALOG_HOLDING_REGISTERS) + self.int2str(regAddr) + self.int2str(regNb)
    tx += self.int2str(self.switchEndian(self.calcCRC16(tx, 0))) + chr(0)

    # sent frame
    result = self.conn_write(tx)

    self.log += "Request: " + self.bin2hex(tx) + "\n"
    buf = ""
    i = 0

    # wait for answer frame
    while True:
      time.sleep(self.REQUEST_TO_ANSWER_DELAY_STEP)
      self.rxBuf = self.conn_read(self.MAX_BYTE_READ)
      i += 1
      if self.rxBuf is not None and self.rxBuf != '':
        break
      if i >= self.REQUEST_TO_ANSWER_MAX_STEP:
        break

    self.log += "Answer: " + self.bin2hex(self.rxBuf) + "\n"

    # check socket result
    if self.rxBuf is None:
      self.log += "READ_ERROR\n"
      self.status = self.READ_ERROR
      return self.status

    # check rough length
    if len(self.rxBuf) > self.FRAME_MAX_LENGTH or len(self.rxBuf) < self.FRAME_MIN_LENGTH:
      self.log += "FRAME_ERROR: length\n"
      self.status = self.FRAME_ERROR
      return self.status

    # check modBus addr
    addr = ord(self.rxBuf[0])
    if addr != modBusAddr:
      self.log += "NOT_ADDRESSED_TO_ME\n"
      self.status = self.NOT_ADDRESSED_TO_ME
      return self.status

    # check modBus feature
    fc = ord(self.rxBuf[1])
    if fc != self.READ_ANALOG_HOLDING_REGISTERS:
      self.log += "NOT_SUPPORTED_FC: >" + hex(fc) + "<\n"
      self.status = self.NOT_SUPPORTED_FC
      return self.status

    # check answer number of bytes. if received frame is too small or too long
    byteNb = ord(self.rxBuf[2])
    frameLength = 5 + byteNb
    if byteNb != 2 * regNb or len(self.rxBuf)<frameLength or frameLength+self.FRAME_EXTRA_BYTE_ALLOWED<len(self.rxBuf):
      self.log += "FRAME_ERROR: bytes received are wrong\n"
      self.status = self.FRAME_ERROR
      return self.status

    # check CRC
    crcCalc = self.calcCRC16(self.rxBuf, frameLength-2)
    crc = 0x100 * ord(self.rxBuf[frameLength-1])+ord(self.rxBuf[frameLength-2])
    if crc != crcCalc:
      self.log += "CRC_ERROR\n"
      self.status = self.CRC_ERROR
      return self.status

    # the frame is correct: save values
    for i in range(0, regNb):
      idx = regAddr + i
      val = 0x100 * ord(self.rxBuf[2*i+3])+ord(self.rxBuf[2*i+4])
      if val >= 0x8000:
        val = -(val & 0x7fff)
      self.rxReg.update( {idx: val} )

    self.log += self.print_r(self.rxReg)
    self.status = self.FRAME_OK
    return self.status

  # function used to set 1 data register in master
  def masterTx(self, modBusAddr, register):
    return self.masterTxN(modBusAddr, register)

  # function used to set data in master mode for several consecutive registers (with consecutive numeric index)
  def masterTxN(self, modBusAddr, register):
    # Init Log
    self.log = "Master TXN:" + str(modBusAddr) + ":" + self.print_r(register)

    # prepare request frame
    nb = len(register)
    tx = chr(modBusAddr) + chr(self.WRITE_MULTIPLE_REGISTERS) + \
         self.int2str(register[0][1]) + \
         self.int2str(nb) + chr(2*nb)
    for index in range(0, nb):
      tx += self.int2str(register[index][0])
    tx += self.int2str(self.switchEndian(self.calcCRC16(tx, 0))) + chr(0)

    # log
    self.log += "Request: " + self.bin2hex(tx)+"\n"

    # send it
    result = self.conn_write(tx)

    # wait 100ms max for answer time
    buf = ""
    i = 0
    while True:
      time.sleep(self.REQUEST_TO_ANSWER_DELAY_STEP)
      buf = self.conn_read(self.MAX_BYTE_READ)
      i += 1
      if buf is not None and buf != '':
        break
      if i >= self.REQUEST_TO_ANSWER_MAX_STEP:
        break

    # log
    self.log += "Answer: " + self.bin2hex(buf) + "\n"

    # check socket result
    if buf is None:
      self.log += "NO_ACK\n"
      self.status = self.NO_ACK
      return self.status

    # check rough length
    if len(buf) > self.FRAME_MAX_LENGTH or len(buf) < self.FRAME_MIN_LENGTH:
      self.log += "FRAME_ERROR\n"
      self.status = self.FRAME_ERROR
      return self.status

    # check modBus addr
    addr = ord(buf[0])
    if addr != modBusAddr:
      self.log += "ADDR_ERROR\n"
      self.status = self.ADDR_ERROR
      return self.status

    # check modBus feature
    fc = ord(buf[1])
    if fc != self.WRITE_MULTIPLE_REGISTERS:
      self.log += "FC_ERROR\n"
      self.status = self.FC_ERROR
      return self.status

    # check answer number of bytes
    regNb = ord(buf[5])
    frameLength = 8
    if regNb != nb or len(buf) < frameLength or \
       frameLength + self.FRAME_EXTRA_BYTE_ALLOWED < len(buf):
      self.log += "FRAME_ERROR\n"
      self.status = self.FRAME_ERROR
      return self.status

    # check CRC
    crcCalc = self.calcCRC16(buf, frameLength-2)
    crc = 0x100 * ord(buf[frameLength-1]) + ord(buf[frameLength-2])
    if crc != crcCalc:
      self.log += "CRC_ERROR\n"
      self.status = self.CRC_ERROR
      return self.status

    self.status = self.FRAME_OK
    return self.status

  # calculate ModBus CRC16 of buf array
  def calcCRC16(self, buf, length):
    crc = 0xffff
    b = i = n = 0
    if length == 0:
      length = len(buf)

    for i in range(0,length):
      b = ord(buf[i])
      crc ^= b
      n = 1
      for n in range(1, 9):
        if crc & 1 == 1:
          crc = (crc >> 1) ^ 0xa001
        else:
          crc >>= 1

    return crc

  # modBus integer to string converter
  def int2str(self, int):
    return chr((int >> 8) & 0xff) + chr(int & 0xff)

  def switchEndian(self, int):
    return ((int >> 8) & 0xff) | ((int & 0xff) << 8)
