#!/usr/bin/env python
# -*- coding: utf-8 -*-


class Procedure(object):
    """
        A user-defined Scheme procedure.
    """
    def __init__(self, parms, exp, env):
        self.parms, self.exp, self.env = parms, exp, env

    def __call__(self, *args):
        return eval(self.exp, Env(self.parms, args, self.env))