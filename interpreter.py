from __future__ import print_function
from __future__ import division
import sys
import syntax


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
        self.data[name] = value

    def set(self, name, value):
        self.find(name).data[name] = value


class Procedure(object):
    def __init__(self, interpreter, parameters, body, outer_scope):
        self.interpreter = interpreter
        self.parameters = parameters
        self.body = body
        self.outer_scope = outer_scope

    def __call__(self, *arguments):
        scope = Scope(
            parameters=self.parameters,
            arguments=arguments,
            outer=self.outer_scope
        )
        return self.interpreter.eval_lisp(self.body, scope)


def scope_init(scope):
    scope.define('nil', [])
    scope.define('t', True)

    scope.define('abs', abs)

    scope.define('car', lambda x: x[0])
    scope.define('cdr', lambda x: x[1:])

    scope.define('begin', lambda *x: x[-1])

    scope.define('integer?', lambda x: isinstance(x, int))
    scope.define('float?', lambda x: isinstance(x, float))
    scope.define('string?', lambda x: isinstance(x, str) and not isinstance(x, syntax.Symbol))
    scope.define('symbol?', lambda x: isinstance(x, syntax.Symbol))
    scope.define('list?', lambda x: isinstance(x, list))


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
        'lambda': 'builtin_lambda',
        '\\': 'builtin_lambda',
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

    def typeof(self, value):
        if isinstance(value, syntax.Symbol):
            return self.T_SYMBOL
        elif isinstance(value, bool):
            return self.T_BOOLEAN
        elif isinstance(value, str):
            return self.T_STRING
        elif isinstance(value, float):
            return self.T_FLOAT
        elif isinstance(value, int):
            return self.T_INTEGER
        elif isinstance(value, list):
            return self.T_LIST
        elif isinstance(value, Procedure):
            return self.T_LAMBDA
        else:
            return self.T_UNKNOWN

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

        got = self.typeof(args[n])
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

        got = self.typeof(value)
        if got not in expected:
            raise RuntimeError(
                "{}: expected {} argument to be evaluated into {}, got {}.".format(
                    context,
                    n,
                    "/".join(expected),
                    got
                )
            )

    def builtin_if(self, scope, args):
        self.assert_rargs("if", args, 2, 3)
        test_result = self.eval_lisp(args[0], scope)
        self.assert_type_eval("if", test_result, 0, self.T_BOOLEAN)

        if test_result:
            clause = args[1]
        elif len(args) == 3:
            clause = args[2]
        else:
            clause = []

        return self.eval_lisp(clause, scope)

    def builtin_typeof(self, scope, args):
        self.assert_nargs("typeof", args, 1)
        return self.typeof(args[0])

    def builtin_setq(self, scope, args):
        self.assert_nargs("setq", args, 2)
        self.assert_type("setq", args, 0, self.T_SYMBOL)
        scope.define(args[0], self.eval_lisp(args[1], scope))

    def builtin_setq_bang(self, scope, args):
        self.assert_nargs("setq!", args, 2)
        self.assert_type("setq!", args, 0, self.T_SYMBOL)
        scope.set(args[0], self.eval_lisp(args[1], scope=scope))

    def builtin_set(self, scope, args):
        self.assert_nargs("setq", args, 2)
        name = self.eval_lisp(args[0], scope)
        self.assert_type_eval("set", name, 0, self.T_SYMBOL)
        scope.define(name, self.eval_lisp(args[1], scope))

    def builtin_set_bang(self, scope, args):
        self.assert_nargs("set!", args, 2)
        name = self.eval_lisp(args[0], scope)
        self.assert_type_eval("set!", name, 0, self.T_SYMBOL)
        scope.set(name, self.eval_lisp(args[1], scope=scope))

    def builtin_format(self, scope, args):
        return sprintf(args[0], *args[1:])

    def builtin_quote(self, scope, args):
        return args[0]

    def builtin_lambda(self, scope, args):
        (parameters, body) = args
        return Procedure(self, parameters, body, scope)

    def builtin_print(self, scope, args):
        self.assert_nargs("print", args, 1)
        print(self.eval_lisp(args[0], scope=scope))

    def builtin_prin1(self, scope, args):
        self.assert_nargs("prin1", args, 1)
        print(self.eval_lisp(args[0], scope=scope), end='')

    def builtin_while(self, scope, args):
        (cond, body) = args
        while self.eval_lisp(cond, scope=scope):
            self.eval_lisp(body, scope=scope)

    def builtin_head(self, scope, args):
        self.assert_nargs("head", args, 1)
        args = self.eval_all(args, scope)
        self.assert_type_eval("head", args[0], 0, self.T_LIST)

        return args[0][0]

    def builtin_tail(self, scope, args):
        self.assert_nargs("tail", args, 1)
        args = self.eval_all(args, scope)
        self.assert_type_eval("tail", args[0], 0, self.T_LIST)

        return args[0][-1]

    def builtin_len(self, scope, args):
        self.assert_nargs("len", args, 1)
        args = self.eval_all(args, scope)
        self.assert_type_eval("len", args[0], 0, self.T_LIST)

        return len(args[0])

    def builtin_math_eq(self, scope, args):
        self.assert_rargs("=", args, 1, sys.maxint)
        args = self.eval_all(args, scope)
        for i in range(len(args)):
            self.assert_type_eval("=", args[i], i, [self.T_INTEGER, self.T_FLOAT])

        for x in args[1:]:
            if not args[0] == x:
                return False

        return True

    def builtin_math_lt(self, scope, args):
        self.assert_rargs("<", args, 1, sys.maxint)
        args = self.eval_all(args, scope)
        for i in range(len(args)):
            self.assert_type_eval("<", args[i], i, [self.T_INTEGER, self.T_FLOAT])

        for x in args[1:]:
            if not args[0] < x:
                return False

        return True

    def builtin_math_le(self, scope, args):
        self.assert_rargs("<=", args, 1, sys.maxint)
        args = self.eval_all(args, scope)
        for i in range(len(args)):
            self.assert_type_eval("<=", args[i], i, [self.T_INTEGER, self.T_FLOAT])

        for x in args[1:]:
            if not args[0] <= x:
                return False

        return True

    def builtin_math_gt(self, scope, args):
        self.assert_rargs(">", args, 1, sys.maxint)
        args = self.eval_all(args, scope)
        for i in range(len(args)):
            self.assert_type_eval(">", args[i], i, [self.T_INTEGER, self.T_FLOAT])


        for x in args[1:]:
            if not args[0] > x:
                return False

        return True

    def builtin_math_ge(self, scope, args):
        self.assert_rargs(">=", args, 1, sys.maxint)
        args = self.eval_all(args, scope)
        for i in range(len(args)):
            self.assert_type_eval(">=", args[i], i, [self.T_INTEGER, self.T_FLOAT])

        for x in args[1:]:
            if not args[0] >= x:
                return False

        return True

    def builtin_math_add(self, scope, args):
        self.assert_rargs("+", args, 1, sys.maxint)
        args = self.eval_all(args, scope)
        for i in range(len(args)):
            self.assert_type_eval("+", args[i], i, [self.T_INTEGER, self.T_FLOAT])

        result = args[0]
        for x in args[1:]:
            result += x

        return result


    def builtin_math_sub(self, scope, args):
        self.assert_rargs("-", args, 1, sys.maxint)
        args = self.eval_all(args, scope)
        for i in range(len(args)):
            self.assert_type_eval("-", args[i], i, [self.T_INTEGER, self.T_FLOAT])

        result = args[0]
        for x in args[1:]:
            result -= x

        return result

    def builtin_math_div(self, scope, args):
        self.assert_rargs("/", args, 1, sys.maxint)
        args = self.eval_all(args, scope)
        for i in range(len(args)):
            self.assert_type_eval("/", args[i], i, [self.T_INTEGER, self.T_FLOAT])

        result = args[0]
        for x in args[1:]:
            result /= x

        return result

    def builtin_math_mul(self, scope, args):
        self.assert_rargs("*", args, 1, sys.maxint)
        args = self.eval_all(args, scope)
        for i in range(len(args)):
            self.assert_type_eval("*", args[i], i, [self.T_INTEGER, self.T_FLOAT])

        result = args[0]
        for x in args[1:]:
            result *= x

        return result

    def builtin_math_mod(self, scope, args):
        self.assert_nargs("mod", args, 2)
        args = self.eval_all(args, scope)
        for i in range(len(args)):
            self.assert_type_eval("mod", args[i], i, [self.T_INTEGER, self.T_FLOAT])

        return args[0] % args[1]

    def builtin_math_min(self, scope, args):
        self.assert_rargs("min", args, 1, sys.maxint)
        args = self.eval_all(args, scope)
        for i in range(len(args)):
            self.assert_type_eval("min", args[i], i, [self.T_INTEGER, self.T_FLOAT])

        return min(args)

    def builtin_math_max(self, scope, args):
        self.assert_rargs("max", args, 1, sys.maxint)
        args = self.eval_all(args, scope)
        for i in range(len(args)):
            self.assert_type_eval("max", args[i], i, [self.T_INTEGER, self.T_FLOAT])

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
            return procedure(*arguments)
