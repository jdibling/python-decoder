from __future__ import print_function
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand

import decoder

class Tox(TestCommand):
    user_options = [('tox-args=', 'a', "Arguments to pass to tox")]
    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.tox_args = None
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True
    def run_tests(self):
        #import here, cause outside the eggs aren't loaded
        import tox
        import shlex
        args = self.tox_args
        if args:
            args = shlex.split(self.tox_args)
        errno = tox.cmdline(args=args)
        sys.exit(errno)

setup(
    name='decoder',
    version=decoder.__version__,
    packages=find_packages(),
    url='',
    license='',
    author='John Dibling',
    author_email='john.dibling@picotrading.com',
    description='PyDecode',
    tests_require=['tox'],
    install_requires=['PyYAML >= 3.11'],
    cmdclass={'test': Tox},
)
