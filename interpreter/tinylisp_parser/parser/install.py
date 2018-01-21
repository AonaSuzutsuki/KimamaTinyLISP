#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, os, shutil, argparse


def w_chmod(path, _):
    """
        Empty function for Windows.
    """
    return 0


def main():
    """
        main function.
        :return: exit code
    """
    if not os.path.exists('../../../bin/interpreter'):
        os.makedirs('../../../bin/interpreter')

    parser = argparse.ArgumentParser(description='installer on Python 3')
    parser.add_argument('file', nargs='?', help='Executable parser file.')
    parser.add_argument('-w', dest='windows', nargs='?', default='false', help='Executable parser file.')
    args = parser.parse_args()

    chmod = os.chmod
    if args.windows == 'true':
        chmod = w_chmod
    filename = args.file
    if os.path.exists(filename):
        shutil.copyfile(filename, '../../../bin/interpreter/' + filename)
        chmod('../../../bin/interpreter/' + filename, 700)


if __name__ == '__main__':
    exit(main())