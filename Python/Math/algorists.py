#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Author: Arjan de Haan (Vepnar)

from PIL import Image
import numpy as np

# Default width, height & background colour  of the generated image
WIDTH = 1024
HEIGHT = 1024
BACKGROUND = (0, 0, 0)

# Generate RGB values based on coordinates to generate art
# See: https://en.wikipedia.org/wiki/Algorithmic_art
def generate_rgb_values(x, y):
    r = 0 % 256
    g = (((x ^ y) - (x | y)) ^ y) | x % 256
    b = (((x ^ y) - (x | y)) ^ y) % 256
    return (r, g, b)

# Generates image based on the given variables
def main(width, height, background):
        new_image = Image.new('RGB',
                (width, height), background)
                
        pixels = list(new_image.getdata())

        for x in range(width):
                for y in range(height):
                        location = x + y * width
                        pixels[location] = generate_rgb_values(x, y)

        new_image.putdata(pixels)
        return new_image

# Called when this file isn't imported
# This will generate the image and show it
if __name__ == "__main__":
    generated_image =  main(WIDTH,HEIGHT,BACKGROUND)
    generated_image.show()