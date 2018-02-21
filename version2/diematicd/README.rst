diematicd
=========
Diematic communication daemon based on python-flask.
For development the required python libraries are stored in a virtualenv
in directory ./flask. For production this can/should be replaced by system-wide
installed python packages.

start with
----------

* ./run.py

This outputs the URL you can connect to.




Test the diematicd with http requests
-------------------------------------

* curl http://0.0.0.0:5000/registers
* curl http://0.0.0.0:5000/registers/TEMP_EXT
