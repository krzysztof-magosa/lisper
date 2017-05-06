from __future__ import print_function
from __future__ import division
import sys
import syntax
from lisp import *


def sprintf(format, *values):
    return (format % values)


class Scope(object):
    def __init__(self, parameters=[], arguments=[], outer=None):
        self.data = dict()
        self.data.update(zip(parameters, arguments))
        self.outer = outer

    def find(self, name):
        if name in self.data:
            return self
        elif self.outer is None:
            raise RuntimeError(
                "Attempt to use not existing variable '{}'.".format(name)
            )
        else:
            return self.outer.find(name)

    def get(self, name):
        return self.find(name).data[name]

    def define(self, name, value):
        # Creates new variable.
        self.data[name] = value

    def set(self, name, value):
        # Changes existing variable or creates new variable.
        try:
            self.find(name).data[name] = value
        except:
            self.define(name, value)


class Macro(Procedure):
    pass


def scope_init(scope):
    scope.define('nil', [])
    scope.define('t', True)

    scope.define('abs', abs)

    scope.define('car', lambda x: x[0])
    scope.define('cdr', lambda x: x[1:])

    scope.define('begin', lambda *x: x[-1])

    scope.define('integer?', lambda x: is_integer(x))
    scope.define('float?', lambda x: is_float(x))
    scope.define('string?', lambda x: is_string(x))
    scope.define('symbol?', lambda x: is_symbol(x))
    scope.define('list?', lambda x: is_list(x))


class Interpreter(object):
    T_SYMBOL = 'symbol'
    T_STRING = 'string'
    T_FLOAT = 'float'
    T_INTEGER = 'integer'
    T_BOOLEAN = 'boolean'
    T_LIST = 'list'
    T_LAMBDA = 'lambda'
    T_UNKNOWN = 'unknown'

    BUILTINS = {
        'if': 'builtin_if',
        c.LAMBDA: 'builtin_lambda',
        '\\': 'builtin_lambda',
        'macro': 'builtin_macro',
        'quasiquote': 'builtin_quasiquote',
        'set': 'builtin_set',
        'set!': 'builtin_set_bang',
        'setq': 'builtin_setq',
        'setq!': 'builtin_setq_bang',
        'quote': 'builtin_quote',
        'print': 'builtin_print',
        'prin1': 'builtin_prin1',
        'while': 'builtin_while',
        'typeof': 'builtin_typeof',
        'format': 'builtin_format',
        'cons': 'builtin_cons',

        'head': 'builtin_head',
        'tail': 'builtin_tail',
        'len': 'builtin_len',

        '=': 'builtin_math_eq',
        '<': 'builtin_math_lt',
        '<=': 'builtin_math_le',
        '>': 'builtin_math_gt',
        '>=': 'builtin_math_ge',

        '+': 'builtin_math_add',
        '-': 'builtin_math_sub',
        '/': 'builtin_math_div',
        '*': 'builtin_math_mul',
        'mod': 'builtin_math_mod',
        'min': 'builtin_math_min',
        'max': 'builtin_math_max'
    }

    def __init__(self, parser=syntax.parser, scope_init=scope_init):
        self.parser = parser
        self.scope = Scope()
        scope_init(self.scope)

    def interpret(self, code):
        lisp = self.parser.parse(code)
#        print(lisp)
        return self.eval_lisp(lisp, scope=self.scope)

    def assert_nargs(self, context, args, expected):
        got = len(args)
        if got != expected:
            raise RuntimeError(
                "{}: expected {} argument(s), got {}.".format(
                    context,
                    expected,
                    got
                )
            )

    def assert_rargs(self, context, args, minimum, maximum):
        got = len(args)

        if got < minimum or got > maximum:
            raise RuntimeError(
                "{}: expected {}-{} arguments, got {}.".format(
                    context,
                    minimum,
                    maximum,
                    got
                )
            )

    def assert_type(self, context, args, n, expected):
        if not isinstance(expected, list):
            expected = [expected]

        got = typeof(args[n])
        if got not in expected:
            raise RuntimeError(
                "{}: expected {} argument to be {}, got {}.".format(
                    context,
                    n,
                    "/".join(expected),
                    got
                )
            )

    def assert_type_eval(self, context, value, n, expected):
        if not isinstance(expected, list):
            expected = [expected]

        got = typeof(value)
        if got not in expected:
            raise RuntimeError(
                "{}: expected {} argument to be evaluated into {}, got {}.".format(
                    context,
                    n,
                    "/".join(expected),
                    got
                )
            )

    def is_nil(self, x):
        if isinstance(x, syntax.Symbol) and x == "nil":
            return True
        elif x == []:
            return True

        return False

    def builtin_cons(self, scope, args):
        head = self.eval_lisp(args[0], scope)
        rest = self.eval_lisp(args[1], scope)

        if self.is_nil(head):
            head = []

        if self.is_nil(rest):
            rest = []

        if not isinstance(rest, list):
            rest = [rest]

        return [head] + rest

    def builtin_if(self, scope, args):
        self.assert_rargs("if", args, 2, 3)
        test_result = self.eval_lisp(args[0], scope)
        self.assert_type_eval("if", test_result, 0, c.T_BOOLEAN)

        if test_result:
            clause = args[1]
        elif len(args) == 3:
            clause = args[2]
        else:
            clause = []

        return self.eval_lisp(clause, scope)

    def builtin_typeof(self, scope, args):
        self.assert_nargs("typeof", args, 1)
        return typeof(args[0])

    def builtin_setq(self, scope, args):
        self.assert_nargs("setq", args, 2)
        self.assert_type("setq", args, 0, c.T_SYMBOL)
        scope.define(args[0], self.eval_lisp(args[1], scope))

    def builtin_setq_bang(self, scope, args):
        self.assert_nargs("setq!", args, 2)
        self.assert_type("setq!", args, 0, c.T_SYMBOL)
        scope.set(args[0], self.eval_lisp(args[1], scope=scope))

    def builtin_set(self, scope, args):
        self.assert_nargs("setq", args, 2)
        name = self.eval_lisp(args[0], scope)
        self.assert_type_eval("set", name, 0, c.T_SYMBOL)
        scope.define(name, self.eval_lisp(args[1], scope))

    def builtin_set_bang(self, scope, args):
        self.assert_nargs("set!", args, 2)
        name = self.eval_lisp(args[0], scope)
        self.assert_type_eval("set!", name, 0, c.T_SYMBOL)
        scope.set(name, self.eval_lisp(args[1], scope=scope))

    def builtin_format(self, scope, args):
        return sprintf(args[0], *args[1:])

    def builtin_quote(self, scope, args):
        return args[0]

    def builtin_lambda(self, scope, args):
        (parameters, body) = args
        return Procedure(self, parameters, body, scope)

    def builtin_macro(self, scope, args):
        (parameters, body) = args
        return Macro(self, parameters, self.eval_lisp(body, scope), scope)

    def is_pair(self, x):
        return x != [] and isinstance(x, list)

    def expand_quasiquote(self, x):
        if not self.is_pair(x):
            return ['quote', x]
        elif x[0] == 'unquote':
            return x[1]
        else:
            return [
                'cons',
                self.expand_quasiquote(x[0]),
                self.expand_quasiquote(x[1:])
            ]

    def builtin_quasiquote(self, scope, args):
        y = self.expand_quasiquote(args[0])
        y = self.eval_lisp(y, scope)
        return y

    def builtin_print(self, scope, args):
        self.assert_nargs("print", args, 1)
        obj = self.eval_lisp(args[0], scope=scope)
        print(to_lisp(obj))

    def builtin_prin1(self, scope, args):
        self.assert_nargs("prin1", args, 1)
        print(to_lisp(self.eval_lisp(args[0], scope=scope)), end='')

    def builtin_while(self, scope, args):
        (cond, body) = args
        while self.eval_lisp(cond, scope=scope):
            self.eval_lisp(body, scope=scope)

    def builtin_head(self, scope, args):
        self.assert_nargs("head", args, 1)
        args = self.eval_all(args, scope)
        self.assert_type_eval("head", args[0], 0, c.T_LIST)

        return args[0][0]

    def builtin_tail(self, scope, args):
        self.assert_nargs("tail", args, 1)
        args = self.eval_all(args, scope)
        self.assert_type_eval("tail", args[0], 0, c.T_LIST)

        return args[0][-1]

    def builtin_len(self, scope, args):
        self.assert_nargs("len", args, 1)
        args = self.eval_all(args, scope)
        self.assert_type_eval("len", args[0], 0, c.T_LIST)

        return len(args[0])

    def builtin_math_eq(self, scope, args):
        self.assert_rargs("=", args, 1, sys.maxint)
        args = self.eval_all(args, scope)
        for i in range(len(args)):
            self.assert_type_eval("=", args[i], i, [c.T_INTEGER, c.T_FLOAT])

        for x in args[1:]:
            if not args[0] == x:
                return False

        return True

    def builtin_math_lt(self, scope, args):
        self.assert_rargs("<", args, 1, sys.maxint)
        args = self.eval_all(args, scope)
        for i in range(len(args)):
            self.assert_type_eval("<", args[i], i, [c.T_INTEGER, c.T_FLOAT])

        for x in args[1:]:
            if not args[0] < x:
                return False

        return True

    def builtin_math_le(self, scope, args):
        self.assert_rargs("<=", args, 1, sys.maxint)
        args = self.eval_all(args, scope)
        for i in range(len(args)):
            self.assert_type_eval("<=", args[i], i, [c.T_INTEGER, c.T_FLOAT])

        for x in args[1:]:
            if not args[0] <= x:
                return False

        return True

    def builtin_math_gt(self, scope, args):
        self.assert_rargs(">", args, 1, sys.maxint)
        args = self.eval_all(args, scope)
        for i in range(len(args)):
            self.assert_type_eval(">", args[i], i, [c.T_INTEGER, c.T_FLOAT])


        for x in args[1:]:
            if not args[0] > x:
                return False

        return True

    def builtin_math_ge(self, scope, args):
        self.assert_rargs(">=", args, 1, sys.maxint)
        args = self.eval_all(args, scope)
        for i in range(len(args)):
            self.assert_type_eval(">=", args[i], i, [c.T_INTEGER, c.T_FLOAT])

        for x in args[1:]:
            if not args[0] >= x:
                return False

        return True

    def builtin_math_add(self, scope, args):
        self.assert_rargs("+", args, 1, sys.maxint)
        args = self.eval_all(args, scope)
        for i in range(len(args)):
            self.assert_type_eval("+", args[i], i, [c.T_INTEGER, c.T_FLOAT])

        result = args[0]
        for x in args[1:]:
            result += x

        return result


    def builtin_math_sub(self, scope, args):
        self.assert_rargs("-", args, 1, sys.maxint)
        args = self.eval_all(args, scope)
        for i in range(len(args)):
            self.assert_type_eval("-", args[i], i, [c.T_INTEGER, c.T_FLOAT])

        result = args[0]
        for x in args[1:]:
            result -= x

        return result

    def builtin_math_div(self, scope, args):
        self.assert_rargs("/", args, 1, sys.maxint)
        args = self.eval_all(args, scope)
        for i in range(len(args)):
            self.assert_type_eval("/", args[i], i, [c.T_INTEGER, c.T_FLOAT])

        result = args[0]
        for x in args[1:]:
            result /= x

        return result

    def builtin_math_mul(self, scope, args):
        self.assert_rargs("*", args, 1, sys.maxint)
        args = self.eval_all(args, scope)
        for i in range(len(args)):
            self.assert_type_eval("*", args[i], i, [c.T_INTEGER, c.T_FLOAT])

        result = args[0]
        for x in args[1:]:
            result *= x

        return result

    def builtin_math_mod(self, scope, args):
        self.assert_nargs("mod", args, 2)
        args = self.eval_all(args, scope)
        for i in range(len(args)):
            self.assert_type_eval("mod", args[i], i, [c.T_INTEGER, c.T_FLOAT])

        return args[0] % args[1]

    def builtin_math_min(self, scope, args):
        self.assert_rargs("min", args, 1, sys.maxint)
        args = self.eval_all(args, scope)
        for i in range(len(args)):
            self.assert_type_eval("min", args[i], i, [c.T_INTEGER, c.T_FLOAT])

        return min(args)

    def builtin_math_max(self, scope, args):
        self.assert_rargs("max", args, 1, sys.maxint)
        args = self.eval_all(args, scope)
        for i in range(len(args)):
            self.assert_type_eval("max", args[i], i, [c.T_INTEGER, c.T_FLOAT])

        return max(args)


    def eval_all(self, args, scope):
        return [self.eval_lisp(x, scope) for x in args]

    def eval_lisp(self, item, scope):
        if isinstance(item, syntax.Symbol):
            return scope.get(item)
        elif not isinstance(item, list) or len(item) == 0:
            return item
        elif item[0] in self.BUILTINS:
            func = getattr(self, self.BUILTINS[item[0]])
            return func(scope, item[1:])
        else:
            procedure = self.eval_lisp(item[0], scope=scope)
            arguments = [self.eval_lisp(arg, scope=scope) for arg in item[1:]]

            if isinstance(procedure, Macro):
                print("MAKRO")
#                procedure.outer_scope = scope
                return self.eval_lisp(procedure(*arguments), scope)
            else:
                return procedure(*arguments)
