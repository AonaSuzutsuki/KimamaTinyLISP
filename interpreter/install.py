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
    translator = 'Messenger.py
    echo = 'echo.py'
    common = 'Common.py'
    runbat = 'run.bat'
    runsh = 'run.sh'

    copyfile(run)
    copyfile(setup)
    copyfile(translator)
    copyfile(echo)
    copyfile(common)
    copyfile(runbat, '../bin/')
    copyfile(runsh, '../bin/')
    if not os.path.exists('../bin/interpreter/tinylisp'):
        shutil.copytree("tinylisp", "../bin/interpreter/tinylisp")


if __name__ == '__main__':
    exit(main())