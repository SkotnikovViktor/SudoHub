#include"Alg.H"
#include <string.h> 
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

int main() {
    char text[] = "Это предложение с тремя пробелами до точки. Второе с двумя пробелами. Третье. Четвертое предложение с четырьмя пробелами до точки.";
    int dotCount;
    int a;
    int *spaceCounts = countSpacesBeforeEachDot(text, &dotCount);
    a=shotchic(spaceCounts,dotCount);
    printf("%d\n%d",a,dotCount);
    free(spaceCounts);

    return 0;
}
