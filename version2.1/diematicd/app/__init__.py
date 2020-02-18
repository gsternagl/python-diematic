#-*- coding: utf-8 -*-
"""  __init__.py

     Daemon for Diematic III maintenance which speaks JSON
     data requests:

     GET:
     1. All registers:
         curl http://127.0.0.1:5000/registers
     2. One register:
         curl http://127.0.0.1:5000/registers/TEMP_EXT

     PUT:
     1. Only one register can be updated at a time:
     curl http://127.0.0.1:5000/registers/TEMP_ECS -H \
        'Content-Type: application/json' \
        -X POST -d '{ \"TEMP_ECS\": [ 45.0 ] }'
"""

import threading
import time
import json
import atexit
from datetime import datetime
import logging
from flask import Flask, request
import config
from .diematic import Diematic

logger = None
regs = {}
UPDT_TIME = 30      # intervals when to update diematic registers

# get a lock to prevent concurrent access to data
dataLock = threading.Lock()

# thread handler
syncerThread = threading.Thread()

# Flask main class
app = Flask(__name__)
app.config.from_object('config')
app.config['PROPAGATE_EXCEPTIONS'] = False


def create_json(reg, arg):
    """ write Diematic registers into a string in JSON-format
        if arg = <None> then dump all registers
        otherwise just dump one register with the name = <arg>.
    """

    buff = ''

    if reg is not None:
        try:
            if arg is None:
                buff = json.dumps(reg, indent=4)
            else:
                buff = json.dumps({arg: reg[arg]}, indent=4)
        except Exception as inst:
            print( type(inst) )
            print(inst.args )
            print(inst )
            buff = json.dumps({'ERROR': 2})
    return buff


def copy_regs(reg1, reg2):
    """ copy registers from downstream to upstream."""
    for idx in reg1:
        reg2.update({idx: reg1[idx]})


def update_reg(reg, val):
    """ update a register by writing the value into the set register."""
    global regs
    global dataLock

    with dataLock:
        regs[reg][Diematic.REG_SET] = val
        regs[reg][Diematic.REG_VAL] = val


def check_data(reg, data):
    """check whether the data is valid."""

    global regs
    data_ok = False
    reg_match = False
    val = None
    idx1 = None

    if data is not None and data != {}:
        for idx1 in data:
            # register name doesn't match HTTP POST API
            if idx1 != reg:
                break
            reg_match = False
            # Search in register list whether posted register exists
            for idx2 in regs:
                if idx1 == idx2:
                    reg_match = True
                    break
            if reg_match:
                break
        if reg_match:
            if data[idx1]:
                val = data[idx1][0]
                data_ok = True
    return data_ok, val


# dump all register data in JSON
@app.route('/registers', methods=['GET'])
def dump_registers():
    """main rout for dumping all registers."""

    global regs

    buff = create_json(regs, None)
    return buff


# GET, PUT, POST one register in JSON
@app.route('/registers/<string:reg>', methods=['GET', 'PUT', 'POST'])
def get_set_register(reg):
    """route for dumping one specific register <reg>."""

    global regs
    found = False

    buff = ""
    for idx in regs:
        if idx == reg:
            found = True
            break
    if found:
        if request.method == 'GET':
            buff = create_json(regs, reg)
        else:
            if request.headers['Content-Type'] == 'application/json':
                data = request.get_json()
                data_ok, val = check_data(reg, data)
                if data_ok:
                    # check whether register can be modified
                    if regs[reg][Diematic.REG_MOD]:
                        update_reg(reg, val)
                        return "Register update OK"
                    return "Attempt to change non-writable Diematic Register"

                return "Data received not OK!"

            return "415 Unsupported Media Type"
    else:
        buff = 'register <' + reg + '> doesn\'t exist'
    return buff

   
def createSyncerTask():

    def interrupt():
        global syncerThread
        syncerThread.cancel()


    def data_producer():
        """ read/write from/to Diematic III and copy into temp registers."""

        global syncerThread
        global dataLock
        global regs
        update_request = False

        # print("data_producer called")
        regulator.synchro()
        # print("data_synchronized")

        with dataLock:
        # check for updated registers
            for idx in regs:
                if regs[idx] is not None:
                    if regs[idx][Diematic.REG_SET] is not None:
                        update_request = True
                        val = regs[idx][Diematic.REG_SET]
                        # print( "Updating Diematic Reg:", idx, " Value: ", val)
                        # reset REG_SET
                        regs[idx][Diematic.REG_SET] = None
                        regulator.diematicReg[idx][Diematic.REG_SET] = val
            if not update_request:
                copy_regs(regulator.diematicReg, regs)

        if update_request:
            regulator.synchro()
            with dataLock:
                copy_regs(regulator.diematicReg, regs)
        
        syncerThread = threading.Timer(UPDT_TIME, data_producer, ())
        syncerThread.start()


    def startSyncerThread():
        global syncerThread
        
        syncerThread = threading.Timer(UPDT_TIME, data_producer, ())
        syncerThread.start()


    # main for createSyncerTask
    startSyncerThread()
    atexit.register(interrupt)
    return  # from createSyncerTask()


def init_logger():
    """ setup our logfile."""

    logging.basicConfig(
        filename=app.config['DIEMATICD_LOGFILE'],
        format='%(name)-12s:%(levelname)-8s %(message)s',
        level=logging.INFO
    )
    logger1 = logging.getLogger('diematicd')
    return logger1


logger = init_logger()
connection = {'type':     app.config['CONN_TYPE'], \
              'device':   app.config['RS485_DEVICE'], \
              'baudrate': app.config['RS485_BAUDRATE'], \
              'ip_addr':  app.config['USR_TCP232_24_IP'], \
              'ip_port':  app.config['USR_TCP232_24_PORT']}

logger.info('started diematicd at: ' + \
            datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
regulator = Diematic(connection, debug=app.config['DIEMATIC_DEBUG'])
copy_regs(regulator.diematicReg, regs)
createSyncerTask()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
