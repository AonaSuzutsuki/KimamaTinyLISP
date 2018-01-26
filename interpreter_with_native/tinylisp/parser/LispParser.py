#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Provide conversion system from token to Python list.
"""

from tinylisp.parser import LispLexer


class LispParser:
    """
        Provide conversion system from token to Python list.
    """

    def parse(self, _tokens):
        """
            Read the expression from the token column.
        """
        if not _tokens:
            raise SyntaxError('unexpected EOF while reading')
        token = _tokens.pop(0)
        if token == '(':
            token_list = []
            while _tokens[0] != ')':
                token_list.append(self.parse(_tokens))
            _tokens.pop(0)  # pop off ')'
            return token_list
        elif token == ')':
            raise SyntaxError('unexpected )')
        else:
            return LispParser._atom(token)

    @staticmethod
    def _atom(token):
        """
            The string number is a number, and the other tokens are symbols.
        """
        try:
            return int(token)
        except ValueError:
            try:
                return float(token)
            except ValueError:
                return str(token)


def main():
    """
        main function.
        :return: exit code
    """
    lexer = LispLexer.LispLexer()
    parser = LispParser()
    tokens = lexer.make_token('(defun plus (lambda (a b) (+ a b)))')
    lisp_list = parser.parse(tokens)
    assert ['defun', 'plus', ['lambda', ['a', 'b'], ['+', 'a', 'b']]] == lisp_list, "no"
    print(lisp_list)
    return 0


if __name__ == '__main__':
    exit(main())
