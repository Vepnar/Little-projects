// Author: Arjan de Haan (Vepnar)
// https://projecteuler.net/problem=4
// There is a better way of doing this. I'm 100% sure about that!

#include <string> 
#include <iostream>

int main ()
{
    for(int multiplier = 999; multiplier > 100; multiplier--)
    { 
        for(int multiplicand = 999; multiplicand > 100; multiplicand --)
        {  
            int product = multiplier * multiplicand;
            std::string product_string = std::to_string(product);

            int size = product_string.length();

            for(int i = size; i > 0; i--)
            {
                if(product_string[size-i] != product_string[i-1])
                    break;

                if(i==1)
                {
                    std::cout << multiplier << " * " << multiplicand << " = " << product << "\n";
                    return 0;
                }
            }
        }
    }
    return 0;
}