"""Setup for the valve package."""

# !/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import warnings
import setuptools
import versioneer


# Require Python 3.4 or higher
if sys.version_info.major < 3 or sys.version_info.minor < 4:
    warnings.warn("valve requires Python 3.4 or higher!")
    sys.exit(1)


INSTALL_REQUIRES = ['pymongo>=3.4', 'strct']
TEST_REQUIRES = ['pytest', 'coverage', 'pytest-cov']

with open('README.rst') as f:
    README = f.read()

setuptools.setup(
    author="Shay Palachy",
    author_email="shay.palachy@gmail.com",
    name='valve',
    description='Automate and version datasets generation from data sources.',
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    long_description=README,
    url='https://github.com/shaypal5/valve',
    packages=setuptools.find_packages(),
    include_package_data=True,
    entry_points='''
        [console_scripts]
        valve=valve.scripts.valve_cli:cli
    ''',
    install_requires=[
        INSTALL_REQUIRES
    ],
    extras_require={
        'test': TEST_REQUIRES + INSTALL_REQUIRES,
    },
    classifiers=[
        # Trove classifiers
        # (https://pypi.python.org/pypi?%3Aaction=list_classifiers)
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Intended Audience :: Developers',
    ],
)
