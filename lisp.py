import consts as c

# Python does not have type like that
class Symbol(str):
    pass


def to_lisp(x):
    if is_symbol(x):
        return x
    elif is_string(x):
        return '"{}"'.format(x)
    elif is_integer(x) or is_float(x):
        return str(x)
    elif list(x):
        return "({})".format(" ".join([to_lisp(i) for i in x]))
    elif is_boolean(x):
        return c.TRUE if x else c.NIL

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
