#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, os, shutil


def copyfile(filename, path='../bin/interpreter/'):
    if os.path.exists(filename):
        shutil.copyfile(filename, path + filename)


def main():
    if not os.path.exists('../bin/interpreter'):
        os.makedirs('../bin/interpreter')

    run = 'run.py'
    setup = 'setup.py'
    translator = 'Translator.py'
    echo = 'echo.py'
    runbat = 'run.bat'

    copyfile(run)
    copyfile(setup)
    copyfile(translator)
    copyfile(echo)
    copyfile(runbat, '../bin/')
    if not os.path.exists('../bin/interpreter/tinylisp'):
        shutil.copytree("tinylisp", "../bin/interpreter/tinylisp")


if __name__ == '__main__':
    exit(main())