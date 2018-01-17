#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Processing system for communicating the LISP syntax to the parser.
"""

import subprocess


class Translator:
    """
        Processing system for communicating the LISP syntax to the parser
    """
    def __init__(self, formatter, parser):
        self._formatter = formatter
        self._parser = parser
        self._command = 'python echo.py "{0}" | {2}'

    def send(self, text):
        """
            Send the LISP syntax to the parser.
            :param text: LISP syntax text
            :return: Tiny LIST
        """
        text = text.replace('\r', '').replace('\n', '')
        command = self._command.format(text, self._formatter, self._parser)
        stdout_data = subprocess.check_output(command, shell=True, stderr=subprocess.DEVNULL)
        stdout_data = stdout_data.decode("utf-8")
        return stdout_data
