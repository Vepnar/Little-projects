#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
    Author: Arjan de Haan (Vepnar)
    v = Velocity in M/s
    g = Grafity in M/s
    Returns in degrees

'''

from math import sqrt, atan, degrees

def get_angle(x, y, v=200 ,g=9.8):
    a = g * x * x + 2 * y * v * v
    b = pow(v, 4) - g * a
    c = v * v + sqrt(b)
    d = g * x
    e = c / d
    angle = atan(e)
    return degrees(angle)


result = get_angle(2, 0)
print(result)