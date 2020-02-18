#!/usr/bin/python
#-*- coding: utf-8 -*-
""" This file defines the ModBus class which provides communication methods
    to talk to an RS485 connected Diematic III controller."""

import time
import socket
import logging
import binascii
import sys
from .timeout import timeout

def b_chr(a: int) -> bytes:
    a = a & 0xff
    return bytes([a])

""" The Modbus class does all the communication with the Diematic III
    controller.
"""
class ModBus(object):
    NOT_CONNECTED = -1
    FRAME_OK = 0
    FRAME_EMPTY = 1
    READ_ERROR = 2
    FRAME_ERROR = 3
    FRAME_LENGTH_ERROR = 4
    FRAME_TOO_SHORT = 5
    NOT_ADDRESSED_TO_ME = 6
    NOT_SUPPORTED_FC = 7
    FRAME_TOO_LONG = 8
    CRC_ERROR = 9
    NO_ACK = 10
    ADDR_ERROR = 11
    FC_ERROR = 12
    WRITE_ERROR = 13

    READ_ANALOG_HOLDING_REGISTERS = 0x03
    WRITE_MULTIPLE_REGISTERS = 0x10

    FRAME_MIN_LENGTH = 0x04
    FRAME_MAX_LENGTH = 0x100
    FRAME_EXTRA_BYTE_ALLOWED = 0x03

    REQUEST_TO_ANSWER_DELAY_STEP = 0.02
    REQUEST_TO_ANSWER_MAX_STEP = 30

    MAX_BYTE_READ = 512

    # connection types
    CONN_SERIAL = 1
    CONN_SOCKET = 2

    status = FRAME_OK

    def __init__(self, modbus_addr, conn, logger=None):
        if logger:
            self.logger = logger
        else:
            self.logger = logging.getLogger('modbus.py')
        self.modbus_addr = modbus_addr
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
            self.logger.debug("can't open data connection to diematic")
            self.status = self.NOT_CONNECTED
            return

        self.rx_reg = {}
        self.rx_buff = b''
        self.logger.debug("modbus connection established")
        self.status = self.FRAME_OK

    def __del__(self):
        if self.conn_fp is not None:
            self.conn_fp.close()

    @timeout(10)
    def conn_read(self, size) -> bytes:
        buff = None
        ret_str = ''
        try:
            if self.conn_type == self.CONN_SERIAL:
                buff = self.conn_fp.read(size)
            else:
                buff = self.conn_fp.recv(size)
        except:
            buff = b''

        return buff

    @timeout(10)
    def conn_write(self, buff: str) -> int:
        sent = 0
        try:
            if self.conn_type == self.CONN_SERIAL:
                sent = self.conn_fp.write(buff)
            else:
                sent = self.conn_fp.send(buff)
        except:
            self.logger.debug("Error in conn_write")

        return sent

    @timeout(10)
    def conn_open(self):
        if self.conn_type == self.CONN_SERIAL:

            import serial

            try:
                ser = serial.Serial(
                    port=self.conn_addr,
                    baudrate=self.conn_baud,
                    parity=serial.PARITY_NONE,
                    stopbits=serial.STOPBITS_ONE,
                    bytesize=serial.EIGHTBITS,
                    timeout=0.1
                )
            except ValueError:
                pass
            except serial.SerialException:
                self.logger.error("opening serial connection failed")
                ser = None
            return ser

        # otherwise it's a socket connection
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            if sock is not None:
                sock.connect((self.conn_addr, self.conn_port))
                sock.settimeout(0.001)
        except:
            self.logger.error("opening network socket failed")
            sock = None
        return sock


    def print_r(self, reg):
        buff = ''
        for key in sorted(reg):
            buff += '    [' + str(key) + '] => '
            buff += str(reg[key]) + '\n'
        return buff


    def bin2hex(self, buf: bytes) -> str:
        if len(buf) > 0:
            #h = buf.hex()
            a = binascii.hexlify(buf)
            h = a.decode('ascii')
        else:
            h = ''

        return h


    def slave_rx(self):
        self.logger.debug("Slave RX:")
        self.rx_reg.clear()
        self.rx_buff = b''
        self.status = self.FRAME_OK

        self.rx_buff = self.conn_read(self.MAX_BYTE_READ)
        self.logger.debug(self.bin2hex(self.rx_buff) + " : ")

        # check socket result
        if self.rx_buff is None:
            self.logger.debug("slave_rx: READ_ERROR")
            self.status = self.READ_ERROR
            return self.status

        # check if buffer is empty
        if len(self.rx_buff) == 0:
            self.logger.debug("slave_rx: FRAME_EMPTY")
            self.status = self.FRAME_EMPTY
            return self.status

        # check length
        if len(self.rx_buff) > self.FRAME_MAX_LENGTH or \
           len(self.rx_buff) < self.FRAME_MIN_LENGTH:
            self.logger.debug("slave_rx: FRAME_LENGTH_ERROR")
            self.status = self.FRAME_LENGTH_ERROR
            return self.status

        # check modBus address
        addr = int(self.rx_buff[0])
        if self.modbus_addr != 0 and addr != self.modbus_addr:
            self.logger.debug("slave_rx: NOT_ADDRESSED_TO_ME")
            self.status = self.NOT_ADDRESSED_TO_ME
            return self.status

        # check modBus feature
        fc = int(self.rx_buff[1])

        # decode WRITE_MULTIPLE_REGISTERS frame
        if fc == self.WRITE_MULTIPLE_REGISTERS:
            # decode register number
            if len(self.rx_buff) < 9:
                self.logger.debug("slave_rx: FRAME_LENGTH_ERROR")
                self.status = self.FRAME_LENGTH_ERROR
                return self.status

            reg_nr = int(self.rx_buff[4]) * 0x100 + int(self.rx_buff[5])

            # check if byte nb is twice register number
            if 2*reg_nr != int(self.rx_buff[6]):
                self.logger.debug("slave_rx: FRAME_ERROR")
                self.status = self.FRAME_ERROR
                return self.status

            # calculate frame wait length
            frame_len = 2 * reg_nr + 9
            if frame_len > len(self.rx_buff):
                self.logger.debug("slave_rx: FRAME_TOO_SHORT")
                self.status = self.FRAME_TOO_SHORT
                return self.status

            # check frame size
            if (frame_len + self.FRAME_EXTRA_BYTE_ALLOWED) < len(self.rx_buff):
                self.logger.debug("slave_rx: FRAME_TOO_LONG")
                self.status = self.FRAME_TOO_LONG
                return self.status

            # check CRC
            crc_calc = self.calc_crc_16(self.rx_buff, frame_len - 2)
            crc = 0x100 * int(self.rx_buff[frame_len - 1]) + \
                  int(self.rx_buff[frame_len - 2])
            if crc != crc_calc:
                self.logger.debug("slave_rx: CRC_ERROR")
                self.status = self.CRC_ERROR
                return self.status

            # frame is correct, save values and acknowledge
            reg_addr = 0x100 * int(self.rx_buff[2]) + int(self.rx_buff[3])
            for i in range(0, reg_nr):
                idx = reg_addr + i
                val = 0x100 * int(self.rx_buff[2*i+7]) + int(self.rx_buff[2*i+8])
                self.rx_reg.update({idx : val})

            self.logger.debug("FRAME_OK")
            self.logger.debug(self.print_r(self.rx_reg))
            tx = self.rx_buff[0:6]

            # calculate and add checksum
            checksum = self.calc_crc_16(tx, 6)
            tx += b_chr(checksum & 0xff)
            tx += b_chr((checksum >> 8) & 0xff)
            tx += b_chr(0) + b_chr(0) + b_chr(0)

            # send acknowledge if slave address is not 0
            if self.modbus_addr != 0:
                result = self.conn_write(tx)
                if result == 0:
                    self.logger.debug("slave_rx: acknowledge write failed")

            self.status = self.FRAME_OK
            return self.status

        elif fc == self.READ_ANALOG_HOLDING_REGISTERS:
            # calculate frame wait length
            frame_len = 8

            # check frame size is not too short for data volume
            if frame_len > len(self.rx_buff):
                self.logger.debug("FRAME_TOO_SHORT")
                self.status = self.FRAME_TOO_SHORT
                return self.status

            # check whether frame size is too long for data volume + 3 extra bytes
            if frame_len + self.FRAME_EXTRA_BYTE_ALLOWED < len(self.rx_buff):
                self.logger.debug("FRAME_TOO_LONG")
                self.status = self.FRAME_TOO_LONG
                return self.status

            # check crCalc
            checksum = self.calc_crc_16(self.rx_buff, frame_len-2)
            crc = 0x100 * int(self.rx_buff[frame_len-1]) + int(self.rx_buff[frame_len-2])
            if crc != checksum:
                self.logger.debug("CRC_ERROR")
                self.status = self.CRC_ERROR
                return self.status
            reg_addr = 0x100 * int(self.rx_buff[2]) + int(self.rx_buff[3])
            reg_nb = 0x100 * int(self.rx_buff[4]) + int(self.rx_buff[5])

            self.logger.debug("FRAME_OK Read :" + str(reg_addr) + ":" + str(reg_nb))

            # do not send ACK as there is no data to provide
            self.status = self.FRAME_OK
            return self.status

        else:
            self.logger.debug("NOT_SUPPORTED_FC: >" + hex(fc) + "<")
            self.status = self.NOT_SUPPORTED_FC
            return self.status


    """ master modbus receive method.
    """
    def master_rx(self, modbus_addr, reg_addr, reg_nb):
        # init
        self.rx_reg.clear()

        # init log
        self.logger.debug("Master RX:" + str(modbus_addr) + ":" + \
            str(reg_addr) + ":" + \
            str(reg_nb) \
        )

        # prepare request frame
        tx = b_chr(modbus_addr) + b_chr(self.READ_ANALOG_HOLDING_REGISTERS) + \
             self.int2bytes(reg_addr) + self.int2bytes(reg_nb)
        tx += self.int2bytes(self.switch_endian(self.calc_crc_16(tx, 0))) + \
              b_chr(0)

        # send frame
        result = self.conn_write(tx)
        self.logger.debug("Request: " + self.bin2hex(tx))

        i = 0
        self.rx_buff = b''

        # wait for answer frame
        while True:
            time.sleep(self.REQUEST_TO_ANSWER_DELAY_STEP)
            self.rx_buff = self.conn_read(self.MAX_BYTE_READ)
            i += 1
            if self.rx_buff and len(self.rx_buff) > 0:
                break
            if i >= self.REQUEST_TO_ANSWER_MAX_STEP:
                break

        self.logger.debug("Answer: " + self.bin2hex(self.rx_buff))

        # check socket result
        if self.rx_buff is None:
            self.logger.debug("Socket READ_ERROR")
            self.status = self.READ_ERROR
            return self.status

        # check rough length
        if len(self.rx_buff) > self.FRAME_MAX_LENGTH or \
           len(self.rx_buff) < self.FRAME_MIN_LENGTH:
            self.logger.debug("FRAME_LENGTH_ERROR: length")
            self.status = self.FRAME_LENGTH_ERROR
            return self.status

        # check modBus addr
        addr = int(self.rx_buff[0])
        if addr != modbus_addr:
            self.logger.debug("NOT_ADDRESSED_TO_ME")
            self.status = self.NOT_ADDRESSED_TO_ME
            return self.status

        # check modBus feature
        fc = int(self.rx_buff[1])
        if fc != self.READ_ANALOG_HOLDING_REGISTERS:
            self.logger.debug("NOT_SUPPORTED_FC: >" + hex(fc))
            self.status = self.NOT_SUPPORTED_FC
            return self.status

        # check answer number of bytes. if received frame is too small
        # or too long
        byte_nb = int(self.rx_buff[2])
        frame_len = 5 + byte_nb
        if byte_nb != 2 * reg_nb or \
           len(self.rx_buff) < frame_len or \
           frame_len + self.FRAME_EXTRA_BYTE_ALLOWED < len(self.rx_buff):
            self.logger.debug("FRAME_LENGTH_ERROR: bytes received are wrong")
            self.status = self.FRAME_LENGTH_ERROR
            return self.status

        # check CRC
        crc_calc = self.calc_crc_16(self.rx_buff, frame_len-2)
        crc = 0x100 * int(self.rx_buff[frame_len-1]) + \
              int(self.rx_buff[frame_len-2])
        if crc != crc_calc:
            self.logger.debug("CRC_ERROR")
            self.status = self.CRC_ERROR
            return self.status

        # the frame is correct: save values
        for i in range(0, reg_nb):
            idx = reg_addr + i
            val = 0x100 * int(self.rx_buff[2*i+3]) + int(self.rx_buff[2*i+4])
            if val >= 0x8000:
                val = -(val & 0x7fff)
            self.rx_reg.update({idx: val})

        self.logger.debug(self.print_r(self.rx_reg))
        self.status = self.FRAME_OK
        return self.status


    """ function used to set 1 data register in master.
    """
    def master_tx(self, modbus_addr, register):
        return self.master_tx_n(modbus_addr, register)


    """ function used to set data in master mode for several consecutive
        registers (with consecutive numeric index).
    """
    def master_tx_n(self, modbus_addr, register):
        buff = ''
        # Init Log
        self.logger.debug("Master TXN:" + str(modbus_addr) + ":" + \
                          self.print_r(register))

        # prepare request frame
        nb = len(register)
        tx = b_chr(modbus_addr) + b_chr(self.WRITE_MULTIPLE_REGISTERS) + \
             self.int2bytes(register[0][1]) + \
             self.int2bytes(nb) + b_chr(2*nb)
        for index in range(0, nb):
            tx += self.int2bytes(register[index][0])
        tx += self.int2bytes(self.switch_endian(self.calc_crc_16(tx, 0))) + \
              b_chr(0)
        self.logger.debug("Request: " + self.bin2hex(tx))

        # send it
        result = self.conn_write(tx)

        # wait 100ms max for answer time
        i = 0
        while True:
            time.sleep(self.REQUEST_TO_ANSWER_DELAY_STEP)
            buff = self.conn_read(self.MAX_BYTE_READ)
            i += 1
            if buff is not None and buff != b'':
                break
            if i >= self.REQUEST_TO_ANSWER_MAX_STEP:
                break

        # log
        self.logger.debug("Answer: " + self.bin2hex(buff))

        # check socket result
        if buff is None:
            self.logger.debug("NO_ACK")
            self.status = self.NO_ACK
            return self.status

        # check rough length
        if len(buff) > self.FRAME_MAX_LENGTH or \
           len(buff) < self.FRAME_MIN_LENGTH:
            self.logger.debug("FRAME_LENGTH_ERROR")
            self.status = self.FRAME_LENGTH_ERROR
            return self.status

        # check modBus addr
        addr = int(buff[0])
        if addr != modbus_addr:
            self.logger.debug("ADDR_ERROR")
            self.status = self.ADDR_ERROR
            return self.status

        # check modBus feature
        fc = int(buff[1])
        if fc != self.WRITE_MULTIPLE_REGISTERS:
            self.logger.debug("FC_ERROR")
            self.status = self.FC_ERROR
            return self.status

        # check answer number of bytes
        reg_nb = int(buff[5])
        frame_len = 8
        if reg_nb != nb or \
           len(buff) < frame_len or \
           frame_len + self.FRAME_EXTRA_BYTE_ALLOWED < len(buff):
            self.logger.debug("FRAME_ERROR")
            self.status = self.FRAME_ERROR
            return self.status

        # check CRC
        crc_calc = self.calc_crc_16(buff, frame_len-2)
        crc = 0x100 * int(buff[frame_len-1]) + int(buff[frame_len-2])
        if crc != crc_calc:
            self.logger.debug("CRC_ERROR")
            self.status = self.CRC_ERROR
            return self.status

        self.status = self.FRAME_OK
        return self.status


    """ calculate ModBus CRC16 of buff array.
    """
    def calc_crc_16(self, buff, length):
        crc = 0xffff
        var_b = idx = 0
        if length == 0:
            length = len(buff)

        for idx in range(0, length):
            var_b = int(buff[idx])
            crc ^= var_b
            for loop in range(1, 9):
                if crc & 1 == 1:
                    crc = (crc >> 1) ^ 0xa001
                else:
                    crc >>= 1

        return crc



    """ modBus integer to string converter.
    """
    def int2bytes(self, int_val):
        val = int(int_val)
        return b_chr((val >> 8) & 0xff) + b_chr(val & 0xff)


    """ Switch bytes in short-int.
    """
    def switch_endian(self, int_val):
        return ((int_val >> 8) & 0xff) | ((int_val & 0xff) << 8)
