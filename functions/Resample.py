import numpy as np 
import math

def timeGaps(time, samplingRate):
    timeDiff = np.diff(time)
    arr = []
    indices = []
    for i, td in enumerate(timeDiff):
        if td > samplingRate:
            arr.append(td/samplingRate)
            indices.append(i)
        else:
            pass
    return arr, indices

def getNextTimeGap(time, samplingRate):
    timeDiff = np.diff(time)
    for i,td in enumerate(timeDiff):
        if td > samplingRate:
            return i
        else:
            pass
    return None

def insertList(_list,i, insertee):
    j = i 

    for x in insertee:
        _list.insert(j, x)
        j+=1
        
def getVelocity(start, delta, gap):
    temp = start
    row = []
    for i in range(int(gap)-1):
        temp += delta
        row.append(temp)
    return row

def forwardFill(start, gap):
    row = []
    for i in range(int(gap)-1):
        row.append(start)
    return row

def insertVelocity(velocity, i, tgap, samplingRate=10, threshold=50):
    first = velocity[i]
    Next = velocity[i+1]
    diff = Next - first
    dB = diff/samplingRate

    if tgap > 20:
        row = forwardFill(0, tgap)

    elif dB > threshold:
        delta = diff/(tgap*samplingRate)
        row = getVelocity(first, delta, tgap)

    else:
        row = forwardFill(first, tgap)

    j = i + 1
    for r in row:
        velocity.insert(j, r)
        j += 1


def resampleTimeVelocity(time, velocity, samplingRate=10):
    tGaps, _ = timeGaps(time, samplingRate)

    for tg in tGaps:

        i = getNextTimeGap(time, samplingRate)

        if i == None:
            return time, velocity

        row = getTimeRow(time[i], tg, samplingRate)

        insertList(time, i+1, row)
        insertVelocity(velocity, i, tg)

    return time, velocity


def getTimeRow(start, tg, samplingRate):
    temp = start
    row = []
    for j in range(int(tg)-1):
        temp += samplingRate
        row.append(temp)
    return row

def get_bearing(lat1, long1, lat2, long2):        
    dLon = (long2 - long1)

        
    x = math.cos(math.radians(lat2)) * math.sin(math.radians(dLon))
    y = math.cos(math.radians(lat1)) * math.sin(math.radians(lat2)) - math.sin(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.cos(math.radians(dLon))
    brng = np.arctan2(x,y)
    brng = np.degrees(brng)

    return brng

def getPreviousBearing(latitude, longitude, i):
    first_lat = latitude[i]
    prev_lat = latitude[i-1]
    first_lng = longitude[i]
    prev_lng = longitude[i-1]
    j = i - 1
    while j > 0:
        bearing = get_bearing(prev_lat, prev_lng, first_lat, first_lng)

        if bearing != 0.0:
            return bearing
        else:
            j -= 1
            prev_lat = latitude[j]
            prev_lng = longitude[j]

    return 0.0


def kmhToMps(kmh):
    return kmh/3.6

def getNextCoordinate(row_v,  first_lat, first_lng, bearing, samplingRate=10):
    r = 6378

    
    row_lat = []
    row_lng = []

    temp_lat = first_lat
    temp_lng = first_lng


    for v in row_v:
        d = kmhToMps(v)*samplingRate/1000
        Ad = d/r
        lat2 = math.asin(math.sin(math.radians(temp_lat))*math.cos(Ad)+math.cos(math.radians(temp_lat))*math.sin(Ad)*math.cos(math.radians(bearing)))
        lng2 = temp_lng + math.atan2(math.sin(math.radians(bearing))*math.sin(Ad)*math.cos(math.radians(temp_lat)), math.cos(Ad) - math.sin(math.radians(temp_lat))*math.sin(math.radians(lat2)))

        lat2 = math.degrees(lat2)
        #lng2 = math.degrees(lng2)


        row_lat.append(lat2)
        row_lng.append(lng2)
        temp_lat = lat2
        temp_lng = lng2
        

    return row_lat, row_lng



def insertCoordinates(latitude, longitude, velocity, i, tg, samplingRate=10,threshold=50):

    bearing = getPreviousBearing(latitude, longitude, i)
    first_v = velocity[i]
    second_v = velocity[i+1]
    diff = second_v - first_v
    dB =  diff/samplingRate

    if tg > 20:
        row_lat = forwardFill(latitude[i], tg)
        row_lng = forwardFill(longitude[i], tg)
        row_v = forwardFill(0, tg)
    elif dB > threshold:
        delta = diff/(tg*samplingRate)
        row_v = getVelocity(first_v, delta, tg)
        row_lat, row_lng = getNextCoordinate(row_v, latitude[i], longitude[i], bearing)
    else:
        row_v = forwardFill(first_v, tg)
        row_lat, row_lng = getNextCoordinate(row_v, latitude[i], longitude[i], bearing)

    j = i + 1
    for i in range(len(row_v)):
        velocity.insert(j, row_v[i])
        latitude.insert(j, row_lat[i])
        longitude.insert(j, row_lng[i])
        j += 1

def resampleAll(time, velocity, latitude, longitude, samplingRate=10):

    tGaps, _ = timeGaps(time, samplingRate)

    for tg in tGaps:
        i = getNextTimeGap(time, samplingRate)
        row = getTimeRow(time[i], tg, samplingRate)
        insertList(time, i+1, row)
        
        insertCoordinates(latitude, longitude, velocity, i, tg)

    return time, velocity, latitude, longitude

