import json
from pprint import pprint

with open('data.json') as data_file:
    data_item = json.load(data_file)
pprint(data_item)


