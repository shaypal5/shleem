"""Setup for the shleem package."""

#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import warnings
import setuptools
import versioneer


# Require Python 3.5 or higher
#if sys.version_info.major < 3 or sys.version_info.minor < 5:
#    warnings.warn("shleem requires Python 3.5 or higher!")
#    sys.exit(1)


INSTALL_REQUIRES = ['pymongo>=3.4', 'strct']
TEST_REQUIRES = ['pytest', 'coverage', 'pytest-cov']

with open('README.rst') as f:
    README = f.read()

setuptools.setup(
    author="Shay Palachy",
    author_email="shay.palachy@gmail.com",
    name='shleem',
    description='Automate and version datasets generation from data sources.',
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    long_description=README,
    url='https://github.com/shaypal5/shleem',
    packages=setuptools.find_packages(),
    include_package_data=True,
    entry_points='''
        [console_scripts]
        shleem=shleem.scripts.shleem_cli:cli
    ''',
    install_requires=[
        INSTALL_REQUIRES
    ],
    extras_require={
        'test': TEST_REQUIRES + INSTALL_REQUIRES,
    }
)
