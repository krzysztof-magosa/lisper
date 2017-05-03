import operator
import syntax


class Scope(object):
    def __init__(self, parameters=[], arguments=[], outer=None):
        self.data = dict()
        self.data.update(zip(parameters, arguments))
        self.outer = outer

    def find(self, name):
        # @TODO what to do when there is no outer scope?
        if name in self.data:
            return self
        else:
            return self.outer.find(name)

    def get(self, name):
        return self.find(name).data[name]

    def define(self, name, value):
        self.data[name] = value

    def set(self, name, value):
        self.find(name)[name] = value


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

    scope.define('begin', lambda *x: x[-1])


class Interpreter(object):
    def __init__(self, parser=syntax.parser, scope_init=scope_init):
        self.parser = parser
        self.scope = Scope()
        scope_init(self.scope)

    def interpret(self, code):
        lisp = self.parser.parse(code)
        return self.eval_lisp(lisp, scope=self.scope)

    def eval_lisp(self, item, scope):
        if isinstance(item, syntax.Symbol):
            return scope.get(item)
        elif not isinstance(item, list):
            return item
        elif item[0] == 'if':
            (_, test_clause, then_clause, else_clause) = item
            clause = then_clause if eval_expr(test_clause) else else_clause
            return self.eval_lisp(clause, scope=scope)
        elif item[0] == 'lambda':
            (_, parameters, body) = item
            return Procedure(self, parameters, body, scope)
        elif item[0] == 'define':
            (_, name, value) = item
            scope.define(name, self.eval_lisp(value, scope=scope))
        else:
            procedure = self.eval_lisp(item[0], scope=scope)
            arguments = [self.eval_lisp(arg, scope=scope) for arg in item[1:]]
            return procedure(*arguments)
