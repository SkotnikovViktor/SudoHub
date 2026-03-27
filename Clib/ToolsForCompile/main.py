import alg_wrapper

# 1. Поиск подстроки
text = "abracadabra"
pattern = "abra"
print("Количество вхождений:", alg_wrapper.knut_morris_pratta(pattern, text))

# 2. Подсчёт пробелов перед точками
s = "Hello world.This is a test.Another sentence."
spaces = alg_wrapper.count_spaces_before_each_dot(s)
print("Пробелы перед точками:", spaces)

print(len(spaces))
# 3. Вычисление "shotchic"
result = alg_wrapper.py_shotchic(spaces)+1
print("Результат shotchic:", result)
