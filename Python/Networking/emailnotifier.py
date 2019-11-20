#!/usr/bin/python3.7
# Configparser 4.0.2 is required
# Author: Arjan de Haan (Vepnar)
# Blink a luxafor when there are E-Mails found in the user their E-Mail box
# Credits to: https://github.com/vmitchell85/luxafor-python
# TODO add windows compatibility 

import imaplib
import base64
import usb.core
import usb.util
import time
import sys
import os.path
import configparser
from contextlib import suppress

DEFAULT_CONFIG = '''[EMAIL]
email     = example@gmail.com
password  = password123
server    = imap.gmail.com
port      = 993
interval  = 5

[ACTIONS]
example@example.com   = [0,0,255]
boss@gmail.com  = [255,0,0]
'''


def setup_luxafor():
    # First we check on what operation system we are running
    if sys.platform == "win32":
        pass
    else:
        # Looks like we are running in Linux
        # First we look the our luxafor device
        device = usb.core.find(idVendor=0x04d8, idProduct=0xf372)

        # Now we check if it actually exists
        if device is None:
            return None

        # Linux kernel sets up a device driver for USB device, which you have to detach.
        # Otherwise trying to interact with the device gives a 'Resource Busy' error.
        with suppress(Exception):
            device.detach_kernel_driver(0)

        # Setup configuration for the luxafor
        device.set_configuration()
        return device


def setup_email(username, password, server='imap.gmail.com', port=993):
    # Connect to the SMTP server with IMAP
    mail = imaplib.IMAP4_SSL(server, port)

    # Login to the SMTP server
    mail.login(username, password)

    # Access the inbox of the user
    mail.select('inbox')

    return mail


def setup_config(file='config.cfg'):
    # Check if the config file exists
    if not (os.path.exists(file) and os.path.isfile(file)):

        # Create a new config file and write a default config inside of it
        with open(file, 'w') as f:
            f.write(DEFAULT_CONFIG)

        # Write a message to the user and exit the application
        print('Config file created please edit this file first before you re-execute')
        sys.exit(1)

    # Setup the config parser and read the file
    config = configparser.ConfigParser()
    config.read(file)

    return config

def blink(device, red=0, green=0, blue=0):
    # First we check on what operation system we are running
    if sys.platform == "win32":
        pass
    else:
        # Write a stobe command to the luxafor
        # the array explained:
        # 1st byte: mode
        # 2-5th byte: colour (0-255)
        # 6th byte: speed (0-255)
        device.write(1, [3, 255, red, green, blue, 40])

def turn_off(device):
    # First we check on what operation system we are running
    if sys.platform == "win32":
        pass
    else:
        # Write no colour to the luxafor to turn it off
        device.write(1, [1, 0, 0, 0, 0])


def check_emails(mail, address):
    # Check if there are unseen emails for a certain address.
    _, data = mail.search(None, '(UNSEEN)', f'(FROM {address})')

    # Return if there are items found
    if data[0]:
        return True
    return False


def loop(mail, actions):
    # Loop through all the actions and their addresses
    for address, action in actions.items():

        # Check if address is found in the E-Mail box
        if check_emails(mail, address):

            # Convert the action to a list with eval
            # TODO make this less dangerous (EVAL IS REALLY DANGEROUS AND UNSAFE)
            return eval(action)

def main():
    # Begin setting setting up the config and Luxafor
    config = setup_config()
    luxafor = setup_luxafor()

    # Receive credential for the E-Mail reader
    username = config.get('EMAIL', 'email')
    password = config.get('EMAIL', 'password')

    # Receive information about the SMTP server
    server = config.get('EMAIL', 'server')
    port = config.getint('EMAIL', 'port')

    # Receive information about how fast we should read our emails
    delay = config.getint('EMAIL', 'interval')

    # Receive actions set by the user
    actions = dict(config.items('ACTIONS'))

    # Begin setting up email
    mail = setup_email(username, password, server=server, port=port)

    # Turn the Luxafor off
    turn_off(luxafor)

    # Store the last colour so we don't have to use the usb port a lot
    last_colour = None

    # Create an infinite loop to check if there are any new E-Mails
    while(True):
        time.sleep(delay)

        # Check if there are any new mails and receive the colour it should show on the Luxafor
        new_colour = loop(mail, actions)

        # Check if there are any changes in colour
        if last_colour == new_colour:
            continue

        # Set the last colour the new colour
        last_colour = new_colour

        # Check if the last colour is none
        # Turn the luxafor off when it is None
        if last_colour is None:
            turn_off(luxafor)
            continue

        # Set the colour of the luxafor in blinking mode
        blink(luxafor, red=last_colour[0],
              green=last_colour[1], blue=last_colour[2])

if __name__ == '__main__':
    main()
