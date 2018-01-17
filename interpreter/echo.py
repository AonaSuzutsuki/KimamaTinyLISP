#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    echo on Python 3.
    Absorb the difference between Windows and Linux echo commands.
"""


import sys


def main():
    """
        main function.
        :return: exit code
    """

    args = sys.argv
    if len(args) > 1:
        arg = args[1]
        if isinstance(arg, str):
            arg = arg.replace('"', '')
            print(arg)


if __name__ == '__main__':
    exit(main())
