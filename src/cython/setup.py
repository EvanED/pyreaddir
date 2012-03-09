from distutils.core import setup
from distutils.extension import Extension
from distutils.cmd import Command
from Cython.Distutils import build_ext


class TestCommand(Command):
    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        print "Hello world!"

    sub_commands = []
    user_options = []

##############################################
setup(
    cmdclass    = {'build_ext': build_ext,
                   'test'     : TestCommand},
    ext_modules = [Extension("readdir_bare_posix", ["lib/posix.pyx"])],
    package_dir = {'': 'lib'},
    py_modules  = ['generic', 'posix2']
)
