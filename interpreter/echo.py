#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

"""


import sys


def main():
    args = sys.argv
    if len(args) > 1:
        arg = args[1]
        if isinstance(arg, str):
            arg = arg.replace('"', '')
            print(arg)


if __name__ == '__main__':
    exit(main())
