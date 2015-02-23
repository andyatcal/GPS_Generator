# Copyright reserved 2015 Yu Wang (SID: 24106507) from UC Berkeley.
# Need to use pyproj package. Run sudo pip install pyproj in the console.
import pyproj
# import LatLon # maybe use in the future

# Date and time
import time
import datetime

# Vectors for motion
import numpy as np

# Random number
import random

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

# A class of GPS data. There are two parameters: longtitude
# and latitude.
class GPS():
    def __init__(self, longtitude = 0.0, latitude = 0.0):
        assert (longtitude <= 180) & (longtitude >= -180) \
         & (latitude >= -90) & (latitude <=90)
        self.longtitude = longtitude
        self.latitude = latitude

    def setGPS(self, longtitude, latitude):
        """
        Set the longtitude and latitude
        """
        self.longtitude = longtitude
        self.latitude = latitude

    def getGPS(self):
        """
        Get the longtitude and latitude data

        >>> gps1 = GPS()
        >>> gps1.getGPS()
        (0.0, 0.0)
        >>> gps2 = GPS(-122.398314, 37.7747)
        >>> gps2.getGPS()
        (-122.398314, 37.7747)
        """
        return self.longtitude, self.latitude

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

    def setGPS(self, longtitude, latitude):
        self.gps.setGPS(longtitude, latitude)

    def info(self):
        """
        This function returns the ID and location of worker as a list.
        >>> worker1 = Worker(1, GPS(-122.398314, 37.7747))
        >>> worker1.info()
        [1, 37.7747, -122.398314]
        """
        return [self.workerID, self.gps.latitude, self.gps.longtitude]


# Simulator for the motion of worker, generate a list in the form of 
# [[workerID, latitude, longtitude, lastUpdateTime, geoFenceID], ...]
class Simulator():
    def __init__(self):
        self.data = [] # This is the data we want in the end
        self.time = 0 # Hard coding with 0, will change to Datatime later
        self.workerLists = [] # The worker lists we have in this simulation
        self.mapConvert = sfmap # Hard coding with sfmap, will change later

    def update(self, timeIncrement):
        """
        Update time, position, velocity for one unit of time.
        """
        for worker in self.workerLists:
            lon, lat = worker.getGPS()
            position = np.array(self.mapConvert(lon, lat)) # Can be improved
            position += worker.velocity * timeIncrement
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
        timeIncrement = 1 # Hard coding timeIncrement for 1 second, but can be smaller transmission. 
        worker1 = Worker(1, GPS(-122.398314, 37.7747)) # Initial Position set to be our office.
        self.workerLists += [worker1]
        while self.time < 1000:
            for worker in self.workerLists:
                worker.velocity = np.array((random.uniform(-2.5, 2.5), random.uniform(-2.5, 2.5)))
                self.update(timeIncrement)

    def result(self):
        return self.data

sim = Simulator()
sim.SimSingleMoveRandomly()
print(sim.result())
