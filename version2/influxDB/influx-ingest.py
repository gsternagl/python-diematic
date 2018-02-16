from datetime import datetime
import sys
from influxdb import InfluxDBClient

fname = "./temp.txt"

HOST = '127.0.0.1'
PORT = 8086
USER = "root"
PASSWORD = "root"
DBNAME = "diematic"
MY_RETENTION = "weekly_policy"

if len(sys.argv) > 1:
    fname = sys.argv[1]

count = 0
client = InfluxDBClient(HOST, PORT, USER, PASSWORD, DBNAME)
client.create_database(DBNAME)
client.create_retention_policy(MY_RETENTION, '7d', 1, default=True)

def conv2float(val):
    if val is not None:
        return(float(val))
    else:
        return None

if client is None:
    print "couldn't open InfluxDB"
else:
    with open(fname) as f:
	for line in f:
    	    words = line.split()
            mydate = words[0] + ' ' + words[1]
            data_value1 = conv2float(words[2])
            data_value2 = conv2float(words[3])
            data_value3 = conv2float(words[4])
            count = count + 1
            json_body = [
                {
                    "measurement": "temperatures",
                    "time": mydate,
                    "fields": {
                        "temp_ext": data_value1,
                        "temp_ecs": data_value2,
                        "temp_boiler": data_value3
                    }
                }
            ]
            client.write_points(json_body)

        print("written %d datasets to DB") % (count)
