from setuptools import setup, Extension

module = Extension(
    'alg_wrapper',
    sources=['Alg.c'],
    include_dirs=['.'],
)

setup(
    name='alg_wrapper',
    ext_modules=[module],
)