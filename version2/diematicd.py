import threading
import time
import json
import atexit
from flask import Flask, request
from flask_restful import Resource, Api
from Diematic import Diematic

regs = {}
UPDT_TIME = 30

# get a lock to prevent concurrent access to data
dataLock = threading.Lock()

# thread handler
updaterThread = threading.Thread()

# Flask main class
app = Flask(__name__)
app.config['PROPAGATE_EXCEPTIONS'] = False

# write Diematic registers into a string in JSON-format
# if arg = <None> then dump all registers
# otherwise just dump one register with the name = <arg>

def create_json(reg, arg):
    s = ''

    if reg is not None:
        try:
            if arg is None:
                s = json.dumps(reg, indent = 4)
            else:
                s = json.dumps({ idx: reg[idx] }, indent = 4)
        except:
            s = json.dumps({'ERROR': 2})
    return s
    
def copy_regs(reg1, reg2):
  for idx in reg1:
    reg2.update( { idx: reg1[idx] } )

def update_reg(reg, val):
    global regs

    regs[reg][Diematic.REG_SET] = val

def check_data(reg, data):
    global regs
    data_ok = False
    reg_match = False
    val = None

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
            if len(data[idx1]) > 0:
                val = data[idx1][0]
                data_ok = True
    return data_ok, val


# dump all register data in JSON
@app.route('/registers', methods=['GET'])
def dump_registers():
    global regs
    
    s = create_json(regs, None)
    return s

# GET, PUT, POST one register in JSON
@app.route('/registers/<string:reg>', methods=['GET', 'PUT', 'POST'])
def dump_register(reg):
    global regs
    found = False

    s = ""
    for idx in regs:
        if idx == reg:
            found = True
            break
    if found:
        if request.method == 'GET':
            s = create_json(regs, reg)
        else:
            if request.headers['Content-Type'] == 'application/json':
                data = request.get_json()
                data_ok, val = check_data(reg, data)
                if data_ok:
                    if regs[reg][Diematic.REG_MOD]:
                        update_reg(reg, val)
                        return "OK"
                    else:
                        return "Not a writable Diematic Register"
                else:
                    return "Data received not OK!"
            else:
                return "415 Unsupported Media Type"
    else:
        s = 'register <' + reg + '> doesn\'t exist'
    return s

def create_app():

    def interrupt():
        global updaterThread
        updaterThread.cancel()
        
    def dataProducer():
        global updaterThread
        global dataLock
        global regs
        update_request = False

        regulator.synchro()
        with dataLock:
            # check for updated registers
            for idx in regs:
                if regs[idx] is not None:
                    if regs[idx][Diematic.REG_SET] is not None:
                        update_request = True
                        val = regs[idx][Diematic.REG_SET]
                        # print "Updating Diematic Reg:", idx, " Value: ", val
                        # reset REG_SET 
                        regs[idx][Diematic.REG_SET] = None
                        regulator.diematicReg[idx][Diematic.REG_SET] = val
            if not update_request:
                copy_regs(regulator.diematicReg, regs)

        if update_request:
            regulator.synchro()
            with dataLock:
                copy_regs(regulator.diematicReg, regs)

        updaterThread = threading.Timer(UPDT_TIME, dataProducer, ())
        updaterThread.start()

    def dataProducer_start():
        global updaterThread

        # do first sync quickly so that we have some data
        updaterThread = threading.Timer(UPDT_TIME, dataProducer, ())
        updaterThread.start()

    dataProducer_start()
    atexit.register(interrupt)
    return app
    
connection = { 'type': 'socket', \
               'device': '/dev/ttyAMA0', \
               'baudrate': 9600, \
               'ip_addr': '192.168.178.160', 'ip_port': 20108 }

regulator = Diematic(connection, debug=False)
copy_regs(regulator.diematicReg, regs)

app = create_app()
app.run(debug=True)
