#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
"""This is the beginning of something amazing!

usage: python file.bf
"""
import os
import sys

# Create memory cells and a memory index.
memory = [0]
memory_index = 0

# Count at which charater we are.
index = 0

# Open given file
file = open(sys.argv[1], 'r')

# Start infinite loop to check all chars.
while True:

    # Read a character.
    byte = file.read(1)

    # Add 1 to the index counter.
    index += 1

    # Cancel the reader when the we are at the end of the file.
    if not byte:
        break

    # The '+' character means it is going to add 1 to the current selected cell
    elif byte == '+':
        memory[memory_index] = memory[memory_index] + \
            1 if memory[memory_index] < 255 else 0

    # The '-' character means it is going to remove 1 from the current selected cell
    elif byte == '-':
        memory[memory_index] = memory[memory_index] - \
            1 if memory[memory_index] > 0 else 255
    elif byte == '~':
        print(memory_index, memory)

    # Select the cell to the right
    elif byte == '>':
        memory_index += 1
        if memory_index == len(memory):
            memory.append(0)

    # Select the cell on the left
    elif byte == '<':
        memory_index = memory_index - 1 if memory_index > 0 else 0

    # Print the current character in ascii
    elif byte == '.':
        print(chr(memory[memory_index]), end='')

    # Read one character from the console
    elif byte == ',':
        memory[memory_index] = ord(sys.stdin.read(1))

    # Open a loop
    elif byte == '[' and memory[memory_index] == 0:

        # Check if the given cell their value is 0
        # and skip to the end of the loop
        open_brackets = 1
        while open_brackets > 0:
            byte = file.read(1)
            if byte == ']':
                open_brackets -= 1
            elif byte == '[':
                open_brackets += 1
            else:
                index += 1

    # Close loop detected
    elif byte == ']' and memory[memory_index] != 0:
        # Check if the index is 0 and there is more than 1 open bracket
        open_brackets = 1
        while index > 0 and open_brackets:

            # Reduce the index by 1
            index -= 1

            # Set 2 steps back
            file.seek(index-1, os.SEEK_SET)

            # Reading a character will set 1 step. thats why we set 2 steps
            byte = file.read(1)

            # Detect if the see any closing brackets
            if byte == '[':
                open_brackets -= 1

            # Add any opening brackets to the open bracket counter
            elif byte == ']':
                open_brackets += 1

        # Go 1 extra step back
        file.seek(index-1, os.SEEK_SET)
        index -= 1

        file.read(1)

    # Ignore other characters
    else:
        continue

# Print the finish message

file.close()
print('\nDone')
