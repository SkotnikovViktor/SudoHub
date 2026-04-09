#include "Alg.h"
#include <string.h>
#include <stdio.h>
#include <stdlib.h>

void compute_prefix_function(char *obraz, int *pi, int m) {
    pi[0] = 0;
    for (int i = 1; i < m; i++) {
        int j = pi[i-1];
        while (j > 0 && obraz[i] != obraz[j])
            j = pi[j-1];
        if (obraz[i] == obraz[j])
            j++;
        pi[i] = j;
    }
}

int Knut_Morris_Pratta(char *obraz, char *str) {
    int n = (int)strlen(str);
    int m = (int)strlen(obraz);

    if (m == 0) return 0;

    /* MSVC не поддерживает VLA — используем malloc */
    int *pi = (int*)malloc(m * sizeof(int));
    if (!pi) return -1;

    compute_prefix_function(obraz, pi, m);

    int counter = 0;
    int j = 0;

    for (int i = 0; i < n; i++) {
        while (j > 0 && str[i] != obraz[j])
            j = pi[j-1];
        if (str[i] == obraz[j])
            j++;
        if (j == m) {
            counter++;
            j = pi[j-1];
        }
    }

    free(pi);
    return counter;
}

int* countSpacesBeforeEachDot(const char *text, int *dotCount) {
    int len = (int)strlen(text);
    int *spaceCounts = NULL;
    int spaceCounter = 0;
    int dots = 0;

    for (int i = 0; i < len; i++) {
        if (text[i] == '.') dots++;
    }

    spaceCounts = (int*)malloc(dots * sizeof(int));
    if (!spaceCounts) { *dotCount = 0; return NULL; }

    dots = 0;
    spaceCounter = 0;

    for (int i = 0; i <= len; i++) {
        if (text[i] == '.' || text[i] == '\0') {
            spaceCounts[dots++] = spaceCounter;
            spaceCounter = 0;
        } else if (text[i] == ' ') {
            spaceCounter++;
        }
    }

    *dotCount = dots;
    return spaceCounts;
}

int shotchic(int *spaceCounts, int dotCount) {
    int result = 0;
    for (int i = 1; i < dotCount - 2; i++) {
        if (spaceCounts[i-1] - 8 < spaceCounts[i] || spaceCounts[i] < spaceCounts[i-1] + 8) {
            result++;
        }
    }
    return result;
}
