import threading
import time
import atexit
from flask import Flask
from flask_restful import Resource, Api
import json

POOL_TIME = 5 #Seconds

# variables that are accessible from anywhere
regs = {  'CTRL':   (0, 0, 0, 0), \
          'HOUR':   (1, 1, 1, 1), \
          'MINUTE': (2, 2, 2, 2),\
          'COUNTER':(0, 0, 0, 0) }



# lock to control access to variable
dataLock = threading.Lock()
# thread handler
updaterThread = threading.Thread()

class DumpRegisters(Resource):
    def get(self):
        global regs

        s = json.dumps(regs, indent=4)
        return s

class DumpRegister(Resource):
    def get(self, reg):
        global regs

        r = regs[reg]
        return json.dumps(r, indent=4)

def create_app():
    app = Flask(__name__)
    api = Api(app)
    api.add_resource(DumpRegister,  '/registers/<string:reg>')
    api.add_resource(DumpRegisters, '/registers')


    def interrupt():
        global updaterThread
        updaterThread.cancel()

    def doStuff():
        global regs
        global updaterThread
        with dataLock:
            cnt = regs['COUNTER'][0]
            cnt += 1
            regs.update( {'COUNTER': (cnt, 0, 0, 0) } )
#            print ("Register", regs)

        # Set the next thread to happen
        updaterThread = threading.Timer(POOL_TIME, doStuff, ())
        updaterThread.start()   

    def doStuffStart():
        # Do initialisation stuff here
        global updaterThread
        # Create your thread
        updaterThread = threading.Timer(POOL_TIME, doStuff, ())
        updaterThread.start()

    # Initiate
    doStuffStart()
    # When you kill Flask (SIGTERM), clear the trigger for the next thread
    atexit.register(interrupt)
    return app

app = create_app()          
app.run()
