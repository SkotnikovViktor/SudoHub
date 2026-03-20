# setup.py
from setuptools import setup, Extension
from Cython.Build import cythonize

ext = Extension(
    name="alg_wrapper",
    sources=["alg_wrapper.pyx", "Alg.c"],   # включаем исходный C-файл
    include_dirs=["."],                     # папка, где лежит Alg.h
)

setup(
    name="AlgWrapper",
    ext_modules=cythonize([ext]),
)
