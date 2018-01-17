#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

"""

import subprocess


class Translator:
    """

    """
    def __init__(self, formatter, parser):
        self._formatter = formatter
        self._parser = parser
        self._command = 'python echo.py "{0}" | {1} | {2}'

    def send(self, text):
        text = text.replace('\r', '').replace('\n', '')
        command = self._command.format(text, self._formatter, self._parser)
        proc = subprocess.Popen(
            command,
            shell=True,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        #stdout_data = proc.stdout.readline()
        stdout_data = subprocess.check_output(command, shell=True, stderr=subprocess.DEVNULL)
        stdout_data = stdout_data.decode("utf-8")
        return stdout_data
