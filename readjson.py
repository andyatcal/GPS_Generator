import json
from pprint import pprint
# need to revise the name of the file here.
with open('test.json') as data_file:    
    data = json.load(data_file)
pprint(data)