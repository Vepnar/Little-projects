#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
"""This is the beginning of something amazing!"""
import os
import sys


memory = [0]
memory_index = 0
index = 0
open_brackets = 0
open_loop = []
file = open('test.bf', 'r')

while True:
    byte = file.read(1)
    index+=1
    if not byte:
        break
    elif byte == '+':
        memory[memory_index] = memory[memory_index] + \
            1 if memory[memory_index] < 255 else 0
    elif byte == '-':
        memory[memory_index] = memory[memory_index] - \
            1 if memory[memory_index] > 0 else 255
    elif byte == '>':
        memory_index += 1
        if memory_index == len(memory):
            memory.append(0)
    elif byte == '<':
        memory_index = memory_index - 1 if memory_index > 0 else 0
    elif byte == '.':
        print(chr(memory[memory_index]), end='')
    elif byte == ',':
        memory[memory_index] = ord(sys.stdin.read(1))
    elif byte == '[':
        open_brackets += 1
        if memory[memory_index] == 0:
            while  open_brackets > 0:
                byte = file.read(1)
                if byte == ']':
                    open_brackets -= 1
                else:
                    index += 1
    elif byte == ']':
        while index > 0 and open_brackets > 0:
            index -= 1
            file.seek(index-1, os.SEEK_SET)
            byte = file.read(1)
            if byte == '[':
                open_brackets -= 1
            if byte == ']':
                open_brackets += 1
        file.seek(index-1, os.SEEK_SET)
        index -= 1


    else:
        continue
print()
print(memory)