import pyspark
import pymongo
from pyspark.sql.functions import *

import numpy as np
import pymongo
import datetime, time
from datetime import datetime
import os

from functions.Resample import *
from functions.PowerCalculation import *


def getDays(df):
    daysDF = []

    days= [x.YMD for x in df.withColumn("YMD", date_format(df.Date, "yyyy MM dd")).select("YMD").distinct().sort("YMD").collect()]

    return days 

def getDaysDF(df, days):
    days_array = []

    for day in days:
        temp = df.withColumn("YMD", date_format(df.Date, "yyyy MM dd"))
        temp = temp.filter(temp.YMD == day)
        days_array.append(temp.drop("YMD"))

    return days_array

def cleanDF(df):
    return df.select("Date", "Latitude", "Longitude", "Speed").dropDuplicates().sort("Date").withColumnRenamed("Speed", "Velocity")

def getISODate(df):
    return np.array([x.Date.isoformat() + "Z" for x in df.select("Date").collect()])

class Tag:
    def __init__(self, numPlate):
        self.numPlate = numPlate
    def getLatTag(self):
        return self.numPlate + "_lat"
    def getVelocityTag(self):
        return self.numPlate + "_V"
    def getLngTag(self):
        return self.numPlate + "_lng"
    def getNumPlate(self):
        return self.numPlate
    def getAccTag(self):
        return self.numPlate + "_acc"
    def getPowerTag(self):
        return self.numPlate + "_pow"
    def getElevationTag(self):
        return self.numPlate + "_elv"
    def getAnglesTag(self):
        return self.numPlate + "_ang"
    def getDispTag(self):
        return self.numPlate + "_disp"
    def getCumTag(self):
        return self.numPlate + "_cum"



class Vehicle:
    def __init__(self, vehicleRegistration, df):
            self.tag = Tag(vehicleRegistration)
            self.df = df


    def getDate(self):
        return [x.Date for x in self.df.select("Date").collect()]

    def getParameter(self, param):
        match param:
            case "Latitude":
                return np.array([x.Latitude for x in self.df.select("Latitude").collect()])
            case "Longitude":
                return np.array([x.Longitude for x in self.df.select("Longitude").collect()])
            case "Velocity":
                return np.array([x.Velocity for x in self.df.select("Velocity").collect()])
            case _:
                return None
        
    def resample(self):
        group = self.df.withColumn("Minute", minute(self.df.Date)).groupBy('Minute', window("Date", "10 seconds")).agg(
            mean("Velocity").alias("Velocity"),
            mean("Longitude").alias("Longitude"),
            mean("Latitude").alias("Latitude"),
        )


        df_resampled = group.withColumn("Start", group.window.start).withColumn("End", group.window.end).sort("Start")
        df_resampled = df_resampled.withColumn("Date",from_unixtime((unix_timestamp(df_resampled.Start) + unix_timestamp(df_resampled.End))/2, "yyyy-MM-dd HH:mm:ss"))
        df_resampled = df_resampled.select("Date", "Start", "End", "Velocity", "Latitude", "Longitude").withColumn("Date", to_timestamp(df_resampled.Date, "yyyy-MM-dd HH:mm:ss"))
        self.df = df_resampled

        return

    def setParameters(self):
        pass
    
    def noneToMean(self, array):
        
        for i,x in enumerate(array):
            
            if x == None:  
                array[i] = np.mean(array[i-5:i])
        return array

    def getRegularTimestep(self):
        v = self.noneToMean(self.getParameter("Velocity"))
        lat = self.noneToMean(self.getParameter("Latitude"))
        lng = self.noneToMean(self.getParameter("Longitude"))
        return resampleAll(getTimestampArr(self.getDate()), list(v), list(lat), list(lng))
    
class ExportStop:
    def __init__(self,carReg, SP):
        self.SP = SP
        self.carReg = carReg
        
    def generateTag(self, i, start):
        
        start = start.strftime("%Y%m%d")

        tag = f'{self.carReg}_{start}_{i}'
        return tag
    def getObjects(self):
        entry = []
        
        for i,s in enumerate(self.SP):
            
            tag = self.generateTag(i,s[2])
            
            stopInfo = {
                "VehicleRegistration": self.carReg,
                "start":s[2],
                "end":s[3],
                "latitude":s[0],
                "longitude":s[1],
                "duration": datetime.timestamp(s[3])-datetime.timestamp(s[2]),
                "stopNumber": i
            }
            entry.append(stopInfo)

        return entry
    
    def exportMongoDB(self, collection):

        try:
            x = collection.insert_many(self.getObjects())
            print(x)

        except Exception as e:
            print("Issue exporting to MongoDB")
            print(e)
            
            
            
class ExportTrip:

    def __init__(self, vehicleRegistration, trips):
        self.trips = trips
        self.vehicleRegistration = vehicleRegistration

    def generateTag(self, i, start):
        
        start = start.strftime("%Y%m%d")

        tag = f'{self.vehicleRegistration}_{start}_{i}'
        return tag


    def getObjects(self):
        
        entry = []
        for i,trip in enumerate(self.trips):

            tag = self.generateTag(i,trip[0])
            
            tripInfo = {
                "VehicleRegistration":self.vehicleRegistration,
                "start": trip[0],
                "end": trip[1],
                "duration": trip[2],
                "distance": trip[3],
                "energy": trip[4],
                "aveVelocity": trip[5],
                "tripNumber": i
            }
            

            entry.append(tripInfo)

        return entry

    def exportMongoDB(self, collection):

        try:
            x = collection.insert_many(self.getObjects())
            print(x)

        except Exception as e:
            print("Issue exporting to MongoDB")
            print(e)




class ExportPower:
    def __init__(self, v_reg, time, velocity, lat, lng, acc, power, elevation, angles, s, c):
        self.v_reg = Tag(v_reg)
        self.time = time
        self.velocity = velocity
        self.lat = lat
        self.lng = lng
        self.acc = acc
        self.power = power
        self.elevation = elevation
        self.angles = angles
        self.s = s 
        self.c = c 

    def getVelocity(self):

        res = []

        tag = self.v_reg.getVelocityTag()

        for i,v in enumerate(self.velocity):

            x = {
            "tag": tag,
            "timestamp": datetime.fromtimestamp(self.time[i]),
            "value": float(v)
            }

            res.append(x)

        return res

    def getLatitude(self):

        res = []

        tag = self.v_reg.getLatTag()

        for i,l in enumerate(self.lat):

            x = {
            "tag": tag,
            "timestamp": datetime.fromtimestamp(self.time[i]),
            "value": l
            }

            res.append(x)

        return res

    def getLongitude(self):

        res = []

        tag = self.v_reg.getLngTag()

        for i,l in enumerate(self.lng):

            x = {
            "tag": tag,
            "timestamp": datetime.fromtimestamp(self.time[i]),
            "value": l
            }

            res.append(x)

        return res

    def getPower(self):

        res = []

        tag = self.v_reg.getPowerTag()

        for i,p in enumerate(self.power):

            x = {
            "tag": tag,
            "timestamp": datetime.fromtimestamp(self.time[i]),
            "value": p
            }

            res.append(x)

        return res

    def getAcceleration(self):

        res = []

        tag = self.v_reg.getAccTag()

        for i,a in enumerate(self.acc):

            x = {
            "tag": tag,
            "timestamp": datetime.fromtimestamp(self.time[i]),
            "value": a
            }

            res.append(x)

        return res

    def getElevation(self):

        res = []

        tag = self.v_reg.getElevationTag()

        for i,e in enumerate(self.elevation):

            x = {
            "tag": tag,
            "timestamp": datetime.fromtimestamp(self.time[i]),
            "value": e
            }

            res.append(x)

        return res

    def getAngles(self):

        res = []

        tag = self.v_reg.getAnglesTag()

        for i,a in enumerate(self.angles):

            x = {
            "tag": tag,
            "timestamp": datetime.fromtimestamp(self.time[i]),
            "value": a
            }

            res.append(x)

        return res


    def getDisplacement(self):

        res = []

        tag = self.v_reg.getDispTag()

        for i,s in enumerate(self.s):

            x = {
            "tag": tag,
            "timestamp": datetime.fromtimestamp(self.time[i]),
            "value": s
            }

            res.append(x)

        return res

    def getCumulative(self):

        res = []

        tag = self.v_reg.getCumTag()

        for i,c in enumerate(self.c):

            x = {
            "tag": tag,
            "timestamp": datetime.fromtimestamp(self.time[i]),
            "value": c
            }

            res.append(x)

        return res


    def exportMongoDB(self, collection):

        try:
            x = collection.insert_many(self.getVelocity())
            print(x)
            x = collection.insert_many(self.getLatitude())
            print(x)
            x = collection.insert_many(self.getLongitude())
            print(x)
            x = collection.insert_many(self.getAcceleration())
            print(x)
            x = collection.insert_many(self.getPower())
            print(x)
            #x = collection.insert_many(self.getElevation())
            #print(x)
            #x = collection.insert_many(self.getAngles())
            #print(x)
            x = collection.insert_many(self.getDisplacement())
            print(x)
            x = collection.insert_many(self.getCumulative())
            print(x)
        except Exception as e:
            print("Issue exporting to MongoDB")
            print(e)

class ExportDay:
    def __init__(self,carReg, trips, stops):
        self.carReg = carReg
        self.trips = trips
        self.stops = stops
        
    def getTripData(self):
        
        total_dist = 0
        total_dur = 0
        total_trips = 0
        date = self.trips[0][0]
        date = datetime(date.year, date.month, date.day)
        total_energy = 0
        for trip in self.trips:
            total_dur += trip[2]
            total_dist += trip[3]
            total_energy += trip[4]
            total_trips += 1
            
        return (total_trips, total_dist, total_dur, date, total_energy)
    
    def getDurationStop(self):
        
        total_dur = 0
        i = 0
        for s in self.stops:
            total_dur += datetime.timestamp(s[3])-datetime.timestamp(s[2])
            i += 1
        return (i, total_dur)
    
    def getObject(self):
        
        return [{
            "VehicleRegistration": self.carReg,
            "Date": self.getTripData()[3],
            "TotalTrips": self.getTripData()[0],
            "DistanceTravelled": self.getTripData()[1],
            "DrivingTime": self.getTripData()[2],
            "TotalEnergy": self.getTripData()[4],
            "TotalStops": self.getDurationStop()[0],
            "TotalStopTime": self.getDurationStop()[1]
        }]
    
    def exportMongoDB(self, collection):
        y = self.getObject()
        try:
            
            x = collection.insert_many(y)
            print(x)

        except Exception as e:
            print("Issue exporting to MongoDB")
            print(e)
          