#!/usr/bin/env python

from distutils.core import setup, Extension

setup(
    name='PyMUMPS',
    version='0.1',
    description='Python bindings for MUMPS, a parallel sparse direct solver',
    author='Bradley M. Froehle',
    author_email='brad.froehle@gmail.com',
    license='BSD',
    url='http://github.com/bfroehle/pymumps',
    packages=['mumps'],
    ext_modules=[
        Extension(
            'mumps._dmumps',
            sources=['mumps/_dmumps.c'],
            libraries=['dmumps'],
        ),
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Scientific/Engineering :: Mathematics',
    ],
)
