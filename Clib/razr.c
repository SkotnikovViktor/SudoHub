#include <stdio.h>
#include <string.h>
#include <stdlib.h>

int* countSpacesBeforeEachDot(const char *text, int *dotCount) {
    int len = strlen(text);
    int *spaceCounts = NULL;
    int count = 0;
    int spaceCounter = 0;
    int dots = 0;

    // Первый проход: подсчитываем количество точек
    for (int i = 0; i < len; i++) {
        if (text[i] == '.') {
            dots++;
        }
    }
 spaceCounts = (int*)malloc(dots * sizeof(int));
    // Второй проход: заполняем массив
    dots = 0;
    spaceCounter = 0;

    for (int i = 0; i <= len; i++) {
        if (text[i] == '.' || text[i] == '\0') {
            spaceCounts[dots++] = spaceCounter;
            spaceCounter = 0;
        }
        else if (text[i] == ' ') {
            spaceCounter++;
        }
    }

    *dotCount = dots;
    return spaceCounts;
}
int shotchic(int *spaceCounts,int dotCount){
    int shotchic=0;
    int i;
    for (int i = 1; i < dotCount-2; i++) {
            if (spaceCounts[i-1]-8 < spaceCounts [i] || spaceCounts [i] < spaceCounts[i-1]+8){
            shotchic++;
            }
        }
    return shotchic;
}
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
