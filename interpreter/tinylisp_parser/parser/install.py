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
    args = parser.parse_args()

    filename = args.file
    if os.path.exists(filename):
        shutil.copyfile(filename, '../../../bin/interpreter/' + filename)
        os.chmod('../../../bin/interpreter/' + filename, 0o700)


if __name__ == '__main__':
    exit(main())