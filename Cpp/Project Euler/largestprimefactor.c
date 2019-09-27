// Author: Arjan de Haan (Vepnar)
// https://en.wikipedia.org/wiki/Fibonacci_number
// https://projecteuler.net/problem=2

#include <stdio.h>

int main(void)
{
    int prime[47];
    int counter=0;
    for(int i = 2; i<201; i++)
    {
        int is_prime=0;
        // if(i/2 <= 1)
        //     is_prime=1;

        for(int j = 2;j < i;j++)
        {
            if (i % j == 0) break;
            is_prime=1;
        }
        
        if(is_prime==1)
        {
            printf("%d\n",i);
            //prime[counter] = i;
            counter++;
        }
        
    }
    printf("Amount of prime numbers: %d\n",counter);
    return 0;


}