#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Arjan de Haan (Vepnar)
# Target device: HP Switch 3500yl-24G (J8692A)
# Status: Smooth doesn't work yet
# This piece of code should visualize internet usage live

# Requirements
# matplotlib==3.1.1
# scipy==1.3.1
# pysnmp==0.3.4

from pysnmp.entity.rfc3413.oneliner import cmdgen
from scipy.ndimage.filters import gaussian_filter1d
import matplotlib.pyplot as plt
import numpy as np
import time
import sys

# SNMP connection information
SNMP_HOST = ('192.168.10.2', 161)
SNMP_COMMUNITY = 'public'
DELAY = 1

# Bytes recieved 'iso.3.6.1.2.1.2.2.1.10.1'
# Bytes send 'iso.3.6.1.2.1.2.2.1.16.1'
IDO = ('iso.3.6.1.2.1.2.2.1.10.1', 'iso.3.6.1.2.1.2.2.1.16.1')

# Recieve network information about the switch


def recieve_values():

    # Prepare command to send to the snmp server
    cmd_generator = cmdgen.CommandGenerator()

    error_indication, error_status, _, values = cmd_generator.getCmd(
        cmdgen.CommunityData(SNMP_COMMUNITY),
        cmdgen.UdpTransportTarget(SNMP_HOST),
        *IDO
    )

    # Check if there are any errors in the connection and exit if there is
    # TODO: Improve error message
    if error_indication or error_status:
        print("Error")
        sys.exit(1)

    # Process recieved information and parse it
    output = []
    for name, val in values:
        output.append(int(val.prettyPrint()))
    return output[0], output[1]


def draw_plot(list_down, list_up, i, smooth=True):

    # Create values for the x axis & clear the plot
    x_raw = list(range(i-len(list_down), i))
    plt.clf()

    #  Draw lines in the plot if smooth is disabled
    # Smooth should stay disabled because it doesn't work yet :(
    if not smooth:
        plt.plot(x_raw, list_down,
                 label="Down", color=(1, 0, 0, 0.6)
                 )
        plt.plot(x_raw, list_up,
                 label="Up", color=(0, 1, 0, 0.6)
                 )

        # Add a legend and wait
        plt.legend(loc='best')
        plt.draw()
        plt.pause(DELAY)
        return

    # Create a linespace between lowest item on the x axis and the higest one
    x_new = np.linspace(min(x_raw), i, 50)

    # Create spline objects
    down_smooth_object = make_interp_spline(x_raw, list_down, k=3)
    up_smooth_object = make_interp_spline(x_raw, list_up, k=3)

    # Smooth everything
    down_smooth = down_smooth_object(x_new)
    up_smooth = up_smooth_object(x_new)

    # Draw all information on the screen and wait
    plt.plot(x_new, down_smooth,
             label="Down", color=(1, 0, 0, 0.6)
             )
    plt.plot(x_new, up_smooth,
             label="Up", color=(0, 1, 0, 0.6)
             )
    plt.legend(loc='best')
    plt.draw()
    plt.pause(DELAY)


def main():
    # Who doesn't want a pretty grid?
    plt.style.use('seaborn-whitegrid')
    last_down, last_up = recieve_values()
    list_down, list_up = [], []
    time.sleep(DELAY)
    i = 0

    # Dynamic renderloop for the plot
    while True:
        # Calculate new values based on recieved information
        new_down, new_up = recieve_values()

        # Calculate values and converts them to kilobytes
        calc_down, calc_up = (new_down - last_down) / \
            1000, (new_up - last_up)/1000
        
        # It overflows sometimes and thows a huge negative spike
        # We don't want that here
        calc_down = calc_down if 0 < calc_down else 0
        calc_up = calc_up if 0 < calc_up else 0
        i += 1

        # Add values to value list
        list_up.append(calc_up)
        list_down.append(calc_down)

        # Smooth is only available when there are more than 3 items in the list
        if i > 10:
            draw_plot(list_down, list_up, i, smooth=False)
        else:
            draw_plot(list_down, list_up, i, smooth=False)

        # We dont want too much data in our graph
        if len(list_down) > 10:
            list_down = list_down[1:]
            list_up = list_up[1:]

        # Refresh data
        last_down, last_up = new_down, new_up

if __name__ == "__main__":
    main()