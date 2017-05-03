#!/usr/bin/env python

from interpreter import Interpreter

interpreter = Interpreter()

print("KM Lisp v0.1")
while True:
    code = raw_input('hlisp> ')
    value = interpreter.interpret(code)
    if value is not None:
        print(value)
