# diematicd: Diematic communication daemon based on flask
For development the required python libraries are stored in a virtualenv
in directory ./flask. For production this can be replaced by system-wide
python packages.

# start with:

./run.py

This outputs the URL you can connect to.

# Test:
curl http://0.0.0.0:5000/registers


curl http://0.0.0.0:5000/registers/TEMP_EXT
