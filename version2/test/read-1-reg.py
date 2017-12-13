#!/usr/bin/python

import json
import urllib2

request = urllib2.Request('http://127.0.0.1:5000/registers/TEMP_EXT')
request.add_header('Content-Type', 'application/json')

response = urllib2.urlopen(request)
resp_str = response.read()

try:
    data = json.loads(resp_str)
except:
    data = {}

if data is not None and data != {}:
    if len(data['TEMP_EXT']) > 4:
        print "The outside Temperature is: ", data['TEMP_EXT'][4]
    else:
        print "Received data but dataset too short"
else:
    print "couldn't read proper data"

