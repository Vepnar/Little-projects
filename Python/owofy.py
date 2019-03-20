#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
    Author: Arjan de Haan (Vepnar)
'''

import re
import random

# Use at your own risk

faces = ['(・`ω´・)', ';;w;;', 'owo', 'OwO','>.<', 'uwu', '( ˘͈ ᵕ ˘͈♡)','UwU', '>w<', '^w^','>.>', '(つ✧ω✧)つ', '(/ =ω=)/']

def owofy(msg):
    face =' '+faces[random.randint(0,len(faces)-1)]
    msg = re.sub(r'(?:l|r)', 'w',msg)
    msg = re.sub(r'(?:L|R)', 'W',msg)
    msg = re.sub(r'n([aeiou])','ny$1',msg)
    msg = re.sub(r'N([aeiou])','ny$1',msg)
    msg = re.sub(r'N([AEIOU])','ny$1',msg)
    msg = re.sub(r'ove','uv',msg)

    return re.sub(r'!+',face,msg)
    
if __name__ == '__main__':
    import sys
    args = ' '.join(sys.argv[1:])

print(owofy(args))