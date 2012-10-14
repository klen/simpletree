#!/usr/bin/env python
import os

from setuptools import setup

from simpletree import __version__, __project__, __license__


def read(fname):
    try:
        return open(os.path.join(os.path.dirname(__file__), fname)).read()
    except IOError:
        return ''


META_DATA = dict(
    name=__project__,
    version=__version__,
    license=__license__,
    description=read('DESCRIPTION'),
    long_description=read('README.rst'),
    platforms=('Any'),

    author='Kirill Klenov',
    author_email='horneds@gmail.com',
    url=' http://github.com/klen/djang-tree',

    packages=['simpletree'],

    install_requires = ('Django>=1.2'),
    test_suite = 'tests.run_tests',
    tests_require = ['milkman']
)


if __name__ == "__main__":
    setup(**META_DATA)
