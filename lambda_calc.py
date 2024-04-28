import sys
from base import *

"""
Implements applicative order reduction.
"""
    
class Interpreter:
    """Applicative order"""
    def __init__(self):
        self.context = dict()
    def interpret(self, expression : Expression, context: dict):
        if(isinstance(expression, Variable)):
            return context[str(expression)]
        elif(isinstance(expression, Abstraction)):
            return expression
        elif(isinstance(expression, Application)):
            argument = self.interpret(expression.argument, context)
            newContext = dict(context)
            newContext[str(expression.function.param)] = argument
            return self.interpret(self.beta_replacement(expression.function.body, newContext), newContext)

    def beta_replacement(self, expression, context):
        if(isinstance(expression, Variable)):
            if(expression.name) in context:
                return context[expression.name]
            else:
                return expression
        elif(isinstance(expression, Abstraction)):
            return Abstraction(expression.param, self.beta_replacement(expression.body, context))
        elif(isinstance(expression, Application)):
            return Application(self.beta_replacement(expression.function, context), self.beta_replacement(expression.argument, context))


def main() -> int:
    # Testing
    test_expression = Application(Abstraction(Variable("x"), Abstraction(Variable("y"), Variable("x"))), (Abstraction(Variable("z"), Variable("z"))))
    interpreter = Interpreter()
    context = dict()
    reduced = interpreter.interpret(test_expression, context)
    print(reduced)
    return 0


if __name__ == '__main__':
    sys.exit(main())
