#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Provide conversion system from string to token list.
"""

import Common
import LispLexer
import LispParser
import ListParser


class LispInterpreter:
    def __init__(self):
        self.global_env = LispInterpreter.add_globals(Env())

    @staticmethod
    def add_globals(env):
        """
            環境にScheme標準の手続きをいくつか追加する
        """

        import cmath
        import operator as op

        env.update(vars(cmath))  # sin, sqrt, ...
        env.update(
            {
                '+': op.add, '-': op.sub, '*': op.mul, '/': op.floordiv, 'not': op.not_,
                '>': op.gt, '<': op.lt, '>=': op.ge, '<=': op.le, '=': op.eq,
                'equal?': op.eq, 'eq?': op.is_, 'length': len, 'cons': lambda x, y: [x] + y,
                'car': lambda x: x[0], 'cdr': lambda x: x[1:], 'append': op.add,
                'list': lambda *x: list(x), 'list?': lambda x: isinstance(x, list),
                'null?': lambda x: x == [], 'symbol?': lambda x: isinstance(x, Common.Symbol),
                'print': print
            })
        return env

    def eval(self, x, env=None):
        """
            環境の中で式を評価する。
        """
        if env is None:
            env = self.global_env

        if isinstance(x, Common.Symbol):  # 変数参照
            #t = env.find(x)
            return env.find(x)[x]
        elif not isinstance(x, list):  # 定数リテラル
            return x
        elif x[0] == 'quote':  # (quote exp)
            (_, exp) = x
            return exp
        elif x[0] == 'if':  # (if test conseq alt)
            (_, test, conseq, alt) = x
            return self.eval((conseq if self.eval(test, env) else alt), env)
        elif x[0] == 'set!':  # (set! var exp)
            (_, var, exp) = x
            env.find(var)[var] = self.eval(exp, env)
            return None
        elif x[0] == 'defun':  # (define var exp)
            (_, var, exp) = x
            env[var] = self.eval(exp, env)
            return None
        elif x[0] == 'lambda':  # (lambda (var*) exp)
            (_, vars, exp) = x
            return lambda *args: self.eval(exp, Env(vars, args, env))
        elif x[0] == 'begin':  # (begin exp*)
            for exp in x[1:]:
                val = self.eval(exp, env)
                return val
        elif x[0] == 'call':
            (_, exp) = x
            return self.eval(exp, env)
        elif x[0] == 'exit':
            return 'exit'
        else:  # (proc exp*)
            exps = [self.eval(exp, env) for exp in x]
            proc = exps.pop(0)
            try:
                return proc(*exps)
            except TypeError:
                return x


class Env(dict):
    """
        環境: ペア{'var':val}のdictで、外部環境(outer)を持つ。
    """

    def __init__(self, parms=(), args=(), outer=None):
        super().__init__()
        self.update(zip(parms, args))
        self._outer = outer

    def find(self, var):
        """
            var が現れる一番内側のEnvを見つける。
        """
        # return self if var in self else self._outer.find(var)
        if var in self:
            return self
        return self._outer.find(var)


def to_string(exp):
    """
        PythonオブジェクトをLispの読める文字列に戻す。
        """
    isa = isinstance
    return '(' + ' '.join(map(to_string, exp)) + ')' if isa(exp, list) else str(exp)


def repl(lexerp, parserp, interp, prompt='lispy> '):
    """
        read-eval-print-loopのプロンプト
    """
    while True:
        val = interp.eval(parserp.parse(lexerp.make_token(input(prompt))))
        if val == 'exit':
            break
        elif val is not None:
            print(to_string(val))
        else:
            continue
    return 0


def main():
    """
        main function.
        :return: exit code
    """

    """
    lispy> (defun factorial (lambda (n) (if (<= n 1) 1 (* n (factorial (- n 1))))))
    lispy> (factorial 5)
    120
    lispy> 
    """

    lexer = LispLexer.LispLexer()
    parser = LispParser.LispParser()
    interp = LispInterpreter()
    code = repl(lexer, parser, interp)
    return code


if __name__ == '__main__':
    exit(main())
