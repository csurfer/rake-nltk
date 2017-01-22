#!/usr/bin/env python
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.rst')) as f:
    long_description = f.read()

setup(
    # Name of the module
    name='rake_nltk',

    # Details
    version='1.0.0',
    description='Python implementation of the Rapid Automatic Keyword' +
    ' Extraction algorithm using NLTK',
    long_description=long_description,

    # The project's main homepage.
    url='https://github.com/csurfer/rake-nltk',

    # Author details
    author='Vishwas B Sharma',
    author_email='sharma.vishwas88@gmail.com',

    # License
    license='MIT',
    packages=['rake_nltk'],
    test_suite='tests',
    keywords='nlp text-mining algorithms development',
    classifiers=[
        # Intended Audience.
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        # License.
        'License :: OSI Approved :: MIT License',
        # Project maturity.
        'Development Status :: 3 - Alpha',
        # Operating Systems.
        'Operating System :: POSIX',
        # Supported Languages.
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        # Topic tags.
        'Topic :: Software Development :: Build Tools',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    install_requires=['nltk'])
