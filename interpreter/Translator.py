#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Processing system for communicating the LISP syntax to the parser.
"""

import subprocess
import Common


class Translator:
    """
        Processing system for communicating the LISP syntax to the parser
    """
    def __init__(self, parser):
        self._parser = parser
        self._command = 'python echo.py "{0}" | {1}'

    def send(self, text):
        """
            Send the LISP syntax to the parser.
            :param text: LISP syntax text
            :return: Tiny LIST
        """
        text = text.replace('\r', '').replace('\n', '')
        command = self._command.format(text, self._parser)

        proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        errtext = b''
        text = b''
        while True:
            line = proc.stdout.readline()
            text += line

            errline = proc.stderr.readline()
            if errline != b'':
                errtext += errline

            # バッファが空 + プロセス終了.
            if (not line and not errline)and proc.poll() is not None:
                break

        suc = True
        stdout_data = Common.replace_newline(text.decode('utf-8'))
        stderr_data = Common.replace_newline(errtext.decode('utf-8'))
        if stderr_data != '\nparser successfully ended\n\n':
            stdout_data = stderr_data
            suc = False
        #stdout_data = subprocess.check_output(command, shell=True, stderr=subprocess.DEVNULL)
        #stdout_data = stdout_data.decode("utf-8")
        return suc, stdout_data
