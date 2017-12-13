import json
from pprint import pprint

with open('reg-all-dump1.json') as data_file:
    data_item = json.load(data_file)
pprint(data_item)
