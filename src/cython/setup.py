from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext

setup(
    cmdclass    = {'build_ext': build_ext},
    ext_modules = [Extension("readdir_bare_posix", ["lib/posix.pyx"])],
    package_dir = {'': 'lib'},
    py_modules  = ['generic', 'posix2']
)
