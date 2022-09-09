from urllib import request, parse, error
import json
import time
import numpy as np
import math

def getElevationAPI(lat, lon, base_url = 'https://api.open-elevation.com/api/v1/lookup'):
  d_arr = [{}]*len(lat)

  for i in range(len(lat)):
    d_arr[i] = {"latitude":lat[i],"longitude":lon[i]}
  location = {"locations": d_arr}

  json_data = json.dumps(location, skipkeys=True).encode('utf8')
  response = request.Request(base_url, data=json_data, headers={'Content-Type': 'application/json'})
  current_delay = 0.100
  max_delay = 10

  while True:
    try:
      fp = request.urlopen(response)

    except error.URLError:
      pass

    else:
      res_byte = fp.read()
      res_str = res_byte.decode("utf8")
      js_str = json.loads(res_str)
      fp.close()

      return [x['elevation'] for x in js_str['results']]

    if current_delay > max_delay:
      raise Exception("Too many retry attempts")

    time.sleep(current_delay)
    current_delay *= 2


def getSlices(N):
	x = N//1000
	rem = N - x*1000
	indices = []
	for i in range(x):
	    if i == 0:
	        start = 0
	        end = (i+1)*1000
	    else:
	        start = (i)*1000
	        end = (i+1)*1000
	    indices.append((start,end))

	start = (indices[x-1][1])
	end = start + rem
	indices.append((start,end))

	return indices


def getElevation(lat, lon):

	N = len(lat)

	if N < 1000:
		results = getElevationAPI(lat, lon)
		return results

	else:
		slices = getSlices(N)
		final = []
		for x,y in slices:
			temp_lat = lat[x:y]
			temp_lon = lon[x:y]

			results = getElevationAPI(temp_lat, temp_lon)
			final = np.concatenate((final, results), axis=0)
		

		return list(final)


def getAngles(elevation, distance):
	angles = [0]

	for i in range(1, len(distance)):

		num = elevation[i] - elevation[i-1]

		if abs(num) > 0.1:
			if distance[i] == 0.0 or distance[i] < 0.05:
				angles.append(0)
			else:
				angle = np.arcsin(num/(distance[i]*1000))
				angles.append(np.degrees(angle))

		else:
			angles.append(0)


	return angles

