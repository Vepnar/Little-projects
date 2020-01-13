#!/usr/bin/python3.7
# -*- coding: utf-8 -*-
"""A sorting algoritm based on the way stalin ruled"""

def receive_input(size=10):
    """Receive input from the user"""
    counter = 0
    number_array = []
    while counter < size:
        raw_input = input(f'[{counter+1}] Write down a number: ')
        try:
            raw_input = int(raw_input)
            number_array.append(raw_input)
            counter += 1
        except ValueError:
            print('I said number!')
            continue

    return number_array

def stalin_sort(array):
    """This will remove all the numbers that are not in the right order"""
    array_size = len(array)
    array = array[:] # Copy the array
    for _ in range(array_size):
        i = 0
        while i < array_size - i: # Loop through all citizens
            if array[i] > array[i + 1]:
                del array[i] # Send them to gulag
                array_size -= 1 # Lower the citizen size
            i += 1
    return array

def reverse_stalin_sort(array):
    """The same as stalin sort but reversed"""
    array_size = len(array)
    array = array[:]
    for _ in range(array_size):
        i = 0
        while i < array_size - 1:
            if array[i] < array[i + 1]:
                del array[i + 1]
                array_size -= 1
            i += 1
    return array


def main():
    """Default function"""
    user_input = receive_input()
    print()
    stalin_1 = stalin_sort(user_input)
    stalin_2 = reverse_stalin_sort(user_input)
    print('User input:')
    print(user_input)
    print('Stalin sort:')
    print(stalin_1)
    print('Reversed Stalin sort:')
    print(stalin_2)
    print('Have fun ruling arrays with communism')

if __name__ == '__main__':
    main()
