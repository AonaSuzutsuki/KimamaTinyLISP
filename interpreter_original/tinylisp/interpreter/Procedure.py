#!/usr/bin/env python
# -*- coding: utf-8 -*-


from tinylisp.interpreter.Enviroment import Env


class Procedure(object):
    """
        A user-defined Scheme procedure.
    """
    def __init__(self, parms, exp, env):
        self._parms, self._exp, self._env = parms, exp, env

    # def __call__(self, *args):
    #     return eval(self._exp, Env(self._parms, args, self._env))

    @property
    def exp(self):
        return self._exp

    @property
    def parms(self):
        return self._parms

    @property
    def env(self):
        return self._env
