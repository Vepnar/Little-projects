#!/usr/bin/python3.7
# Author: Arjan de Haan (Vepnar)
# Credits: https://stackoverflow.com/questions/54778105/python-pygame-fails-to-output-to-dev-fb1-on-a-raspberry-pi-tft-screen

# Requirements:
# pygame
# PiTFT 2.2

import pygame, time, math, random

# Size of the display
display_size = (320, 240)


# Note that we don't instantiate any display!
pygame.init()

# The size of the display we are going to draw on
# This must be the same size as the actual screen
lcd = pygame.Surface(display_size)

# This is the important part
def draw_buffer():
    # We open the TFT screen's framebuffer as a binary file. Note that we will write bytes into it, hence the "wb" operator
    f = open("/dev/fb1","wb")

    # According to the TFT screen specs, it supports only 16bits pixels depth
    # Pygame surfaces use 24bits pixels depth by default, but the surface itself provides a very handy method to convert it.
    # once converted, we write the full byte buffer of the pygame surface into the TFT screen framebuffer like we would in a plain file:
    f.write(lcd.convert(16,0).get_buffer())

    # We can then close our access to the framebuffer
    f.close()

    # According to the PiTFT2.2 screen specs, it supports only 10 frames per second.
    # By adding a delay of 0.1 seconds we will get a constant speed of around 10 frames per second.
    time.sleep(0.1)

# Now we've got a function that can get the bytes from a pygame surface to the TFT framebuffer, 
# we can use the usual pygame primitives to draw on our surface before calling the refresh function.

# Here we just blink the screen background in a few colors with the "Hello World!" text
pygame.font.init()
defaultFont = pygame.font.SysFont(None,30)


# After we done all of that we can finally do some tests if the display works and if the colours look right
while(True):
    
    # We first start by overwriting the display with darkness to make our display start in a smooth transition 
    for i in range(17):
        pygame.draw.rect(lcd,(0,0,0),(i*20,0,20,240))
        draw_buffer()

    # After we done that we will start by turning the red up in the display
    for i in range(25):
        lcd.fill((i*10,0,0))
        draw_buffer()

    # Now we start adding green to the display this should make the display look yellow
    for i in range(25):
        lcd.fill((250,i*10,0))
        draw_buffer()

    # And the last thing we add is blue. adding red green and blue together will make white.
    # That means after running this part of code the display should be white
    for i in range(25):
        lcd.fill((250,250,i*10))
        draw_buffer()
    
    # The display ain't completely white and we are missing 5 of every colour so we add that here
    lcd.fill((255,255,255))

    # Now we will write random bars of 10 pixels on the display just for fun
    for i in range(1,33):
        colour = (random.randint(0,25)*10, random.randint(0,25)*10,random.randint(0,25)*10)
        pygame.draw.rect(lcd,colour,(i*10-10,0,10,240))
        draw_buffer()

    # After we done all the test the display automatically restarts until you hit CRTL+C on your keyboard