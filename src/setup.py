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
        import unittest
        import sys
        t1r = unittest.main(module='tests', exit=False, argv=[sys.argv[0]])
        t2r = unittest.main(module='test_directoryentry', exit=False, argv=[sys.argv[0]])
        total = t1r.result.testsRun + t2r.result.testsRun
        xfail_fail = len(t1r.result.expectedFailures
                         + t2r.result.expectedFailures)
        xfail_success = len(t1r.result.unexpectedSuccesses
                            + t2r.result.unexpectedSuccesses)
        skipped = len(t1r.result.skipped + t2r.result.skipped)
        failures = len(t1r.result.failures + t2r.result.failures)
        errors = len(t1r.result.errors + t2r.result.errors)
        success = total - xfail_fail - xfail_success - skipped - failures - errors
        print "********************"
        print "  Overall results:"
        print ""
        print "  successes             ", success
        print "  skipped               ", skipped
        print "  expected failures     ", xfail_fail
        print "  total pass            ", (success + skipped + xfail_fail)
        print ""
        print "  errors                ", errors
        print "  failures              ", failures
        print "  unexpected successes  ", xfail_success
        print "  total fail            ", (errors + failures + xfail_success)
        print ""
        print "  total                 ", total

        if xfail_success + failures + errors > 0:
            sys.exit(1)

    sub_commands = []
    user_options = []

##############################################
setup(
    cmdclass    = {'build_ext': build_ext,
                   'test'     : TestCommand},
    ext_modules = [Extension("posix_bare", ["lib/posix_bare.pyx"])],
    package_dir = {'': 'lib'},
    py_modules  = ['generic', 'posix_wrapper']
)
