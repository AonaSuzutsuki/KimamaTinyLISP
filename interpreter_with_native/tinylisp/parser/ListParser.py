#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Parse TinyLIST from yacc tree.
"""


def car(list):
    if isinstance(list, str):
        return list
    return list[0]


def cdr(list):
    return list[1:]


class ListParser():
    """
        Parse TinyLIST from yacc tree.
    """

    def __init__(self):
        return

    def parse(self, text):
        pList = []
        tokens = ListParser._preparse(text)

        while len(tokens) > 0:
            token = ListParser._convert_list(tokens)
            pList.append(ListParser._parse(token, []))
        return pList

    @staticmethod
    def _parse(aList, rList):
        for elem in aList:
            if isinstance(elem, list):
                celem = car(elem)
                if celem == 'LIST':  # ネストされたリスト判定
                    rList.append(ListParser._parse(cdr(elem), []))
                elif celem == 'ATOM':  # アトム判定
                    (id, val) = cdr(elem)[0]
                    val = ListParser._resolve(id, val)
                    rList.append(val)
                else:
                    ListParser._parse(elem, rList)
            elif elem == 'LIST':  # 一番初めのリスト判定
                ListParser._parse(elem, rList)
        return rList

    @staticmethod
    def _resolve(id, val):
        if id == 'IDENTIFIER':
            return str(val)
        elif id == 'INTEGER':
            return int(val)
        elif id == 'FLOAT':
            return float(val)

    @staticmethod
    def _replace_newline(text):
        text = text.replace('\r\n', '\r')
        text = text.replace('\r', '\n')
        return text

    @staticmethod
    def _preparse(text):
        text = ListParser._replace_newline(text).replace('\n', '')
        text = text.replace('(', ' ( ').replace(')', ' ) ').split()
        return text

    @staticmethod
    def _convert_list(tokens):
        token = tokens.pop(0)
        if token == '(':
            list = []
            while tokens[0] != ')':
                list.append(ListParser._convert_list(tokens))
            tokens.pop(0)  # pop off ')'
            return list
        return token


def main():
    text = """
(LIST
        (
            (
                (ATOM
                    (IDENTIFIER defun))
                (ATOM
                    (IDENTIFIER test)))
            (LIST
                (
                    (
                        (ATOM
                            (IDENTIFIER lambda))
                        (LIST
                            (
                                (
                                    (ATOM
                                        (IDENTIFIER a))
                                    (ATOM
                                        (IDENTIFIER b)))
                                (ATOM
                                    (IDENTIFIER c)))))
                    (LIST
                        (
                            (
                                (ATOM
                                    (IDENTIFIER +))
                                (ATOM
                                    (IDENTIFIER a)))
                            (LIST
                                (
                                    (
                                        (ATOM
                                            (IDENTIFIER +))
                                        (ATOM
                                            (IDENTIFIER b)))
                                    (ATOM
                                        (IDENTIFIER c))))))))))
"""
    text2 = """
(LIST
        (
            (
                (ATOM
                    (IDENTIFIER +))
                (ATOM
                    (INTEGER 1)))
            (LIST
                (
                    (
                        (ATOM
                            (IDENTIFIER +))
                        (ATOM
                            (INTEGER 1)))
                    (ATOM
                        (INTEGER 2))))))
"""
    listParser = ListParser()
    pList = listParser.parse(text)
    print(pList)
    pList = listParser.parse(text2)
    print(pList)
    return 0


if __name__ == '__main__':
    exit(main())