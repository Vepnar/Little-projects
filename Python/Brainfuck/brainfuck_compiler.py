#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
"""This is the beginning of something amazing!"""
import sys


memory = [0]
memory_index = 0
index = 0
open_loop = []
file = open('test.bf', 'r')
while 1:
    byte = file.read(1)
    if not byte:
        break
    if byte == '+':
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

    index += 1

print(memory)
