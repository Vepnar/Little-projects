# Author: Arjan de Haan (Vepnar)
# https://en.wikipedia.org/wiki/Fibonacci_number

F0 = 1
F1 = 0

for _ in range(100):
    F1,F0 = F0,F0+F1
    print(F1)
