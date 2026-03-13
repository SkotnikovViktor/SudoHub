#include"Alg.H"
#include <string.h> 
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

// str строка поиска.
// obraz образец, который ищем.
// pi массив длин префиксов для образца (минимум  сколько символов в образце).
// int f(size_t i) когда образец найден, вызывается эта функция,
// ей передается индекс начала найденного в str образца.
// функция возвращает 0, если надо прекратить поиск и 1, если надо продолжить.

// Поиск всех вхождений образца в строку
int Knut_Morris_Pratta(char *obraz, char *str) {
    int n = strlen(str);
    int m = strlen(obraz);

    if (m == 0) return 0;  // Пустой образец

    int pi[m];
    compute_prefix_function(obraz, pi, m); 

    int counter = 0;
    int j = 0;  // текущая позиция в образце

    for (int i = 0; i < n; i++) {
        // Пока несовпадение - откатываемся по префикс-функции
        while (j > 0 && str[i] != obraz[j])
            j = pi[j-1];

        // Если символы совпали
        if (str[i] == obraz[j])
            j++;

        // Если нашли полное вхождение
        if (j == m) {
            counter++;
            j = pi[j-1];  // продолжаем поиск следующих вхождений
        }
    }

    return counter;
}

