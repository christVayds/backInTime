from setuptools import setup, Extension
from Cython.Build import cythonize

ext_modules = [
    Extension('main_cython', ['python_cython/main.pyx'])
]

setup(
    name = 'optimized_game',
    ext_modules=cythonize(ext_modules)
)