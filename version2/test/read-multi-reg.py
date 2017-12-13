#!/usr/bin/python

import json
import urllib2
import sys

request = urllib2.Request('http://127.0.0.1:5000/registers')
request.add_header('Content-Type', 'application/json')

try:
    response = urllib2.urlopen(request, timeout=4)
    resp_str = response.read()
except:
    print "problem reading from URL"
    sys.exit()

print "response str=", resp_str

if len(resp_str) > 0:
    try:
        data = json.loads(resp_str)
    except:
        print "error decoding data"
        data = {}

    if data is not None and data != {}:
        for idx in data:
            print "Register: ", idx, ", data: ", data[idx]
    else:
        print "couldn't read proper data"
else:
    print "no proper response received"

