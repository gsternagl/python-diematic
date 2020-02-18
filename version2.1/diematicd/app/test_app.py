import threading
import atexit
from flask import Flask

POOL_TIME = 5 #Seconds

# variables that are accessible from anywhere
commonDataStruct = {}

# lock to control access to variable
dataLock = threading.Lock()

# thread handler
yourThread = threading.Thread()


def create_app():
    app = Flask(__name__)

    def interrupt():
        global yourThread
        yourThread.cancel()

    def doStuff():
        global commonDataStruct
        global yourThread
        with dataLock:
        # Do your stuff with commonDataStruct Here
            print("I am in thread now")

        # Set the next thread to happen
        yourThread = threading.Timer(POOL_TIME, doStuff, ())
        yourThread.start()   

    def doStuffStart():
        # Do initialisation stuff here
        global yourThread
        # Create your thread
        yourThread = threading.Timer(POOL_TIME, doStuff, ())
        yourThread.start()

    # Initiate
    doStuffStart()
    # When you kill Flask (SIGTERM), clear the trigger for the next thread
    atexit.register(interrupt)
    return app

app = create_app()
#app.run(debug=True, host='0.0.0.0', port=5000)
app.run(host='0.0.0.0', port=5000)


# dump all register data in JSON
@app.route('/dump', methods=['GET'])
def handle_requests():
    """main rout for dumping all registers."""

    buff = json.dumps({'High Gerry!': 7})
    return buff

