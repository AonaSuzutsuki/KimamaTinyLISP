#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Parse TinyLIST from yacc tree.
"""


class ListParser:
    """
        Parse TinyLIST from yacc tree.
    """

    def __init__(self):
        return

    @staticmethod
    def parse(text):
        """
            Do parse yacc tree.
            :param text:
            :return:
        """
        p_list = []
        tokens = ListParser._preparse(text)

        while tokens:
            token = ListParser._convert_list(tokens)
            p_list.append(ListParser._parse(token, []))
        return p_list

    @staticmethod
    def car(a_list):
        """
            Get a car element from list.
            :param a_list:
            :return:
        """
        if isinstance(a_list, str):
            return a_list
        return a_list[0]

    @staticmethod
    def cdr(a_list):
        """
            Get a cdr elements from list.
            :param a_list:
            :return:
        """
        return a_list[1:]

    @staticmethod
    def _parse(a_list, ret_list):
        car = ListParser.car
        cdr = ListParser.cdr
        for elem in a_list:
            if isinstance(elem, list):
                top_elem = car(elem)
                if top_elem == 'LIST':  # ネストされたリスト判定
                    ret_list.append(ListParser._parse(cdr(elem), []))
                elif top_elem == 'EMPTY':
                    return []
                elif top_elem == 'ATOM':  # アトム判定
                    (nid, val) = cdr(elem)[0]
                    val = ListParser._resolve_atom(nid, val)
                    ret_list.append(val)
                else:
                    ListParser._parse(elem, ret_list)
            elif elem == 'LIST':  # 一番初めのリスト判定
                ListParser._parse(elem, ret_list)
            elif elem == 'ATOM':
                (nid, val) = cdr(a_list)[0]
                val = ListParser._resolve_atom(nid, val)
                return val
        return ret_list

    @staticmethod
    def _resolve_atom(nid, val):
        """
            Convert yacc tree atom to python value.
            :param nid:
            :param val:
            :return:
        """
        if nid == 'IDENTIFIER':
            text = str(val)
            if text == 'nil':
                return None
            return text
        elif nid == 'WQUOTED':
            text = str(val)
            return '"' + text + '"'
        elif nid == 'INTEGER':
            return int(val)
        elif nid == 'FLOAT':
            return float(val)

    @staticmethod
    def _replace_newline(text):
        """
            Unify newline to LF.
            :param text:
            :return:
        """
        text = text.replace('\r\n', '\r')
        text = text.replace('\r', '\n')
        return text

    @staticmethod
    def _preparse(text):
        """
            Prepare before analysis.
            Make tokens.
            :param text: yacc tree text
            :return: token python list.
        """
        import shlex
        text = ListParser._replace_newline(text).replace('\n', '')
        text = text.replace('(', ' ( ').replace(')', ' ) ')
        a_list = shlex.split(text)
        return a_list

    @staticmethod
    def _convert_list(tokens):
        """
            Convert tokens to yacc tree of python list.
            :param tokens:
            :return:
        """
        token = tokens.pop(0)
        if token == '(':
            a_list = []
            while tokens[0] != ')':
                a_list.append(ListParser._convert_list(tokens))
            tokens.pop(0)  # pop off ')'
            return a_list
        return token


def main():
    """
        main function.
        :return: exit code
    """
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
    list_parser = ListParser()
    p_list = list_parser.parse(text)
    print(p_list)
    return 0


if __name__ == '__main__':
    exit(main())
