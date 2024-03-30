from base import Type, Expression, Unit, Variable, Abstraction, Application

def partition_context(context):
    lst = [(k, v) for k, v in context.items()]
    n = len(lst)

    contexts = []
    for i in range(2**n):
        context1, context2 = {}, {}
        for index in range(n):
            if i & (1 << index):
                context1[lst[index][0]] = lst[index][2]
            else:
                context2[lst[index][0]] = lst[index][2]
        contexts.append((context1, context2))


def check_with_context(expression, type, context):
    if isinstance(expression, Unit):
        return type.is_unit and not context
    elif isinstance(expression, Variable):
        return expression in context and context[expression] == type and len(context.keys()) == 1
    elif isinstance(expression, Abstraction):
        context[expression.param] = type.t1
        return check_with_context(expression.body, type.t2, context)
    elif isinstance(expression, Application):
        partitions = partition_context(context)
        for context1, context2 in partitions:
            if check_with_context(expression.function, type.t1, context1) and check_with_context(expression.argument, type.t2, context2):
                return True
        return False

def check(expression, type):
    return check_with_context(expression, type, {})

# Testing
e1, t1 = Unit(), Type(True) # passes
e2, t2 = Abstraction(Variable("x"), Unit()), Type(False, Type(True), Type(True)) # fails because we do not use the fact that x is of the Unit Type (as desired)
e3, t3 = Abstraction(Variable("x"), Variable("x")), Type(False, Type(True), Type(True)) # passes as we use x 
print(check(e1, t1))
print(check(e2, t2))
print(check(e3, t3))