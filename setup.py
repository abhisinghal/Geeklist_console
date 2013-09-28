#!/usr/bin/env python

from setuptools import setup, Extension, Command, find_packages
import sys,os,platform
osname=platform.uname()[0].lower()


VERSION = '0.1'
DESCRIPTION = "It is a console based client written in python to access content of https://geekli.st website."
LONG_DESCRIPTION = """
It is a console based client written in python to access content of https://geekli.st website. You can view micros, post micros etc in a geeky way now.
Go on and make an account on https://geekli.st and join an amazing community of geeks.
"""


CLASSIFIERS = filter(None, map(str.strip,
"""
Intended Audience :: Geeks!
License :: Apache License version 2.0
Programming Language :: Python
Operating System :: Linux :: MacOS X
Topic :: Command Line Tool
""".splitlines()))

setup(
    name="Geeklist Console",
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    classifiers=CLASSIFIERS,
    author="Bhavyanshu Parasher",
    author_email="bhavyanshu.spl@gmail.com",
    url="https://github.com/bhavyanshu/Geeklist_console",
    license="Apache License, Version 2.0",
    packages = find_packages(),
    platforms=['any'],
    zip_safe=True,
    install_requires = [
        'setuptools',
        'docutils',
	'rauth',
	'simplejson'
        ],
)

