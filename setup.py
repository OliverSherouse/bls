"""A setuptools based setup module.

See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""

import os
import re

# Always prefer setuptools over distutils
from setuptools import setup
# To use a consistent encoding
from codecs import open


def read(*names, **kwargs):
    with open(
        os.path.join(os.path.dirname(__file__), *names),
        encoding=kwargs.get('encoding', 'utf8')
    ) as fp:
        return fp.read()


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError('Unable to find version string.')


long_description = read('README.rst')
version = find_version('bls', '__init__.py')

setup(
    name='bls',
    version=version,
    author='Oliver Sherouse',
    author_email='oliver@oliversherouse.com',
    packages=['bls'],
    url='https://github.com/OliverSherouse/bls',
    description='A library to access Bureau of Labor Statistics data',
    install_requires=[
        'pandas',
        'requests',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        ('License :: OSI Approved :: '
         'GNU General Public License v2 or later (GPLv2+)'),
        'Operating System :: OS Independent',
        'Topic :: Scientific/Engineering',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    keywords='economics policy government labor data',
)
