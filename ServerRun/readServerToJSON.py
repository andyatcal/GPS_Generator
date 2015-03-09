import json
import pymssql
import time
from datetime import datetime, timedelta
import numpy as np
import random
import pprint

server = "rhumbix-data.com"
db = "rhumbix_foreman"
user = "rhumbix_foreman_app_user"
pw = "1qaz@WSX3e"
table = "Temp_UserLocation"

conn = pymssql.connect(server, user, pw, db)
c1 = conn.cursor()

c1.execute("SELECT * FROM Temp_UserLocation WHERE USERID = 6;")
data = c1.fetchall()
result = []

for i in range(0, len(data)):
    newEntry = {"workerID": data[i][0], "lat":data[i][1], "lng":data[i][2], "time":str(data[i][3]), "geoFenceID":data[i][4]}
    result.append(newEntry)

with open('data6.json', 'w') as outfile:
    json.dump(result, outfile)