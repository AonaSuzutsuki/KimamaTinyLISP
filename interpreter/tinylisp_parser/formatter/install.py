#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, os, shutil


def main():
    if not os.path.exists('../../../bin/interpreter'):
        os.makedirs('../../../bin/interpreter')

    args = sys.argv
    if len(args) > 1:
        filename = args[1]
        if os.path.exists(filename):
            shutil.copyfile(filename, '../../../bin/interpreter/' + filename)


if __name__ == '__main__':
    exit(main())