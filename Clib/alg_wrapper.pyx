# alg_wrapper.pyx
cdef extern from "Alg.h":
    int Knut_Morris_Pratta(char *obraz, char *str)
    int* countSpacesBeforeEachDot(const char *text, int *dotCount)
    int shotchic(int *spaceCounts, int dotCount)

from libc.stdlib cimport free, malloc

def knut_morris_pratta(str obraz, str text):
    cdef bytes b_obraz = obraz.encode('utf-8')
    cdef bytes b_text = text.encode('utf-8')
    return Knut_Morris_Pratta(b_obraz, b_text)

def count_spaces_before_each_dot(str text):
    cdef bytes b_text = text.encode('utf-8')
    cdef int dotCount = 0
    cdef int* spaces = countSpacesBeforeEachDot(b_text, &dotCount)
    # Преобразуем C-массив в Python-список
    result = [spaces[i] for i in range(dotCount)]
    # Освобождаем память, выделенную в C-функции
    free(spaces)
    return result

def py_shotchic(space_counts):
    """Обёртка для C-функции shotchic, принимает Python-список."""
    cdef int n = len(space_counts)
    cdef int* c_arr = <int*> malloc(n * sizeof(int))
    if c_arr == NULL:
        raise MemoryError("Не удалось выделить память для массива")
    # Копируем данные из Python-списка в C-массив
    for i in range(n):
        c_arr[i] = space_counts[i]
    cdef int result = shotchic(c_arr, n)
    free(c_arr)
    return result
