import json

with open('reg-dump.json') as data_file:
    data = json.loads(data_file.read())

print data
