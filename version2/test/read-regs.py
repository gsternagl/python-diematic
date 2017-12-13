import json

with open('reg-dump2.json') as data_file:
    data = json.loads(data_file.read())

print data
for idx in data:
    print(data[idx])

