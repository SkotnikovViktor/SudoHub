import sys
import os

# Добавляем папку ToolsForCompile в путь, чтобы найти скомпилированный alg_wrapper.so
_HERE = os.path.dirname(os.path.abspath(__file__))
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

import alg_wrapper


def resultSpacesAndCount(text):
    # 2. Подсчёт пробелов перед точками
    spaces = alg_wrapper.count_spaces_before_each_dot(text)
    # 3. Вычисление "shotchic"
    result_1 = alg_wrapper.py_shotchic(spaces) + 1
    result = [result_1, len(spaces) - 1] 
    return result

