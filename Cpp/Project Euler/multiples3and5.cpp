// Author: Arjan de Haan (Vepnar)
// https://projecteuler.net/problem=1

#include <stdio.h>

int main(void) 
{
    long sum =0;
    for(int i = 1; i < 1001; i++)
    {
        if(i % 5 == 0 || i % 3 == 0)
            sum+=i;
    }
    printf("The sum of all the multiples of 3 or 5 below 1000: %ld\n", sum);
}