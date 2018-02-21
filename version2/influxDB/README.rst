Diematic timeseries recorder
============================

This little python script talks to **diematicd** every 30 secs and stores the values into a time series database with InfluxDB.

Run the following command in the background to ingest time-series data into an InfluxDB Server:

* python aufz-diem-influx.py &


Ideally this should be done with setting up a systemd service.

Tunables
--------

In the main python-script aufz-diem-influx.py you can set different values:

* *INTERVAL*: time in secs between reading and storing measures.
* *MY_RETENTION*: how long to keep the values in InfluxDB, currently 1 week

There are some more parameters for the InfluxDB access like user, pw, port, IP, etc. They are pretty self-explaining.
