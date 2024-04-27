from type_check import check_with_context
from lambda_calc import Interpreter

def evaluate(expression, type):
    if check_with_context(expression, type):
        interpreter = Interpreter()
        context = dict()
        reduced = interpreter.interpret(interpreter, context)
        return reduced
    else:
        raise Exception("Expression is not well-typed")
    

    