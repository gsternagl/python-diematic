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
        if arg is None:
            registers_to_dump = reg
        else:
            registers_to_dump = {arg: reg[arg]}

        for idx in registers_to_dump:
            s += json.dumps( { idx: reg[idx] }, indent=4) + "\n"

    return s
    
def copy_r(reg1, reg2):
  for idx in reg1:
    reg_set   = reg1[idx][0]
    reg_addr  = reg1[idx][1]
    reg_type  = reg1[idx][2]
    reg_value = reg1[idx][3]
    reg_min   = reg1[idx][4]
    reg_max   = reg1[idx][5]
    reg2.update( {idx: (reg_set, reg_addr, reg_type, reg_value, reg_min, reg_max)} )

@app.route('/registers', methods=['GET'])
def dump_registers():
    global regs

    s = create_json(regs, None)
    return s

@app.route('/registers/<string:reg>', methods=['GET'])
def dump_register(reg):
    global regs
    found = False

    for idx in regs:
        if idx == reg:
            found = True
            break
    if found:
        s = create_json(regs, reg)
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

        regulator.synchro()
        with dataLock:
            copy_r(regulator.diematicReg, regs)

        updaterThread = threading.Timer(UPDT_TIME, dataProducer, ())
        updaterThread.start()

    def dataProducer_start():
        global updaterThread

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
copy_r(regulator.diematicReg, regs)

app = create_app()
app.run(debug=True)