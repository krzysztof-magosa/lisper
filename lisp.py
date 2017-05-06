import consts as c
import interpreter

# Python does not have type like that
class Symbol(str):
    pass

#
class Procedure(object):
    def __init__(self, interpreter, parameters, body, outer_scope):
        self.interpreter = interpreter
        self.parameters = parameters
        self.body = body
        self.outer_scope = outer_scope

    def __call__(self, *arguments):
        scope = interpreter.Scope(
            parameters=self.parameters,
            arguments=arguments,
            outer=self.outer_scope
        )
        return self.interpreter.eval_lisp(self.body, scope)


def to_lisp(x):
    if is_symbol(x):
        return x
    elif is_string(x):
        return '"{}"'.format(x)
    elif is_integer(x) or is_float(x):
        return str(x)
    elif is_list(x):
        return "({})".format(" ".join([to_lisp(i) for i in x]))
    elif is_boolean(x):
        return c.TRUE if x else c.NIL
    elif is_lambda(x):
        return "({} ({}) {})".format(
            c.LAMBDA,
            " ".join([to_lisp(i) for i in x.parameters]),
            to_lisp(x.body)
        )

def typeof(x):
    if is_symbol(x):
        return c.T_SYMBOL
    elif is_string(x):
        return c.T_STRING
    elif is_integer(x):
        return c.T_INTEGER
    elif is_float(x):
        return c.T_FLOAT
    elif is_list(x):
        return c.T_LIST if len(x) > 0 else c.T_NIL
    elif is_boolean(x):
        return c.T_BOOLEAN if x else c.T_NIL
    elif is_lambda(x):
        return c.T_LAMBDA

def is_symbol(x):
    return isinstance(x, Symbol)

def is_string(x):
    return isinstance(x, str) and not isinstance(x, Symbol)

def is_integer(x):
    return isinstance(x, int)

def is_float(x):
    return isinstance(x, float)

def is_boolean(x):
    return x == True or x == []

def is_list(x):
    return isinstance(x, list)

def is_nil(x):
    return x == []

def is_true(x):
    return not is_nil(x)

def is_lambda(x):
    return isinstance(x, Procedure)
