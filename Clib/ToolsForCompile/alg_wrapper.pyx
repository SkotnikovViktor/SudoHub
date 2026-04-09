# cython: language_level=3
from libc.stdlib cimport malloc, free

# Объявляем C-функции из Alg.h
cdef extern from "Alg.h":
    int*  countSpacesBeforeEachDot(const char *text, int *dotCount)
    int   shotchic(int *spaceCounts, int dotCount)
    int   Knut_Morris_Pratta(char *obraz, char *strr)


def count_spaces_before_each_dot(text: str) -> list:
    """Возвращает список — количество пробелов перед каждой точкой."""
    cdef int dotCount = 0
    cdef int *spaceCounts

    text_bytes = text.encode("utf-8")
    spaceCounts = countSpacesBeforeEachDot(text_bytes, &dotCount)

    result = [spaceCounts[i] for i in range(dotCount)]
    free(spaceCounts)
    return result


def py_shotchic(spaces: list) -> int:
    """Вычисляет shotchic по списку пробелов (возвращённому count_spaces_before_each_dot)."""
    cdef int dotCount = len(spaces)
    if dotCount == 0:
        return 0

    cdef int *arr = <int*>malloc(dotCount * sizeof(int))
    if arr == NULL:
        raise MemoryError()

    for i in range(dotCount):
        arr[i] = spaces[i]

    cdef int result = shotchic(arr, dotCount)
    free(arr)
    return result


def kmp_search(pattern: str, text: str) -> int:
    """Алгоритм Кнута–Морриса–Пратта: количество вхождений pattern в text."""
    p = pattern.encode("utf-8")
    t = text.encode("utf-8")
    return Knut_Morris_Pratta(p, t)
