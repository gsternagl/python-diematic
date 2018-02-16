#!/usr/bin/python
#-*- coding: utf-8 -*-

from datetime import date, time, datetime
from time import sleep
from ModBus import ModBus
from Logger import TimestampLogger
from time import time as mytime

class Diematic:
  # Address
  regulatorAddress  = 0x0a
  slaveAddress      = 0
  
  # ModBus Register Types
  INTEGER  = 1
  REAL10   = 2
  BIT      = 3

  # Diematic Mode
  AUTO          = 8
  TEMP_DAY      = 36
  TEMP_NIGHT    = 34
  PERM_DAY      = 4
  PERM_NIGHT    = 2
  ANTIICE       = 1

  # Bus Modes
  SLAVE  = 0
  MASTER = 1

  # log 
  log = None

  # status to remember if the regulator is connected
  modBus = None
  last_sync = None

  #                             set,  addr, type,     value
  diematicReg = { \
    	'CTRL': 		(None, 3,   INTEGER,  0), \
     	'HOUR':			(None, 4,   INTEGER,  0), \
    	'MINUTE':		(None, 5,   INTEGER,  0), \
    	'WEEKDAY':		(None, 6,   INTEGER,  0), \
    	'TEMP_EXT':		(None, 7,   REAL10,   0.0), \
    	'CONS_SUMWIN':		(None, 8,   REAL10,   0.0), \
    	'NB_DAY_ANTIICE':	(None, 13,  INTEGER,  0), \
    	'CONS_DAY_A':     	(None, 14,  REAL10,   0.0), \
    	'CONS_NIGHT_A':   	(None, 15,  REAL10,   0.0), \
    	'CONS_ANTIICE_A': 	(None, 16,  REAL10,   0.0), \
    	'MODE_A':         	(None, 17,  BIT,      0x0), \
    	'TEMP_AMB_A':     	(None, 18,  REAL10,   0.0), \
    	'STEEPNESS_A':     	(None, 20,  REAL10,   0.0), \
    	'TCALC_A':        	(None, 21,  REAL10,   0.0), \
    	'CONS_DAY_B':     	(None, 23,  REAL10,   0.0), \
    	'CONS_NIGHT_B':   	(None, 24,  REAL10,   0.0), \
    	'CONS_ANTIICE_B': 	(None, 25,  REAL10,   0.0), \
    	'STEEPNESS_B': 	        (None, 29,  REAL10,   0.0), \
    	'CONS_ECS_DAY':       	(None, 59,  REAL10,   0.0), \
    	'TEMP_ECS':       	(None, 62,  REAL10,   0.0), \
        'MIN_BOILER':           (None, 70,  REAL10,   0.0), \
        'MAX_BOILER':           (None, 71,  REAL10,   0.0), \
        'CONS_BOILER':          (None, 74,  REAL10,   0.0), \
    	'TEMP_BOILER':      	(None, 75,  REAL10,   0.0), \
    	'BASE_ECS':       	(None, 89,  BIT,      0x0), \
    	'CONS_ECS_NIGHT': 	(None, 96,  REAL10,   0.0), \
    	'DAY':            	(None, 108, INTEGER,  0), \
    	'MONTH':          	(None, 109, INTEGER,  0), \
    	'YEAR':           	(None, 110, INTEGER,  0), \
    	'WATER_PRESSURE': 	(None, 456, REAL10,   0.0), \
    	'ALARM':          	(None, 465, BIT,      0x0) }

  # class constructor
  def __init__(self, conn, debug=False):
    self.debug = debug
    self.conn = conn
    if debug:
      self.logger = TimestampLogger()

  def reg_isset(self, reg, key):
    return (True if reg[key][0] is not None else False)

  def reg_unset(self, reg, key):
    reg_set   = None
    reg_addr  = reg[key][1]
    reg_type  = reg[key][2]
    reg_value = reg[key][3]
    reg.update( {key: (reg_set, reg_addr, reg_type, reg_value)} )

  def reg_set(self, reg, key, set_val):
    reg_set   = int(set_val)
    reg_addr  = reg[key][1]
    reg_type  = reg[key][2]
    reg_value = reg[key][3]
    reg.update( {key: (reg_set, reg_addr, reg_type, reg_value)} )

  def reg_getset(self, reg, key):
    reg_set = reg[key][0]
    return reg_set
  
  def dataDecode(self, modBusReg):
    for key in modBusReg:
      value = modBusReg[key]
      for reg in self.diematicReg:
        reg_set   = self.diematicReg.get(reg)[0]
        reg_addr  = self.diematicReg.get(reg)[1]
        reg_type  = self.diematicReg.get(reg)[2]
        if reg_addr == key:
          if reg_type == self.REAL10:
            reg_value = value * 0.1
          elif reg_type == self.INTEGER:
            reg_value = value
          elif reg_type == self.BIT:
            reg_value = value & 0xffff
           
          self.diematicReg.update({reg: (reg_set, reg_addr, reg_type, reg_value) } )
          break

  def check_transmit_registers(self):
    # mode setting
    if self.reg_isset(self.diematicReg, 'MODE_A'):

      # varying request mode
      if self.reg_getset(self.diematicReg, 'MODE_A') != self.ANTIICE:
	self.modBus.masterTx(self.regulatorAddress, self.diematicReg['MODE_A'])
	if self.debug:
	  self.logger.log(self.modBus.log)
	self.reg_unset(self.diematicReg, 'MODE_A')

	self.reg_set(self.diematicReg, 'NB_DAY_ANTIICE', 0)
	self.modBus.masterTx(self.regulatorAddress, self.diematicReg['NB_DAY_ANTIICE'])
	if self.debug:
	  self.logger.log(self.modBus.log)
	self.reg_unset(self.diematicReg, 'NB_DAY_ANTIICE')
      else:
	self.modBus.masterTx(self.regulatorAddress, self.diematicReg['NB_DAY_ANTIICE'])
	if self.debug:
	  self.logger.log(self.modBus.log)
	self.reg_unset(self.diematicReg, 'NB_DAY_ANTIICE')

    # time setting
    if self.reg_isset(self.diematicReg, 'HOUR'):
      register = { 0: self.diematicReg['HOUR'], \
		   1: self.diematicReg['MINUTE'], \
		   2: self.diematicReg['WEEKDAY'] }
      self.modBus.masterTxN(self.regulatorAddress, register)
      if self.debug:
	self.logger.log(self.modBus.log)
      self.reg_unset(self.diematicReg, 'HOUR')
      self.reg_unset(self.diematicReg, 'MINUTE')
      self.reg_unset(self.diematicReg, 'WEEKDAY')
      register = {}

    if self.reg_isset(self.diematicReg, 'DAY'):
      register = { 0: self.diematicReg['DAY'], \
		   1: self.diematicReg['MONTH'] }
      self.modBus.masterTxN(self.regulatorAddress, register)
      if self.debug:
	self.logger.log(self.modBus.log)
      self.reg_unset(self.diematicReg, 'DAY')
      self.reg_unset(self.diematicReg, 'MONTH')
      register = {}

    # temperature setting circuit A
    if self.reg_isset(self.diematicReg,'CONS_DAY_A'):
      register = { 0: self.diematicReg['CONS_DAY_A'], \
		   1: self.diematicReg['CONS_NIGHT_A'], \
		   2: self.diematicReg['CONS_ANTIICE_A'] }
      self.modBus.masterTxN(self.regulatorAddress, register)
      if self.debug:
	self.logger.log(self.modBus.log)
      self.reg_unset(self.diematicReg, 'CONS_DAY_A')
      self.reg_unset(self.diematicReg, 'CONS_NIGHT_A')
      self.reg_unset(self.diematicReg, 'CONS_ANTIICE_A')
      register = {}
    
    # circuit A curve steepness 
    if self.reg_isset(self.diematicReg, 'STEEPNESS_A'):
      register = { 0: self.diematicReg['STEEPNESS_A'] }
      self.modBus.masterTx(self.regulatorAddress, register)
      if self.debug:
	self.logger.log(self.modBus.log)
      self.reg_unset(self.diematicReg, 'STEEPNESS_A')
      register = {}
    
    # temperature setting circuit B
    if self.reg_isset(self.diematicReg,'CONS_DAY_B'):
      register = { 0: self.diematicReg['CONS_DAY_B'], \
		   1: self.diematicReg['CONS_NIGHT_B'], \
		   2: self.diematicReg['CONS_ANTIICE_B'] }
      self.modBus.masterTxN(self.regulatorAddress, register)
      if self.debug:
	self.logger.log(self.modBus.log)
      self.reg_unset(self.diematicReg, 'CONS_DAY_B')
      self.reg_unset(self.diematicReg, 'CONS_NIGHT_B')
      self.reg_unset(self.diematicReg, 'CONS_ANTIICE_B')
      register = {}
    
    # circuit B curve steepness 
    if self.reg_isset(self.diematicReg, 'STEEPNESS_B'):
      register = { 0: self.diematicReg['STEEPNESS_B'] }
      self.modBus.masterTx(self.regulatorAddress, register)
      if self.debug:
	self.logger.log(self.modBus.log)
      self.reg_unset(self.diematicReg, 'STEEPNESS_B')
      register = {}

    # ECS temperature setting
    if self.reg_isset(self.diematicReg, 'CONS_ECS_DAY'):
      register = { 0: self.diematicReg['CONS_ECS_DAY'] }
      self.modBus.masterTx(self.regulatorAddress, register)
      if self.debug:
	self.logger.log(self.modBus.log)
      self.reg_unset(self.diematicReg, 'CONS_ECS_DAY')
      register = {}

    # ECS night temperature setting
    if self.reg_isset(self.diematicReg, 'CONS_ECS_NIGHT'):
      register = { 0: self.diematicReg['CONS_ECS_NIGHT'] }
      self.modBus.masterTx(self.regulatorAddress, register)
      if self.debug:
	self.logger.log(self.modBus.log)
      self.reg_unset(self.diematicReg, 'CONS_ECS_NIGHT')
      register = {}
    
    # Summer/Winter temperature setting
    if self.reg_isset(self.diematicReg, 'CONS_SUMWIN'):
      register = { 0: self.diematicReg['CONS_SUMWIN'] }
      self.modBus.masterTx(self.regulatorAddress, register)
      if self.debug:
	self.logger.log(self.modBus.log)
      self.reg_unset(self.diematicReg, 'CONS_SUMWIN')
      register = {}


  # exchange data with regulator
  def synchro(self):
    if self.modBus is not None:
      del self.modBus

    # open new connection
    self.modBus = ModBus(self.slaveAddress, self.conn)

    if self.modBus.conn_fp is None:
      raise RuntimeError("Can't create ModBus connection")

    if self.debug:
      self.logger.log("Connection Status: " + str(self.modBus.status) + "\n")
      
    busStatus = self.SLAVE
    silentDetection = -1
    i = 0

    while i<500:
      # slave mode
      if busStatus == self.SLAVE:
        # log
        if self.debug:
          self.logger.log("Index:"+str(i)+" Bus Status : Slave Silence Detection :"+str(silentDetection)+"\n")

        # get data sent to me, if available
        self.modBus.slaveRx()
        if self.debug:
          self.logger.log(self.modBus.log)

        # arm silent detection on first frame received
        if silentDetection == -1 and (self.modBus.status == ModBus.FRAME_OK or 
                                      self.modBus.status == ModBus.NOT_SUPPORTED_FC):
          silentDetection = 0

        # update silent detection following context
        if silentDetection >= 0:
          if self.modBus.status == ModBus.FRAME_EMPTY or \
             self.modBus.status == ModBus.READ_FAILED:
            silentDetection += 1
          else:
            silentDetection = 0

        # decode register if necessary
        if self.modBus.status == ModBus.FRAME_OK:
          self.dataDecode(self.modBus.rxReg)

        # update bus status if no traffic during 1sec
        if silentDetection >= 10:
          busStatus = self.MASTER

        # or wait 100ms
        sleep(0.1)
        i += 1
      # master mode  
      else:
        if self.debug:
          self.logger.log("Index:"+ str(i) +" Bus Status : Master \n")
       
        # check whether any registers are set for transmission and transmit 
        self.check_transmit_registers()

        # get 63 registers starting at reg 1
        self.modBus.masterRx(self.regulatorAddress, 1, 63)
        if self.debug:
          self.logger.log(self.modBus.log)
        if self.modBus.status == ModBus.FRAME_OK:
          self.dataDecode(self.modBus.rxReg)

        # get 64 registers starting at reg 64
        self.modBus.masterRx(self.regulatorAddress, 64, 64)
        if self.debug:
          self.logger.log(self.modBus.log)
        if self.modBus.status == ModBus.FRAME_OK:
          self.dataDecode(self.modBus.rxReg)
       
        # set bus status in slave mode and re-arm silent detection
        busStatus = self.SLAVE
        silentDetection = -1

        # end loop
        i = 500

    # close connection by deleting modBus object
    del self.modBus

  def setMode(self, mode, nb_day_antiice, mode_ecs):
    # if mode value is OK, prepare register to be updated
    if mode == self.TEMP_DAY or \
       mode == self.TEMP_NIGHT or \
       mode == self.AUTO or \
       mode == self.PERM_DAY or \
       mode == self.PERM_NIGHT:
      self.reg_set(self.diematicReg, 'MODE_A',  mode & 0x2f | mode_ecs & 0x50 )
      self.reg_set(self.diematicReg, 'NB_DAY_ANTIICE', 0)

    # if the selected mode is ANTIICE, if the $nb_day_antigel value is OK
    elif mode == self.ANTIICE:
      # set ECS mode
      self.reg_set(self.diematicReg, 'MODE_A', mode & 0x2f)

      # if day number not in 1..99 set it to 1
      if not 1 <= nb_day_antiice <= 99:
        nb_day_antiice = 1
      self.reg_set(self.diematicReg, 'NB_DAY_ANTIICE', nb_day_antiice)

    if self.debug:
      self.logger.log("Mode :" + str(self.reg_getset(self.diematicReg, 'MODE_A')) + \
                    " Nb Days Antigel :" + \
                    str(self.reg_getset(self.diematicReg, 'NB_DAY_ANTIICE')) + "\n")

  # Set temperature for circuit A
  def setTemp_A(self, day, night, antiIce):
    self.reg_set(self.diematicReg, 'CONS_DAY_A',     (min(max(int(2 * day)    * 5, 100), 300)))
    self.reg_set(self.diematicReg, 'CONS_NIGHT_A',   (min(max(int(2 * night)  * 5, 100), 300)))
    self.reg_set(self.diematicReg, 'CONS_ANTIICE_A', (min(max(int(2 * antiIce)* 5, 5),   200)))
  
  # Set temperature for circuit B
  def setTemp_B(self, day, night, antiIce):
    self.reg_set(self.diematicReg, 'CONS_DAY_B',     (min(max(int(2 * day)    * 5, 100), 300)))
    self.reg_set(self.diematicReg, 'CONS_NIGHT_B',   (min(max(int(2 * night)  * 5, 100), 300)))
    self.reg_set(self.diematicReg, 'CONS_ANTIICE_B', (min(max(int(2 * antiIce)* 5, 5),   200)))

  def setEcsTemp(self, day, night):
    self.reg_set(self.diematicReg, 'CONS_ECS_DAY',   (min(max(int(day/5)   * 50, 400), 800)))
    self.reg_set(self.diematicReg, 'CONS_ECS_NIGHT', (min(max(int(night/5) * 50, 100), 800)))
  
  def setSteepness(self, steepness_a, steepness_b):
    self.reg_set(self.diematicReg, 'STEEPNESS_A',    (min(max(int(steepness_a * 10), 0), 40)))
    self.reg_set(self.diematicReg, 'STEEPNESS_B',    (min(max(int(steepness_b * 10), 0), 40)))
  
  def setSumWinTemp(self, sum_win_temp):
    # set the temperature for Summer/Winter AUTO switch
    self.reg_set(self.diematicReg, 'CONS_SUMWIN',    (min(max(int(2*sum_win_temp * 5), 150), 300)))

  def setTime(self):
    # if the mode value is OK, prepare the register to be updated
    today = datetime.today()
    time  = datetime.now()

    self.reg_set(self.diematicReg, 'HOUR',    ( 0xff00 | time.hour ))
    self.reg_set(self.diematicReg, 'MINUTE',  ( 0xff00 | time.minute ))
    self.reg_set(self.diematicReg, 'WEEKDAY', ( 0xff00 | today.isoweekday() ))
    self.reg_set(self.diematicReg, 'DAY',     ( 0xff00 | today.day ))
    self.reg_set(self.diematicReg, 'MONTH',   ( 0xff00 | today.month ))
    self.reg_set(self.diematicReg, 'YEAR',    ( 0xff00 | int(today.strftime("%y")) ))


