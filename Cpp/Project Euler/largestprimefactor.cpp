// Author: Arjan de Haan (Vepnar)
// https://en.wikipedia.org/wiki/Fibonacci_number
// https://projecteuler.net/problem=3

#include <stdio.h>

int main(void)
{
    long long n = 600851475143;
    int i =2;
    int counter=0;
    int factors[10];
    while(i * i <= n)
    {
        if(n % i != 0)
        {
            i++;
        }
        else
        {
            n = n / i;
            factors[counter] = i;
            counter++;
        }
    }
    if(n > 1)
    { 
        factors[counter] = n;
        counter++;
    }
    for(int i=0;i<counter;i++)
        printf("%d\n",factors[i]);
}