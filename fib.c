#include <stdio.h>

int fib(int n) {
    if (n < 2) {
        return n;
    }
    return fib(n-2) + fib(n-1);
}

int main() {
    printf("The answer is: %d\n", fib(45));
    return 0;
}