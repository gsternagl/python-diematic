from datetime import datetime
import sys
from influxdb import InfluxDBClient

HOST = '192.168.178.136'
PORT = 8086
USER = "root"
PASSWORD = "root"
DBNAME = "diematic"
metric = "temperatures"
count = 0


if __name__=='__main__':
    client = InfluxDBClient(HOST, PORT, USER, PASSWORD, DBNAME)
    
    if client is not None:

        # First query
        query = 'SELECT mean(temp_ext) FROM temperatures WHERE time > now() - 24h GROUP BY time(1h) fill(null)'
        result = client.query(query, database=DBNAME)
        if result is not None:
            points = list(result.get_points(measurement='temperatures'))

            for point in points:
                val = point['mean']
                s = str(round(val, 2)) if val is not None else ''
                    
                print('%s: %s' % (point['time'], s) )

        # sys.exit(1)

        # Second query
        query = 'SELECT * FROM temperatures WHERE time > now() - 10m'
        result = client.query(query, database=DBNAME)

        if result is not None:
            points = list(result.get_points(measurement='temperatures'))
            for point in points:
                thetime = datetime.strptime(point['time'], "%Y-%m-%dT%H:%M:%SZ")

                print("time: %s, ext: %.2f ww: %.2f boiler: %.2f" % 
                      ( thetime.strftime("%Y-%m-%d %H:%M:%S"),
                        point['temp_ext'], 
                        point['temp_ecs'], 
                        point['temp_boiler']
                       )
                     )

    else:
        print "couldn't open InfluxDB"
