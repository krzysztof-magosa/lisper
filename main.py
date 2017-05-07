#!/usr/bin/env python

from interpreter import Interpreter
import sys
from lisp import *

interpreter = Interpreter()


def run_code(code):
    try:
        value = interpreter.interpret(code)
        if value is not None:
            print(to_lisp(value))
    except RuntimeError as e:
        print(e.message)


with open('stdlib.lisper', 'r') as handle:
        code = handle.read()
        run_code(code)

if len(sys.argv) == 2:
    with open(sys.argv[1], 'r') as handle:
        code = handle.read()
        run_code(code)
else:
    while True:
        code = raw_input('LISPer> ')
        run_code(code)
