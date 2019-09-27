#!/usr/bin/env python
# -*- coding: utf-8 -*-

#    Author: Arjan de Haan (Vepnar)
#    requirements: matplotlib


from math import radians, cos, sin
import matplotlib.pyplot as plt

# Default settings
g = 9.80 # Grafity m/s
v = 200 # Velocity m/s

# Calculate displacement based on a number of variables
# See: https://en.wikipedia.org/wiki/Projectile_motion
def displacement(a,t,v):
    a = radians(a)
    x = v*t*cos(a)
    y = v*t*sin(a)-0.5*g*t**2

    return x,y

# Make the angle visible in a plot
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
    angles = [75.32970921248814, 89.98596253345757]
    
    for angle in angles:
        plot_angle(angle)
    plt.show()

    