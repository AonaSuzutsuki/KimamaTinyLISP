#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

"""

from tinylisp.interpreter import LispInterpreter

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
    import sys, subprocess
    args = sys.argv
    if len(args) > 1:
        filename = args[1]
        LispInterpreter.repl_with_list_from_file(filename)
    else:
        out = subprocess.check_output(['D:/Develop/Git/TinyLISP/bin/formatter.exe'], shell=True)
        print(out)
        code = LispInterpreter.repl()
        return code


if __name__ == '__main__':
    exit(main())
