#!/usr/bin/python

import json
import requests
import os, sys
from time import sleep
from datetime import datetime
from influxdb import InfluxDBClient

REG_NAME    =   0
REG_VAL     =   4
REG_MIN     =   5
REG_MAX     =   6

INFLUXDB_HOST = '127.0.0.1'
PORT          = 8086
USER          = "root"
PASSWORD      = "root"
DBNAME        = "diematic"
MY_RETENTION  = "weekly_policy"
INTERVAL      = 30      # every 30 secs

URL = 'http://192.168.178.21:5000/registers'
headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}

def conv2float(val):
    if val is not None:
        return(float(val))
    else:
        return None

def write_data2db(regs, idb_conn, thedate):
    json_body = [
        {
            "measurement": "temperatures",
            # time in nsec
            "time": int(thedate) * 1000000000,
            "fields": {
                "temp_ext":    conv2float(regs['TEMP_EXT'][REG_VAL]),
                "temp_ecs":    conv2float(regs['TEMP_ECS'][REG_VAL]),
                "temp_boiler": conv2float(regs['TEMP_BOILER'][REG_VAL])
            }
        }
    ]
    try:
        resp = idb_conn.write_points(json_body, retention_policy=MY_RETENTION)
    except:
        print("error writing to InfluxDB")
    return resp

if __name__=='__main__':
        
    conn = InfluxDBClient(INFLUXDB_HOST, PORT, USER, PASSWORD, DBNAME)

    while conn is not None:
        try:
            resp = requests.get(URL, headers=headers)
            error = False
        except:
            pass
            error = True

        if not error and resp.status_code == 200:
            data = resp.json()
            thedate = datetime.now().strftime('%s')
            if data is not None:
                try:
                    if write_data2db(data, conn, thedate) is False:
                        print('Error: couldn\'t write dataset to InfluxDB')
                    else:
                        print(f"data set written at: {thedate}")
                except:
                    print("error writing to influxDB")
            else:
                print('Error: data couldn\'t be read')
                break
        else:
            print('Error: response:' + str(resp.status_code))
            break
        sleep(INTERVAL)

    client.close()


