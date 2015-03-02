# Yu Wang (SID: 24106507) from UC Berkeley.
# Need to use pyproj package. Run sudo pip install pyproj in the console.
import pyproj
# import LatLon # maybe use in the future

# Date and time
import time
from datetime import datetime, timedelta

# Vectors for motion
import numpy as np

# Random number
import random

# Write the data to the remote database with pymssql
import json

# Global projection of gps data on x, y coordiante systems (units of meters) of pyproj
# Two examples given in http://all-geo.org/volcan01010/2012/11/change-coordinates-with-pyproj/
# It is a good reference for converting with pyproj.
# This is a projection for Iceland from the reference
# isn2004=pyproj.Proj("+proj=lcc +lat_1=64.25 +lat_2=65.75 +lat_0=65 \
# +lon_0=-19 +x_0=1700000 +y_0=300000 +no_defs +a=6378137 +rf=298.257222101 +to_meter=1")
# LatLon with WGS84 datum used by GPS units and Google Earth
# wgs84=pyproj.Proj("+init=EPSG:4326")

# I found this EPSG for San Francisco on http://epsg.io/6419
sfmap = pyproj.Proj("+init=EPSG:6419")
# The utm projection of San Francisco, an alternative.
# sfmap = pyproj.Proj(proj='utm',zone=10,ellps='WGS84')

# Tests of this sfmap, works good
# x, y = sfmap(-122.398314, 37.7747) # The location of Rhumbix office.
# w, k = sfmap(x, y, inverse = True)
# print(x, y)
# print(w, k)

# A class of GPS data. There are two parameters: longitude
# and latitude.
class GPS():
    def __init__(self, longitude = 0.0, latitude = 0.0):
        assert (longitude <= 180) & (longitude >= -180) \
         & (latitude >= -90) & (latitude <=90)
        self.longitude = longitude
        self.latitude = latitude

    def setGPS(self, longitude, latitude):
        """
        Set the longitude and latitude
        """
        self.longitude = longitude
        self.latitude = latitude

    def getGPS(self):
        """
        Get the longitude and latitude data

        >>> gps1 = GPS()
        >>> gps1.getGPS()
        (0.0, 0.0)
        >>> gps2 = GPS(-122.398314, 37.7747)
        >>> gps2.getGPS()
        (-122.398314, 37.7747)
        """
        return self.longitude, self.latitude

# Worker class contains everything associated with a worker,
# including the ID, last updated location, and others?(active state).
class Worker():
    def __init__(self, workerID, gps = GPS()):
        assert True # ?? Should check the format of workerID
        self.workerID = workerID
        self.gps = gps
        self.velocity = np.array((0, 0))

    def getID(self):
        return self.workerID

    def setID(self, workerID):
        self.workerID = workerID

    def getGPS(self):
        return self.gps.getGPS()

    def setGPS(self, longitude, latitude):
        self.gps.setGPS(longitude, latitude)

    def info(self):
        """
        This function returns the ID and location of worker as a list.
        >>> worker1 = Worker(1, GPS(-122.398314, 37.7747))
        >>> worker1.info()
        [1, 37.7747, -122.398314]
        """
        return [self.workerID, self.gps.latitude, self.gps.longitude]


# Simulator for the motion of worker, generate a list in the form of 
# [[workerID, latitude, longitude, lastUpdateTime, geoFenceID], ...]
class Simulator():
    def __init__(self):
        self.data = [] # This is the data we want in the end
        now = datetime(2015, 2, 22, 20, 53, 10)
        self.time = now.now() # Starting with current time
        self.workerLists = [] # The worker lists we have in this simulation
        self.mapConvert = sfmap # Hard coding with sfmap, will change later

    def update(self, timeIncrement):
        """
        Update time, position, velocity for one unit of time.
        """
        for worker in self.workerLists:
            worker.velocity = np.array((random.uniform(-2.5, 2.5),\
             random.uniform(-2.5, 2.5)))
            lon, lat = worker.getGPS()
            position = np.array(self.mapConvert(lon, lat)) # Can be improved
            position += worker.velocity * (timeIncrement.total_seconds())
            lon, lat = self.mapConvert(position[0], position[1], inverse = True)
            worker.setGPS(lon, lat)
            newEntry = worker.info() + [self.time] + [1] # Geofence hardcoded as 1
            self.data.append(newEntry)
        self.time += timeIncrement

    def SimSingleMoveRandomly(self):
        """
        Simulate a worker walking around with random velocity. Maganitude range from
        0 - 2.5 m/s. 
        """
        # Can simulate mutiple worker walking around. 
        timeIncrement = timedelta(seconds = 15) 
        # Hard coding timeIncrement for 1 second, but can be smaller transmission. 
        worker1 = Worker(1, GPS(-122.398314, 37.7747))
        self.workerLists += [worker1]
        for i in range(0, 100): # Within 1000 seconds
            for worker in self.workerLists:
                worker.velocity = np.array((random.uniform(-2.5, 2.5),\
                 random.uniform(-2.5, 2.5)))
                self.update(timeIncrement)

    def SimMultipleMoveRandomly(self, numWorker = 1):
        """
        Simulate a worker walking around with random velocity. Maganitude range from
        0 - 2.5 m/s. 
        """
        # Can simulate mutiple worker walking around. 
        timeIncrement = timedelta(seconds = 15) 
        # Hard coding timeIncrement for 1 second, but can be smaller transmission.
        for i in range(1, numWorker + 1):
            worker = Worker(i + 4, GPS(-122.398314, 37.7747)) # Worker ID starting from 5.
            self.workerLists += [worker]
        for i in range(0, 1920): # Within 8 hrs
            self.update(timeIncrement)
    
    def result(self):
        return self.data

    def writeToJson(self):
        pass

# Tests of SimSingleMoveRandomly()
sim1 = Simulator()
sim1.SimSingleMoveRandomly()
result = sim1.result()
for entry in result:
    print("new google.maps.LatLng(" + str(entry[1])+", "+str(entry[2])+"),")

# Tests of SimMultipleMoveRandomly()
# Three workers around SF office for 8 hrs.
#sim2 = Simulator()
#sim2.SimMultipleMoveRandomly(3)
#print(sim2.result())

