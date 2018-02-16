from datetime import datetime
import sys
from influxdb import InfluxDBClient

FNAME = "./temp-export.txt"

HOST       = '192.168.178.136'
PORT       = 8086
USER       = "root"
PASSWORD   = "root"
DBNAME     = "diematic"
NEW_DBNAME = "diematic1"
TABLE      = "temperatures"
RETENTION  = "weekly_policy"
count = 0

def conv2float(val):
    if val is not None:
        return(float(val))
    else:
        return None

if __name__=='__main__':
    client = InfluxDBClient(HOST, PORT, USER, PASSWORD, DBNAME)
    
    if client is not None:

        #query = "SELECT * FROM {}".format(TABLE)
        query = "SELECT * FROM {} WHERE time > now() - 7d".format(TABLE)
        result = client.query(query, database=DBNAME)

        if result is not None:
            newpoints = []
            points = list(result.get_points(measurement=TABLE))
            for point in points:
                thetime = datetime.strptime(point['time'], "%Y-%m-%dT%H:%M:%SZ")

                # time since epoch in nsec.
                t = int(thetime.strftime("%s")) * 1000000000

                newpoint = {
                    "measurement": TABLE,
                    "time": t,
                    "fields": {
                        "temp_ext":    conv2float(point['temp_ext']),
                        "temp_ecs":    conv2float(point['temp_ecs']),
                        "temp_boiler": conv2float(point['temp_boiler'])
                    }
                }
                newpoints.append(newpoint)
                count = count + 1
            
            client.drop_database(NEW_DBNAME)
            client.create_database(NEW_DBNAME)
            client.switch_database(NEW_DBNAME)
            client.create_retention_policy(RETENTION, '7d', 1, default=True)
            client.switch_user(USER, PASSWORD)
            
            result = client.write_points(newpoints)
            if result is not None:
                print("%d records written into DB >%s<" % (count, NEW_DBNAME))
            


    else:
        print "couldn't open InfluxDB"
