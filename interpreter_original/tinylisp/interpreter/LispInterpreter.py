#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Provide conversion system from string to token list.
"""

from tinylisp.interpreter import Procedure, Enviroment, Error
from tinylisp.parser import TreeListParser, ListParser
from tinylisp.parser.ListParser import Node


class LispInterpreter:
    """
        Provide conversion system from string to token list.
    """
    def __init__(self):
        self.global_env = LispInterpreter._add_globals(Enviroment.Env())

    @staticmethod
    def _add_globals(env):
        """
            環境にScheme標準の手続きをいくつか追加する
        """

        import cmath
        import operator as op

        env.update(vars(cmath))  # sin, sqrt, ...
        env.update(
            {
                '+': op.add, '-': op.sub, '*': op.mul, '/': op.truediv, 'not': op.not_,
                '>': op.gt, '<': op.lt, '>=': op.ge, '<=': op.le, '=': op.eq, '^': op.pow,
                'equal': op.eq, 'eq': op.is_, 'length': len, 'cons': lambda x, y: LispInterpreter._cons(x, y),
                'car': lambda x: x[0], 'cdr': lambda x: x[1:], 'append': LispInterpreter._append,
                'list': lambda *x: list(x), 'list?': lambda x: isinstance(x, list), 'last': lambda x: [x[-1]],
                'reverse': LispInterpreter._reverse,
                'null?': lambda x: x is None or x == [], 'symbol?': lambda x: isinstance(x, str),
                'atom': LispInterpreter._is_atom, 'integerp': lambda x: isinstance(x, int),
                'print': lambda x: print(LispInterpreter.to_string(x)), 'princ': lambda x: print(x, end='')
            })
        return env

    @staticmethod
    def _cons(x, y):
        a_list = [x]
        if y is not None:
            a_list = [x] + y
        return a_list

    @staticmethod
    def _append(x, y):
        if not isinstance(x, list):
            return Error.Error('unexpected argument {0} for append'.format(x))
        for elem in y:
            x.append(elem)
        return x

    @staticmethod
    def _reverse(x):
        if isinstance(x, list):
            x.reverse()
        return x

    @staticmethod
    def _is_atom(val):
        if isinstance(val, (float, int, str)):
            return True
        return False

    @staticmethod
    def to_string(exp):
        """
            PythonオブジェクトをLispの読める文字列に戻す。
        """
        isa = isinstance
        return '(' + ' '.join(map(LispInterpreter.to_string, exp)) + ')' if isa(exp, list) else str(exp)

    def eval(self, x, env=None):
        """
            環境の中で式を評価する。
        """
        if env is None:
            env = self.global_env

        while True:
            if x is None or (isinstance(x, Node) and len(x) <= 0):
                return None

            if isinstance(x, Node):
                x_car = x.car
            if isinstance(x, str) and x[0] == '"':  # Wquote
                return x[1:-1]
            elif isinstance(x, str):  # 変数参照
                val = env.find(x)
                if not isinstance(val, Error.Error):
                    val = val[x]
                return val
            elif self._is_atom(x):  # 定数リテラル
                return x
            elif x_car == 'quote':  # (quote exp)
                (_, exp) = x
                return exp
            elif x_car == 'if':  # (if test conseq alt)
                (_, test, conseq, alt) = x
                return self.eval((conseq if self.eval(test, env) else alt), env)
            elif x_car == 'cond':
                exps = x[1:]
                for exp in exps:
                    if exp[0] == 't':
                        return self.eval(exp[1], env)
                    elif self.eval(exp[0], env):
                        return self.eval(exp[1], env)
            elif x_car == 'progn':
                exps = x[1:]
                for exp in exps:
                    self.eval(exp, env)
                return None
            elif x_car == 'set!':  # (set! var exp)
                (_, var, exp) = x
                env.find(var)[var] = self.eval(exp, env)
                return None
            elif x_car == 'defun':  # (define var exp)
                (_, var, exp) = x
                env[var] = self.eval(exp, env)
                return None
            elif x_car == 'lambda':  # (lambda (var*) exp)
                (_, vars, exp) = x
                return Procedure.Procedure(vars, exp, env)
                # lambda *args: self.eval(exp, Env(vars, args, env))
            elif x_car == 'begin':  # (begin exp*)
                for exp in x[1:]:
                    val = self.eval(exp, env)
                    return val
            elif x_car == 'trace':
                for key, value in env.items():
                    print('{0} : {1}'.format(key, value))
                return None
            elif x_car == 'exit':
                return 'exit'
            else:  # (proc exp*)
                exps = []
                exps.append(self.eval(x_car, env))
                x_cdr = x.cdr
                while x_cdr is not None:
                    if isinstance(x_cdr, Node):
                        exps.append(self.eval(x_cdr, env))
                        x_cdr = x_cdr.cdr

                #exps = [self.eval(exp, env) for exp in x]
                proc = exps.pop(0)
                try:
                    if isinstance(proc, Procedure.Procedure):
                        x = proc.exp
                        env = Enviroment.Env(proc.parms, exps, proc.env)
                    else:
                        if proc is None:
                            return None
                        elif not LispInterpreter._is_atom(proc):
                            val = proc(*exps)
                            return val
                        else:
                            if isinstance(x_car, str):
                                return proc
                            return x
                except TypeError as type_error:
                    return Error.Error(type_error.args[0])


def _pinput(prompt=''):
    """

        :param prompt:
        :return:
    """
    mbc = 0
    text = ''
    rprompt = prompt
    while True:
        _text = input(rprompt)
        if _text == '!':
            rprompt = prompt
            mbc = 0
            text = ''
            continue

        mbc += _text.count('(')
        mbc -= _text.count(')')
        text += _text + ' '
        rprompt = '>>> '
        if mbc <= 0:
            break
    return text


def repl_with_asm(messenger, trace=False, prompt='tinylisp> '):
    """
        Prompt of tiny lisp interpreter.
        :param messenger:
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
    tree_list_parser = TreeListParser.TreeListParser
    list_parser = ListParser.ListParser
    interp = LispInterpreter()
    #
    # a_list = list_parser.parse(out)
    # for elem in a_list:
    #     val = interp.eval(elem)
    #     if val is not None:
    #         print(val)

    is_exit = False
    while not is_exit:
        text = _pinput(prompt)
        suc, out = messenger.send(text)
        if suc:
            a_list = tree_list_parser.parse(out)
            a_list = list_parser.parse(a_list)
            for elem in a_list:
                if trace:
                    print('trace: ', elem)
                val = interp.eval(elem)
                if val == 'exit':
                    is_exit = True
                    break
                elif isinstance(val, Error.Error):
                    print(val.err_msg)
                elif val is not None:
                    print(LispInterpreter.to_string(val))
                elif val is None:
                    print('nil')
                else:
                    continue
        else:
            print(out)
    return 0


def repl_with_list_from_file(filename, messenger, trace=False, prompt='tinylisp> '):
    """
        Prompt of tiny lisp interpreter from file.
        :param filename:
        :param messenger:
        :param trace:
        :param prompt:
        :return: exit code
    """
    with open(filename, "rU", encoding="utf_8") as a_file:
        interp = LispInterpreter()
        list_parser = TreeListParser.TreeListParser
        text = ''
        for line in a_file:
            if line != '':
                text += line

        suc, out = messenger.send(text)
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
                print(LispInterpreter.to_string(val))
            elif val is None:
                print('nil')

    return 0
