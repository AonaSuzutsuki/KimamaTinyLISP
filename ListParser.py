#!/usr/bin/env python
# -*- coding: utf-8 -*-

Symbol = str


class ListParser:
    def parse(self, text):
        tokens = self._preparse(text)
        return self._parse(tokens)

    def _flatten(self, tokens):
        list = []
        for token in tokens:
            if token != '(' and token != ')':
                list.append(token)
        return list

    def _preparse(self, text):
        text = text.replace('[', ' [ ')
        text = text.replace(']', ' ] ')
        text = text.replace('(', ' ( ')
        text = text.replace(')', ' ) ')
        text = text.replace(',', '')
        text = text.replace("'", '')
        tokens = text.split()
        tokens = self._flatten(tokens)
        return tokens

    def _parse(self, tokens):
        token = tokens.pop(0)
        if '[' == token:
            L = []
            while tokens[0] != ']':
                L.append(self._parse(tokens))
            tokens.pop(0)  # pop off ')'
            return L
        else:
            return self._atom(token)

    def _atom(self, token):
        try:
            return int(token)
        except ValueError:
            try:
                return float(token)
            except ValueError:
                return Symbol(token)


def main():
    """
        main function.
        :return: exit code
    """
    text = "[test, ['+', (1, 2)]]"
    list_parser = ListParser()
    list = list_parser.parse(text)
    print(list)

    test = ['defun', 'test', ['lambda', ['f'], ['call', 'f']]]

    import LispInterpreter
    interp = LispInterpreter.LispInterpreter()
    interp.eval(test)
    val = interp.eval(list)
    print(val)

    return 0


if __name__ == '__main__':
    exit(main())
