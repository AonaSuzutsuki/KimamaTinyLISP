#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Processing system for communicating the LISP syntax to the parser.
"""

import subprocess
import os
import Common


class Translator:
    """
        Processing system for communicating the LISP syntax to the parser
    """
    def __init__(self, python, parser):
        self._python = python
        self._parser = parser
        self._command = '{0} "{2}{1}echo.py" "{3}" | {2}{1}{4}'
        self._sep = os.sep
        self._dirpath = os.path.dirname(os.path.abspath(__file__))

    def send(self, text):
        """
            Send the LISP syntax to the parser.
            :param text: LISP syntax text
            :return: Tiny LIST
        """
        text = Common.replace_newline(text).replace('\n', '@n').replace('"', '\\"')
        command = self._command.format(self._python, self._sep, self._dirpath, text, self._parser)

        proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        rtext = self.read(proc.stdout.readline)
        errtext = self.read(proc.stderr.readline)
        proc.stdout.close()
        proc.stderr.close()

        suc = True
        stdout_data = Common.replace_newline(rtext.decode('utf-8'))
        stderr_data = Common.replace_newline(errtext.decode('utf-8'))
        if stderr_data != '\nparser successfully ended\n\n':
            stdout_data = stderr_data
            suc = False
        return suc, stdout_data

    @staticmethod
    def read(itr):
        """
            Read from readline
            :param itr: readline function
            :return: read to end text
        """
        text = b''
        for line in iter(itr, b''):
            text += line
        return text
