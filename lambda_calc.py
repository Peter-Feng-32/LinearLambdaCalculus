import sys
from base import Expression, Normal, Unit, Variable, Abstraction, Application

"""
This is an implementation of linear lambda calculus.

Roadmap:
1) Implement untyped lambda calculus
2) Add parser and interpreter
3) Extend to typed lambda calculus
4) Extend to linear (typed) lambda calculus.


First we do basic untyped lambda calculus. This file will handle the steps-to semantics assuming the linear type checker has already passed.
Enforcement of linear typing is handled in type_check.py

Lambda calculus:
1) Variable
2) Lambda Abstraction
3) Application

How to handle applications?
Implement a context to map variables to their interpretations.  

Normal - Expression is in normal form if it can no longer be reduced by beta or eta reductions.

Beta(β) reduction - Replacing bound variables in function body with arguments
Eta(η) reduction - Get rid of dummy function
Alpha(o) substitution - variable renaming

Starting out with implementing applicative order reduction.

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
        
    """
    TODO: handle variable name collisions so that beta replacement doesn't replace variables which are bound in the inner expression.
    Right now  λx.(λx.x) (λz.z) gets turned into λx.(λz.z)
    
    """

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
    name_collision_expression = Application(Abstraction(Variable("x"), Abstraction(Variable("x"), Variable("x"))), Abstraction(Variable("z"), Variable("z")))
    interpreter = Interpreter()
    context = dict()
    reduced = interpreter.interpret(name_collision_expression, context)
    print(reduced)
    return 0


if __name__ == '__main__':
    sys.exit(main())
