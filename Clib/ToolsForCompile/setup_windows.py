"""
Компиляция alg_wrapper в один .pyd файл (Windows).

Требования:
    pip install cython setuptools
    + Visual Studio Build Tools (MSVC) — рекомендуется
      https://visualstudio.microsoft.com/visual-cpp-build-tools/
    ИЛИ MinGW-w64 (если хотите gcc вместо MSVC)

Запуск из папки Clib/ToolsForCompile:
    python setup_windows.py build_ext --inplace

Результат — файл вида:
    alg_wrapper.cp311-win_amd64.pyd   (или cp312, зависит от версии Python)

Скопируйте его в Clib/Windows/ для замены старого.
"""
from setuptools import setup, Extension
from Cython.Build import cythonize

ext = Extension(
    name="alg_wrapper",
    sources=["alg_wrapper.pyx", "Alg.c"],   # Cython + C — всё в одном .pyd
    include_dirs=["."],                       # папка, где лежит Alg.h
    extra_compile_args=["/O2"],               # оптимизация MSVC (для MinGW замените на ["-O2"])
)

setup(
    name="AlgWrapper",
    ext_modules=cythonize([ext], compiler_directives={"language_level": "3"}),
)
