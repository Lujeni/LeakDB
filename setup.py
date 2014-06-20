#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup
from setuptools import find_packages

setup(
    name="LeakDB",
    version="0.1",
    packages=find_packages(),
    author="Lujeni",
    author_email="julien@thebault.co",
    description="LeakDB is a very simple and fast key value store for Python",
    long_description=open('README.rst').read(),
    install_requires=['gevent'],
    include_package_data=True,
    url='https://github.com/Lujeni/LeakDB',
    classifiers=[
        "Programming Language :: Python :: 2.7",
        "Development Status :: 1 - Planning",
        "License :: OSI Approved :: BSD License",
        "Natural Language :: English",
        "Operating System :: Unix",
    ]
)
