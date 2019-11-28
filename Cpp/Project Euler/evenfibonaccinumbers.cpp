// Author: Arjan de Haan (Vepnar)
// https://en.wikipedia.org/wiki/Fibonacci_number
// https://projecteuler.net/problem=2

#include <stdio.h>

int main(void)
{
    long F0 = 1, F1 = 0;
    printf("Even Fibonacci numbers: ");
    for(int i=0;i<55;i++) 
    {
        F0 = F1+F0;
        F1 = F0;
        if(F0 % 2 == 0)
            printf("%ld, " , F0);
    }
    printf("\n");
    return 0;

}