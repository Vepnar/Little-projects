#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
    Author: Arjan de Haan (Vepnar)

    requirements: matplotlib
'''

from math import radians, cos, sin
import matplotlib.pyplot as plt

g = 9.80 # m/s
v = 200 # m/s

def displacement(a,t,v):
    a = radians(a)
    x = v*t*cos(a)
    y = v*t*sin(a)-0.5*g*t**2

    return x,y

def plot_angle(a):
    x, y, t = [],[],0
    while True:
        vx, vy = displacement(angle,t,v)
        if 0 > vy:
            break
        x.append(vx)
        y.append(vy)
        t+=1
    plt.plot(x,y)

if __name__ == '__main__':
    angles = [20, 45, 75]
    
    for angle in angles:
        plot_angle(angle)
    plt.show()

    