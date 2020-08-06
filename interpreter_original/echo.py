#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    echo on Python 3.
    Absorb the difference between Windows and Linux echo commands.
"""


import argparse


def main():
    """
        main function.
        :return: exit code
    """

    parser = argparse.ArgumentParser(description='echo on Python 3')
    parser.add_argument('message', nargs='?', help='Tiny LIST format file.')
    args = parser.parse_args()

    if args.message:
        arg = args.message
        if isinstance(arg, str):
            # arg = arg.replace('"', '\\"')
            print(arg, end='')


if __name__ == '__main__':
    exit(main())
