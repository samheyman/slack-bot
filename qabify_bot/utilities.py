import os
import time
import re
from slackclient import SlackClient
from math import radians, cos, sin, asin, sqrt
import json
from urllib import request, parse

google_api_key = os.environ.get('GOOGLE_API_KEY')

def api_call(url, body=None):
    req = request.Request(url)
    print("API call to: {}".format(url))
    try:
        response = request.urlopen(req, body)
        print(response.code)
        return json.load(response)
    except HTTPError as e:
        print('Error code: ', e.code)
        return None
    except URLError as e:
        print('Reason: ', e.reason)
        return None

def get_geocoordinates(address):
    address_to_search = parse.quote(address, safe='')
    url = "https://maps.googleapis.com/maps/api/geocode/json?address=" + address_to_search + "&key=" + google_api_key
    response = api_call(url)
    lat = response["results"][0]["geometry"]["location"]["lat"]
    lon = response["results"][0]["geometry"]["location"]["lng"]
    return (lat, lon)

def get_distance(point_A, point_B, type_of_distance=''):
    if type_of_distance is 'crow_flies':
        dist = haversine(point_A[0], point_A[1], point_B[0], point_B[1])
        return dist
    else:
        dist = road_distance(point_A[0], point_A[1], point_B[0], point_B[1])
        return dist

def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points 
    on the earth
    source: https://stackoverflow.com/questions/4913349/
                haversine-formula-in-python-bearing-and-distance-between-two-gps-points
    """
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    # Radius of earth in kilometers is 6371
    km = 6371* c
    return km

def road_distance(lat1, lon1, lat2, lon2):
    """
    Calculate the distance by road between two points
    """
    point1 = lat1, lon1
    point2 = lat2, lon2
    url = "https://maps.googleapis.com/maps/api/distancematrix/json?origins={0},{1}&destinations={2},{3}&mode=driving&language=en-EN&sensor=false&key={4}".format(str(lat1),str(lon1),str(lat2),str(lon2), google_api_key)
    response = api_call(url)
    km = response['rows'][0]['elements'][0]['distance']['value']
    return round(km/1000,1)
