from datetime import datetime
import sys
from influxdb import InfluxDBClient

FNAME = "./temp-export.txt"

HOST = '192.168.178.136'
PORT = 8086
USER = "root"
PASSWORD = "root"
DBNAME = "diematic"
METRIC = "temperatures"
count = 0


if __name__=='__main__':
    client = InfluxDBClient(HOST, PORT, USER, PASSWORD, DBNAME)
    
    if client is not None:

        query = "SELECT * FROM temperatures WHERE time > now() - 7d"
        result = client.query(query, database=DBNAME)

        if result is not None:
            with open(FNAME, "w") as f:
                points = list(result.get_points(measurement='temperatures'))
                for point in points:
                    thetime = datetime.strptime(point['time'], "%Y-%m-%dT%H:%M:%SZ")
                    s = thetime.strftime("%Y-%m-%d %H:%M:%S") + ' ' + \
                        str(point['temp_ext']) + ' ' + \
                        str(point['temp_ecs']) + ' ' + \
                        str(point['temp_boiler'])
                    f.write(s + '\n')
                    count = count + 1
            print("%d lines written" % count)

    else:
        print "couldn't open InfluxDB"
