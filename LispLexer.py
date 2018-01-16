#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Provide conversion system from string to token list.
"""

import Common


class LispLexer:
    """
        Provide conversion system from string to token list.
    """

    def make_token(self, text):
        """
            Make token list from string.
            :param text: LISP Source text
            :return: Token list
        """
        text = self._replace_newline(text).replace('\n', '')
        text = text.replace('(', ' ( ').replace(')', ' ) ').split()
        return text

    @classmethod
    def _replace_newline(cls, text):
        """
            Replace newline to LF.
            :param text: String to be converted
            :return: Converted String
        """
        text = text.replace('\r\n', '\r')
        text = text.replace('\r', '\n')
        return text


def main():
    """
        main function.
        :return: exit code
    """
    lexer = LispLexer()
    tokens = lexer.make_token(Common.test_src)
    assert ['(', 'defun', 'plus', '(', 'lambda', '(', 'a', 'b', ')', '(', '+', 'a', 'b', ')', ')', ')'] == tokens, "no"
    print(tokens)
    return 0


if __name__ == '__main__':
    exit(main())
