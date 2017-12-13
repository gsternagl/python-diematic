#!/usr/bin/python

import json
import urllib

hres = urllib.urlopen('http://time.jsontest.com')
data = json.loads(hres.read().decode("utf-8"))

#print("Data=", data)
print("Type(data)=", type(data))
print data

s = json.dumps(data, indent=4)

print("Type(s)=", type(s))
print(s)

