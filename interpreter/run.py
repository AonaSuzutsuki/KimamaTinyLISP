#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Entry Point
"""

import argparse
import Messenger
from tinylisp.interpreter import LispInterpreter


def main():
    """
        main function.
        :return: exit code
    """

    parser = argparse.ArgumentParser(description='Tiny LISP Interpreter on Python 3')
    parser.add_argument('file', nargs='?', help='Tiny LIST format file.')
    parser.add_argument('-py', dest='python', nargs='?', default='python', help='Executable python command name.')
    parser.add_argument('-p', dest='parser', nargs='?', default='./parser', help='Executable parser file.')
    parser.add_argument('-t', dest='trace', nargs='?', default=False, help='Whether to trace [true/false]')
    args = parser.parse_args()

    translator = Messenger.Messenger(args.python, args.parser)

    if args.file is not None:
        code = LispInterpreter.repl_with_list_from_file(args.file, translator, args.trace == 'true')
        return code

    code = LispInterpreter.repl_with_asm(translator, args.trace == 'true')
    return code


if __name__ == '__main__':
    exit(main())
