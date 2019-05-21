// Author: Arjan de Haan (Vepnar)

#include <iostream>
#include <cmath>

// Calculate pi based on the BBP formula
// See: https://en.wikipedia.org/wiki/Bailey%E2%80%93Borwein%E2%80%93Plouffe_formula
double pi_inside(int k){
    double w = 1.0 / pow(16,k);
    double b = 4.0 / (8 * k + 1);
    double c = 2.0 / (8 * k + 4);
    double d = 1.0 / (8 * k + 5);
    double e = 1.0 / (8 * k + 6);
    double f = b - c - d - e;
    return w * f;
}   

int main(){
    double pi = 0.0;
    for(int i = 0; i < 100; i++){
        pi += pi_inside(i);
        
    }

    std::cout.precision(18);
    std::cout << "Pi: " << pi << std::endl;
   
}