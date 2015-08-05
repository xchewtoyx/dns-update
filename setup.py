#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name='dnsupdater',
    version='0.1.0',
    description='Update DNS record via joker.com API',
    author='Russell Heilling',
    author_email='russell@heilling.net',
    entry_points={
        'console_scripts': [
            'dns-update = dnsupdater.main:run',
        ],
    },
    packages=find_packages(),
    install_requires=[
        'cement',
    ],
)

