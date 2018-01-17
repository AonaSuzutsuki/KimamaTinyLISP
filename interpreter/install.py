#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, os, shutil


def copyfile(filename):
    if os.path.exists(filename):
        shutil.copyfile(filename, '../bin/' + filename)


def main():
    if not os.path.exists('../bin'):
        os.mkdir('../bin')

    run = 'run.py'
    setup = 'setup.py'
    translator = 'Translator.py'
    echo = 'echo.py'

    copyfile(run)
    copyfile(setup)
    copyfile(translator)
    copyfile(echo)
    if not os.path.exists('../bin/tinylisp'):
        shutil.copytree("tinylisp", "../bin/tinylisp")


if __name__ == '__main__':
    exit(main())