#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
ソースコードディストリビューション（sdist）のための設え（しつらえ：setup）です。
$ python setup.py sdist
"""

__author__ = 'Aona Suzutsuki'
__version__ = '1.0.0'
__date__ = '2018/01/17 (Created: 2018/01/17)'

from distutils.core import setup

setup(
    name='TinyLISP',
    version=__version__,
    description='',
    url='http://kimamalab.azurewebsites.net',
    author=__author__,
    author_email='aonasuzutsuki@gmail.com',
    license='',
    long_description='',
    platforms='Windows 10',
    packages=['tinylisp'],
    )
