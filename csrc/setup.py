from distutils.core import setup, Extension

module1 = Extension('pyreaddir_c',
                    sources = ['readdir.c'])

setup (name = 'PyReaddir_c',
       version = '0.0.1',
       description = 'C-to-Python bridge for readdir()',
       ext_modules = [module1])

