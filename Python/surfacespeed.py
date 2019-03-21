#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
    Author: Arjan de Haan (Vepnar)

'''

from math import pi , radians, sin,cos
from urllib.request import urlopen

EARTH_EQUATOR = 6371000 # meters
STELLAR_DAY = 86164.1 # seconds
GEO_URL = 'http://ipinfo.io/loc'

def earth_rotation(lat):
    lat = radians(lat)
    new_radius = sin(lat) * EARTH_EQUATOR
    new_circumference = 2*pi*new_radius
    return new_circumference / STELLAR_DAY

def geo_location():
    src = urlopen(GEO_URL).read()
    loc = src.decode('UTF-8').split(',')
    return float(loc[0]), float(loc[1])

if __name__ == '__main__':
    lat, lon = geo_location()
    v = earth_rotation(lat)
    out = 'Latitude: {0:.3f}, Longitude: {1:.3f} Surface speed: {2:.2f} M/s\n'

    print(out.format(
        lat, lon, v
    ))
