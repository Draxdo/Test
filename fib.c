#include <stdio.h>

int fizzbuzz(int n) {
    if (n == 0) {
        return 0;
    }
    else if (n % 3 == 0) {
        if (n % 5 == 0) {
            printf("FizzBuzz\n");
            fizzbuzz(n - 1);
        }
        else {
            printf("Fizz\n");
            fizzbuzz(n - 1);
        }
    }
    else if (n % 5 == 0) {
        printf("Buzz\n");
        fizzbuzz(n - 1);
    }
    else {
        printf("%d\n", n);
        fizzbuzz(n - 1);
    }
    return 0;
}

int main() {
    fizzbuzz(100000);
    return 0;
}