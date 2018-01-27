#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""
    An environment: a dict of {'var':val} pairs, with an outer Env.
"""


from tinylisp.interpreter import Error


class Env(dict):
    """
        An environment: a dict of {'var':val} pairs, with an outer Env.
    """

    def __init__(self, parms=(), args=(), outer=None):
        super().__init__()
        self.update(zip(parms, args))
        self._outer = outer

    def find(self, var):
        """
            Find the innermost Env where var appears.
        """
        # return self if var in self else self._outer.find(var)
        if var in self:
            return self
        try:
            return self._outer.find(var)
        except AttributeError:
            return Error.Error("AttributeError: '{0}' object not defined.".format(var))
