#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Convert string representation of TinyLIST to Python internal list.
"""

from tinylisp.interpreter import Common


class ListParser:
    """
        Convert string representation of TinyLIST to Python internal list.
    """
    def parse(self, text):
        """
            Parse string representation of TinyLIST to Python internal list.
            :param text: string representation of TinyLIST
            :return: Python internal list
        """
        tokens = ListParser._preparse(text)
        return self._parse(tokens)

    @staticmethod
    def _flatten(tokens):
        list = []
        for token in tokens:
            if token != '(' and token != ')':
                list.append(token)
        return list

    @staticmethod
    def _preparse(text):
        text = text.replace('[', ' [ ')
        text = text.replace(']', ' ] ')
        text = text.replace('(', ' ( ')
        text = text.replace(')', ' ) ')
        text = text.replace(',', '')
        text = text.replace("'", '')
        tokens = text.split()
        tokens = ListParser._flatten(tokens)
        return tokens

    @staticmethod
    def _parse(tokens):
        token = tokens.pop(0)
        if token == '[':
            list = []
            while tokens[0] != ']':
                list.append(ListParser._parse(tokens))
            tokens.pop(0)  # pop off ']'
            return list
        return ListParser._atom(token)

    @staticmethod
    def _atom(token):
        try:
            return int(token)
        except ValueError:
            try:
                return float(token)
            except ValueError:
                return Common.Symbol(token)


def main():
    """
        main function.
        :return: exit code
    """
    text = "[defun, test, [lambda, [a, b, c], [+, a, [+, b, c]]]]" #[test, ['+', (1, 2)]]"
    list_parser = ListParser()
    list = list_parser.parse(text)
    print(list)

    test = ['defun', 'test2', ['lambda', ['f'], ['call', 'f']]]
    test2 = ['test', 1, 2, 3]

    from tinylisp.interpreter import LispInterpreter
    interp = LispInterpreter.LispInterpreter()
    interp.eval(test)
    interp.eval(list)
    val = interp.eval(test2)
    print(val)

    return 0


if __name__ == '__main__':
    exit(main())
