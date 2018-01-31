#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""
    Manage error message.
"""


class Error:
    """
        Manage error message.
    """
    def __init__(self, err_msg):
        self._err_msg = err_msg

    @property
    def err_msg(self):
        """
            Get an error message.
            :return: Error message
        """
        return self._err_msg
