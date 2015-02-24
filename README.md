# GPS_Generator
Generate GPS data for worker's motion.
Right now. It generates people walking starting at 444 Townsend St. SF. 
Time interval set to be 15s and speed is a random number from 0 - 2.5 m/s in either x or y direction.
It commits simulation results to the database, with the format of [[USERID, LAT, LNG, UPDATETIME, GEOFENCE]...], where the geofence is hard coded to be just 1. 
