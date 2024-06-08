#!/usr/bin/env python

import pkgconfig

from setuptools import setup, Extension

try:
    import Cython
except ImportError:
    raise ImportError('''
Cython is required for building this package. Please install using

    pip install cython

or upgrade to a recent PIP release.
''')


extension = Extension(
    'mumps._dmumps',
    sources=['mumps/_dmumps.pyx']
)

use_coinmumps = False

try:
    pkgconfig.configure_extension(extension, 'coinmumps')
    use_coinmumps = True
    print("Using coinmumps library")
except EnvironmentError:
    print("pkg-config not installed, trying to build without it.")
except pkgconfig.PackageNotFoundError:
    print("coinmumps not found by pkg-config, trying to build without it.")

if not use_coinmumps:
    extension.libraries = ['dmumps', 'mumps_common']


with open('README.md') as f:
    long_description = f.read()


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
    ext_modules=[extension],
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
