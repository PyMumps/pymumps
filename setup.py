#!/usr/bin/env python

import os
from setuptools import setup, Extension

try:
    import Cython
except ImportError:
    raise ImportError('''
Cython is required for building this package. Please install using

    pip install cython

or upgrade to a recent PIP release.
''')


with open('README.md') as f:
    long_description = f.read()

extension_kwargs = {
        'libraries': os.environ.get('PYMUMPS_SETUP_LIBRARIES', 'dmumps').split(':')
        }
if 'PYMUMPS_SETUP_INCLUDE_DIRS' in os.environ:
    extension_kwargs['include_dirs'] = \
        os.environ['PYMUMPS_SETUP_INCLUDE_DIRS'].split(':')
if 'PYMUMPS_SETUP_LIBRARY_DIRS' in os.environ:
    extension_kwargs['library_dirs'] = \
        os.environ['PYMUMPS_SETUP_LIBRARY_DIRS'].split(':')
if 'PYMUMPS_SETUP_EXTRA_OBJECTS' in os.environ:
    extension_kwargs['extra_objects'] = \
        os.environ['PYMUMPS_SETUP_EXTRA_OBJECTS'].split(':')


setup(
    name='PyMUMPS',
    version='0.3.2',
    description='Python bindings for MUMPS, a parallel sparse direct solver',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Bradley M. Froehle',
    author_email='brad.froehle@gmail.com',
    maintainer='Stephan Rave',
    maintainer_email='stephan.rave@uni-muenster.de',
    license='BSD',
    url='http://github.com/pymumps/pymumps',
    packages=['mumps'],
    ext_modules=[
        Extension(
            'mumps._dmumps',
            sources=['mumps/_dmumps.pyx'],
            **extension_kwargs
        ),
    ],
    install_requires=['mpi4py'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Scientific/Engineering :: Mathematics',
    ],
)
