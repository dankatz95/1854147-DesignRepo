import numpy as np
import math
from datetime import datetime
from functions.PowerCalculation import *
from functions.ImportVehicle import ExportPower, ExportTrip, ExportStop, ExportDay
from functions.Plots import *

def rad(d):
    return float(d)*math.pi/180

def getCoordinates(df):
    latitude = [x.latitude for x in df.select('latitude').collect()]
    longitude = [ x.longitude for x in df.select( 'longitude').collect()]
    return latitude, longitude 

def getDistance(lat1, long1, lat2, long2):
    r = 6378
    a = rad(lat2) - rad(lat1)
    b = rad(long2) - rad(long1)
    
    a = math.pow(math.sin(a/2), 2) + math.pow(math.sin(b/2), 2)*math.cos(lat1)*math.cos(lat2)
    c = 2*math.asin(math.sqrt(a)) 

    return r*c
def meanCoordinate(lat, long, i, j):
    amount = j-i+1
    
    if amount ==0:
        return float(lat[i]), float(long[i])
    
    sumLat = 0
    sumLong = 0
    
    for k in range(i, j+1):
        sumLat += float(lat[k])
        sumLong += float(long[k])
        
    return sumLat/amount, sumLong/amount
    
def deltaTime(dates, i, j):
    return datetime.timestamp(dates[j])- datetime.timestamp(dates[i])



def StayPoint_Detection(df, distThresh, timeThresh):
    lat, lon = getCoordinates(df)
    dates = [x.Date for  x  in df.select("Date").collect()]
    
    N = df.count()
    SP = []
    i = 0
    while i < N:
        j = i + 1
        Token = 0
        while j < N:
            distance = getDistance(lat[i], lon[i], lat[j], lon[j])
            if distance > float(distThresh):
                if deltaTime(dates, i, j) > timeThresh:
                    S_lat, S_long = meanCoordinate(lat, lon, i , j-1)
                    t_arrive = dates[i].strftime("%Y/%m/%d, %H:%M:%S")
                    t_depart = dates[j-1].strftime("%Y/%m/%d, %H:%M:%S")
                    SP.append([S_lat, S_long, t_arrive, t_depart, [i, j-1]])
                    i = j
                    Token = 1
                break
            j+=1
        if Token != 1:
            i += 1
    return SP
    

def zeroVelocityPoints(df, speedThresh=5, timeThresh=300):
    time, velocity = getTimeVelocity(df)
    lat, lon = getCoordinates(df)
    N = df.count()
    SP = []
    i = 0
    while i < N:
        Token = 0
        if velocity[i] < speedThresh:
            start = i
            j = i + 1
            Token = 0
            while j < N:
                if velocity[j] > speedThresh:
                    if deltaTime(time, i, j) > timeThresh:
                        end = j - 1
                        S_lat, S_long = meanCoordinate(lat, lon, start, end)
                        t_arrive = time[start].strftime("%Y/%m/%d, %H:%M:%S")
                        t_depart = time[end].strftime("%Y/%m/%d, %H:%M:%S")
                        SP.append([S_lat, S_long, t_arrive, t_depart,  (time[end]-time[start]), [start, end]])
                        i = j
                        Token = 1
                    break
                else:
                    j += 1 
        if Token != 1:
            i += 1 
    return SP


def zeroVP(time, velocity, lat, lon, speedThresh=5, timeThresh=300):
    SP = []
    i = 0
    N = len(time)
    while i < N:
        Token = 0
        if velocity[i] < speedThresh:
            start = i
            j = i + 1
            Token = 0
            while j < N:
                if velocity[j] > speedThresh:
                    if time[j] - time[i] > timeThresh:
                        end = j - 1
                        S_lat, S_long = meanCoordinate(lat, lon, start, end)
                        t_arrive = datetime.fromtimestamp(time[start])
                        t_depart = datetime.fromtimestamp(time[end])
                        SP.append([S_lat, S_long, t_arrive, t_depart,  (time[end]-time[start]), [start, end]])
                        i = j
                        Token = 1
                    break
                else:
                    j += 1 
        if Token != 1:
            i += 1 
    return SP 

def stopStartIndex(SP):
    return [x[5] for x in SP]

def getIndexSlice(StopPoints):
    startStop = []
    for i in range(len(StopPoints)-1):
        if i == 0:
            if StopPoints[i][0] < 6:
                start = StopPoints[i][1]
                end = StopPoints[i+1][0]
                startStop.append((start,end))
            else:
                start = 0
                end = StopPoints[i][0]
                startStop.append((start,end))
                startStop.append((StopPoints[i][1],StopPoints[i+1][0] ))
                
        else:
            startStop.append((StopPoints[i][1],StopPoints[i+1][0] ))
            
    return startStop

    

def getTrips(SP, time, power, lat, long):
    sp = stopStartIndex(SP)
    slices = getIndexSlice(sp)
    trips = []

    for x,y in slices:
        ek = getTotalEnergy(time[x:y], power[x:y], 10)
        dist_, _, _ = getTotalDistance(lat[x:y], long[x:y])
        start = getDateTime([time[x]])[0]
        end = getDateTime([time[y]])[0]
        duration = time[y]-time[x]
        ek = ek 


        trips.append([start,end,duration,dist_,ek])

    return trips

def ExportTrips(SP,time, velocity, lat, long, details, Trips, Clean, Stops,Days):
    sp = stopStartIndex(SP)
    slices = getIndexSlice(sp)

    trips = []

    for x, y in slices:
        
        if y-x < 100:
            pass
        else:
            timeTemp = time[x:y]
            velocityTemp = velocity[x:y]

            acc = CD(velocityTemp, 10)
            _, power = getPower(details['Mass'], acc, velocityTemp, details['Mu'], details['DragCoefficient'], details['Area'], np.zeros(len(timeTemp)))

            dist, s, c = getTotalDistance(lat[x:y], long[x:y])

            energy = getTotalEnergy(timeTemp, power, 10)

            #plotTimeSeries(getDateTime(timeTemp), velocityTemp)
            #plotTimeSeries(getDateTime(timeTemp), acc)
            #plotTimeSeries(getDateTime(timeTemp), power)



            epk = EPK(energy,dist)

            powerExport = ExportPower(
                details['VehicleRegistration'],
                timeTemp,
                velocityTemp,
                lat[x:y],
                long[x:y],
                acc,
                power,
                np.zeros(len(timeTemp)),
                np.zeros(len(timeTemp)),
                s,
                c
            )
        
        

            powerExport.exportMongoDB(Clean)


            start = getDateTime([time[x]])[0]
            end = getDateTime([time[y]])[0]
            duration = time[y]-time[x]

            trips.append([start,end,duration,dist,energy, np.mean(velocityTemp)])

    if len(trips) > 0:
    
        tripsExport = ExportTrip(details['VehicleRegistration'], trips)


        tripsExport.exportMongoDB(Trips)

        stopsExport = ExportStop(details['VehicleRegistration'], SP)

        stopsExport.exportMongoDB(Stops)

        dataExport = ExportDay(details['VehicleRegistration'], trips, SP)

        dataExport.exportMongoDB(Days)

def smoothData(data):
    N = len(data)
    t = np.arange(N)
    
    result = np.zeros(N)
    for i in t:
        kernel = np.exp(-(t-i)**2/(2*3**2))
        kernel = kernel/np.sum(kernel)
        result[i] = np.sum(data*kernel)
        
    return result

