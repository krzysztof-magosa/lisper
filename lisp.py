import consts as c
import interpreter

class Qualifier:
    CONST = 1

class LispType(object):
    def __init__(self, value, qualifiers=[]):
        self._value = value
        self._qualifiers = qualifiers

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        if Qualifier.CONST in self.qualifiers:
            raise RuntimeError("Cannot modify const.")

        self._value = value

    @property
    def qualifiers(self):
        return self._qualifiers

    def __eq__(self, other):
        return self.value == other.value

    def __ne__(self, other):
        return not self.__eq__(other)

class Number(LispType):
    pass

class Integer(Number):
    pass

class Float(Number):
    pass

class String(LispType):
    pass

class Symbol(LispType):
    pass

#class Symbol(str):
#    """Represents LISP symbol."""
#    def __eq__(self, other):
#        if super(Symbol, self).__eq__(c.TRUE) and other == True:
#            return True
#
#        if super(Symbol, self).__eq__(c.NIL) and other == []:
#            return True
#
#        return super(Symbol, self).__eq__(other)
#
#    def __ne__(self, other):
#       return not self.__eq__(other)

class Procedure(object):
    """Represents LISP lambda."""
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
    """Converts object into LISP representation."""
    if is_symbol(x):
        return x
    elif is_string(x):
        return '"{}"'.format(x)
    elif is_integer(x) or is_float(x):
        return str(x)
    elif is_boolean(x):
        return c.TRUE if x else c.NIL
    elif is_list(x):
        return "({})".format(" ".join([to_lisp(i) for i in x]))
    elif is_lambda(x):
        return "({} ({}) {})".format(
            c.LAMBDA,
            " ".join([to_lisp(i) for i in x.parameters]),
            to_lisp(x.body)
        )
    else:
        raise RuntimeError("Unknown type")
        # HOW IT HAPPENS?!
#        return c.NIL

def typeof(x):
    """Returns type of LISP object."""
    if is_symbol(x):
        return c.T_SYMBOL
    elif is_boolean(x):
        return c.T_BOOLEAN if x else c.T_NIL
    elif is_string(x):
        return c.T_STRING
    elif is_integer(x):
        return c.T_INTEGER
    elif is_float(x):
        return c.T_FLOAT
    elif is_list(x):
        return c.T_LIST if len(x) > 0 else c.T_NIL
    elif is_lambda(x):
        return c.T_LAMBDA
    else:
        raise RuntimeError("Unknown type")

def is_symbol(x):
    return isinstance(x, Symbol)

def is_string(x):
    return isinstance(x, str) and not isinstance(x, Symbol)

def is_integer(x):
    # True/False are integers
    return isinstance(x, int) and not isinstance(x, bool)

def is_float(x):
    return isinstance(x, float)

def is_boolean(x):
    return (isinstance(x, bool) and x == True) or x == []

def is_list(x):
    return isinstance(x, list)

def is_nil(x):
    return x == []

def is_true(x):
    return not is_nil(x)

def is_lambda(x):
    return isinstance(x, Procedure)

#if __name__ == '__main__':
#    print(typeof(1))
