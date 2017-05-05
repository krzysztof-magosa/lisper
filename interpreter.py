from __future__ import print_function
import operator
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
            raise RuntimeError("Attempt to use not existing variable '{}'.".format(name))
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
        scope = Scope(parameters=self.parameters, arguments=arguments, outer=self.outer_scope)
        return self.interpreter.eval_lisp(self.body, scope)


def scope_init(scope):
    scope.define('+', operator.add)
    scope.define('-', operator.sub)
    scope.define('/', operator.div)
    scope.define('*', operator.mul)
    scope.define('%', operator.mod)

    scope.define('<', operator.lt)
    scope.define('<=', operator.le)
    scope.define('>', operator.gt)
    scope.define('>=', operator.ge)
    scope.define('=', operator.eq)

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
    T_LAMBDA = 'lambda'
    T_UNKNOWN = 'unknown'

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
        elif isinstance(value, str):
            return self.T_STRING
        elif isinstance(value, float):
            return self.T_FLOAT
        elif isinstance(value, int):
            return self.T_INTEGER
        elif isinstance(value, bool):
            return self.T_BOOLEAN
        elif isinstance(value, Procedure):
            return self.T_LAMBDA
        else:
            return self.T_UNKNOWN

    def assert_nargs(self, context, args, expected):
        got = len(args)
        if got != expected:
            raise RuntimeError(
                "{}: expected {} arguments, got {}.".format(
                    context,
                    expected,
                    got
                )
            )

    def assert_type(self, context, args, n, expected):
        got = self.typeof(args[n])
        if got != expected:
            raise RuntimeError(
                "{}: expected {} argument to be {}, got {}.".format(
                    context,
                    n,
                    expected,
                    got
                )
            )

    def builtin_typeof(self, scope, *args):
        self.assert_nargs("typeof", args, 1)
        return self.typeof(args[0])

#    def builtin_define(self, scope, *args):
#        self.assert_nargs("define", args, 2)

    def eval_lisp(self, item, scope):
        if isinstance(item, syntax.Symbol):
            return scope.get(item)
        elif not isinstance(item, list):
            return item
        elif hasattr(self, "builtin_{}".format(item[0])):
            arguments = [self.eval_lisp(arg, scope=scope) for arg in item[1:]]

            return getattr(self, "builtin_{}".format(item[0]))(
                scope,
                *arguments
            )
        elif item[0] == 'if':
            (_, test_clause, then_clause, else_clause) = item
            clause = then_clause if self.eval_lisp(test_clause, scope=scope) else else_clause
            return self.eval_lisp(clause, scope=scope)
        elif item[0] == 'lambda':
            (_, parameters, body) = item
            return Procedure(self, parameters, body, scope)
        elif item[0] == 'define':
            (_, name, value) = item
            scope.define(name, self.eval_lisp(value, scope=scope))
        elif item[0] == 'set!':
            (_, name, value) = item
            scope.set(name, self.eval_lisp(value, scope=scope))
        elif item[0] == 'quote':
            (_, expr) = item
            return expr
        elif item[0] == 'print':
            (_, text) = item
            print(self.eval_lisp(text, scope=scope))
        elif item[0] == 'prin1':
            (_, text) = item
            print(self.eval_lisp(text, scope=scope), end='')
        elif item[0] == 'format':
            arguments = [self.eval_lisp(arg, scope=scope) for arg in item[2:]]
            return sprintf(self.eval_lisp(item[1], scope=scope), *arguments)
        elif item[0] == 'while':
            (_, cond, body) = item
            while self.eval_lisp(cond, scope=scope):
                self.eval_lisp(body, scope=scope)
        else:
            procedure = self.eval_lisp(item[0], scope=scope)
            arguments = [self.eval_lisp(arg, scope=scope) for arg in item[1:]]
            return procedure(*arguments)
