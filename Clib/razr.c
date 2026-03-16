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
    if (spaceCounts == NULL) {
        printf("Ошибка выделения памяти!\n");
        *dotCount = 0;
        return NULL;
    }

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
int shotchic(int dotCount,int *spaceCounts){
    int shotchic=0;
    int i;
    for (int i = 0; i < dotCount-1; i++) {
            shotchic+=spaceCounts[i];
        }
    free(spaceCounts);
    return shotchic/i;
}
int main() {
    char text[] = "Это предложение с тремя пробелами до точки. Второе с двумя пробелами. Третье. Четвертое предложение с четырьмя пробелами до точки.";
    int dotCount;
    int *spaceCounts = countSpacesBeforeEachDot(text, &dotCount);
    return 0;
}
