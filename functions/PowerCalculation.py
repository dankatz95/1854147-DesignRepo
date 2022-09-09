import numpy as np
import math
from datetime import datetime 

def getDateTime(time):
    return [datetime.fromtimestamp(x) for x in time]

def CD(y,h):
    diff = [0]
    for i in range(1,len(y)-1):
        temp = (y[i+1]-y[i-1])/(2*h)
        diff = np.append(diff,temp)
    return np.append(diff,0)

def central_difference(x, y):
    
    h = x[1] - x[0]
    diff = [
        (y[1]-y[0])/(x[1]-(x[0]-h))
    ]
    
    for i in range(1, len(y)-1):
        temp = (y[i+1]-y[i-1])/(x[i+1]-x[i-1])
        diff = np.append(diff, temp)
    
    h = x[len(y)-1] - x[len(y)-2]
    diff = np.append(
        diff,
        (y[len(y)-1]-y[len(y)-2])/((x[len(y)-1]+h)-x[len(y)-2])
    )
    
    return x, diff

def rad(d):
    return float(d)*math.pi/180

def getDistance(lat1, long1, lat2, long2):
    r = 6378
    a = rad(lat2) - rad(lat1)
    b = rad(long2) - rad(long1)
    
    a = math.pow(math.sin(a/2), 2) + math.pow(math.sin(b/2), 2)*math.cos(lat1)*math.cos(lat2)
    c = 2*math.asin(math.sqrt(a))
    return r*c

def getTotalDistance(lat, long):
    total = 0
    displacement = [0]
    cum = [0]
    for i in range(len(lat)-1):
        temp = getDistance(lat[i], long[i], lat[i+1], long[i+1])
        total += temp
        displacement.append(temp)
        cum.append(total)
    return total, displacement, cum


def getCoordinates(df):
    latitude = [x.Latitude for x in df.select('Latitude').collect()]
    longitude = [ x.Longitude for x in df.select( 'Longitude').collect()]
    return latitude, longitude 

def getTimestamp(DT: datetime):
    return datetime.timestamp(DT)

def getTimestampArr(arr : list):
    return [datetime.timestamp(x) for x in arr]

def getTimeVelocity(df, time="Date", velocity="velocity"):
    time = [x.Date for x in df.select("Date").collect()]
    velocity = [x.velocity for x in df.select('velocity').collect()]
    return time, velocity


def instAcceleration(df, time="Date", velocity="velocity"):
    
    _time, velocity = getTimeVelocity(df, time, time)
    _ , acc = central_difference(_time, velocity)

    return _time, acc

def kmhToMps(kmh):
    return kmh/3.6

def motorForce(m, a, v, mu, Cd, A, theta=0):
    p = 1.225
    g = 9.8
    return (0.5*p*Cd*A*math.pow(v,2) + mu*m*g*math.cos(theta) + m*g*math.sin(theta)+m*a)

def getPower(m, a, v, mu, Cd, A, theta):
    power = 0.0
    powerArr = []
    for i in range(len(a)):
        temp = motorForce(m, a[i], kmhToMps(v[i]), mu, Cd, A, theta[i])* kmhToMps(v[i])
        power += temp
        powerArr = np.append(powerArr, temp)

    return power, powerArr


def unevenTrap(t, y):
    area = []
    total = 0
    dT = np.diff(t)
    for i in range(len(y)-1):
        temp = (y[i] + y[i+1])*(dT[i]/2)
        total += temp
        area = np.append(area, temp)
    return total , area

def getTotalEnergy(t, power, h):
    energy,_ = getEnergy(t,power,h)#Trapezoidal(t, power, h)#unevenTrap(t,power)

    return energy/(1000*3600)


def EPK(energy, distance):
    return energy/distance

def Trapezoidal(x, y, h):
    area = []
    total = 0
    temp = 0

    for i in range(len(x)):
        if i == 0 or i == len(x)-1:
            temp = (h/2)*y[i]
        else:
            temp = h*y[i]
        total += temp
        area = np.append(area, temp)
    return total, area

def getEnergy(x,y,h):
    area = []
    total = 0
    temp = 0
    y = y/0.9
    
    
    
    for i in range(len(x)):
        if i == 0 or i == len(x)-1:
            if y[i] < 0:
                temp = (h/2)*y[i]*0.5
                
            else:
                temp = (h/2)*y[i]
               
        else:
            if y[i] < 0:
                temp = h*y[i]*0.5
                
            else:
                temp = h*y[i]
        
        total += temp
        area = np.append(area, temp)
    return total,area
        
        
        
        
'''        
        if y[i] < 0:
            temp = 0
            
        else:
            
            if i == 0 or i == len(x)-1:
                temp = (h/2)*y[i]
            else:
                
        total += temp
        area = np.append(area, temp)
    return total, area

                temp = h*y[i]
'''
