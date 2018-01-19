#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Provide conversion system from string to token list.
"""

from tinylisp.interpreter import Common
from tinylisp.parser import LispLexer, LispParser, ListParser


class LispInterpreter:
    """
        Provide conversion system from string to token list.
    """
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
                if isinstance(x[0], Common.Symbol):
                    return proc
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


def repl(trace=False, prompt='lispy> '):
    """
        Prompt of native lisp interpreter.
    """
    lexerp = LispLexer.LispLexer()
    parserp = LispParser.LispParser()
    interp = LispInterpreter()

    while True:
        list = parserp.parse(lexerp.make_token(input(prompt)))
        if trace:
            print(list)
        val = interp.eval(list)
        if val == 'exit':
            break
        elif val is not None:
            print(to_string(val))
        else:
            continue
    return 0


def repl_with_asm(translator, trace=False, prompt='listpy> '):
    """
        Prompt of tiny lisp interpreter.
        :param translator:
        :param trace:
        :param prompt:
        :return: exit code
    """
    # out = translator.send("""
    #         (defun test
    #             (lambda
    #                 (r) (+ 1 r)
    #             )
    #         )
    #         (test 1)
    #         """)
    list_parser = ListParser.ListParser()
    interp = LispInterpreter()
    #
    # a_list = list_parser.parse(out)
    # for elem in a_list:
    #     val = interp.eval(elem)
    #     if val is not None:
    #         print(val)

    is_exit = False
    while not is_exit:
        text = input(prompt)
        suc, out = translator.send(text)
        if suc:
            a_list = list_parser.parse(out)
            for elem in a_list:
                if trace:
                    print('trace: ', elem)
                val = interp.eval(elem)
                if val == 'exit':
                    is_exit = True
                    break
                elif val is not None:
                    print(to_string(val))
                else:
                    continue
        else:
            print(out)
    return 0


def repl_with_list_from_file(filename, translator, trace=False, prompt='listpy> '):
    """
        Prompt of tiny lisp interpreter from file.
        :param filename:
        :param trace:
        :param prompt:
        :return: exit code
    """
    with open(filename, "rU", encoding="utf_8_sig") as a_file:
        interp = LispInterpreter()
        list_parser = ListParser.ListParser()
        text = ''
        for line in a_file:
            if line != '':
                text += line

        suc, out = translator.send(text)
        if not suc:
            print(out)
            return 1

        a_list = list_parser.parse(out)
        for elem in a_list:
            if trace:
                print(prompt, end='')
                print(elem)
            val = interp.eval(elem)
            if val is not None:
                print(to_string(val))

    return 0
