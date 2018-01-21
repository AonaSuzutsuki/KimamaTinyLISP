#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Entry Point
"""

import argparse
from tinylisp.interpreter import LispInterpreter

def main():
    """
        main function.
        :return: exit code
    """

    parser = argparse.ArgumentParser(description='Tiny LISP Interpreter on Python 3')
    parser.add_argument('file', nargs='?', help='Tiny LIST format file.')
    parser.add_argument('-p', dest='parser', nargs='?', default='./parser', help='Executable parser file.')
    parser.add_argument('-n', dest='native', nargs='?', help='Use parser on LispInterpreter.')
    parser.add_argument('-t', dest='trace', nargs='?', default=False, help='Whether to trace [true/false]')
    args = parser.parse_args()

    import Translator
    translator = Translator.Translator(args.parser)

    if args.native is not None:
        code = LispInterpreter.repl(args.trace == 'true')
        return code
    elif args.file is not None:
        code = LispInterpreter.repl_with_list_from_file(args.file, translator, args.trace == 'true')
        return code

    code = LispInterpreter.repl_with_asm(translator, args.trace)
    return code


if __name__ == '__main__':
    exit(main())
