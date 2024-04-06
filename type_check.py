from base import Type, UnitType, Expression, Product, Unit, Variable, Abstraction, Application, Sum, SumChoice, SumType, ConjunctiveProduct, ConjunctiveSum, And
from copy import deepcopy
"""
Todo: eventually change from partitioning contexts in brute force????
Can provide full contexts to both expressions, and get back their context on return to have what was unused, and check for matches there?
Is this possible/in line with linear logic?
"""
def partition_context(context):
    lst = [(k, v) for k, v in context.items()]
    n = len(lst)

    contexts = []
    for i in range(2**n):
        context1, context2 = {}, {}
        for index in range(n):
            if i & (1 << index):
                context1[lst[index][0]] = lst[index][1]
            else:
                context2[lst[index][0]] = lst[index][1]
        contexts.append((context1, context2))
    
    return contexts


def check_with_context(expression, type, context={}):
    if isinstance(expression, Unit):
        return isinstance(type, UnitType) and not context
    elif isinstance(expression, Variable):
        return expression in context and context[expression] == type and len(context.keys()) == 1
    elif isinstance(expression, Abstraction):
        context[expression.param] = type.t1
        return check_with_context(expression.body, type.t2, context)
    elif isinstance(expression, Application):
        if not context:
            return check_with_context(expression.function, type.t1, context) and check_with_context(expression.argument, type.t2, context)
        partitions = partition_context(context)
        for context1, context2 in partitions:
            if check_with_context(expression.function, type.t1, context1) and check_with_context(expression.argument, type.t2, context2):
                return True
        return False
    elif isinstance(expression, Product):
        if not isinstance(type, ConjunctiveProduct):
            return False
        elif not context:
            return check_with_context(expression.e1, type.t1, context) and check_with_context(expression.e2, type.t2, context)
        partitions = partition_context(context)
        for context1, context2 in partitions:
            if check_with_context(expression.e1, type.t1, context1) and check_with_context(expression.e2, type.t2, context2):
                return True
        return False
    elif isinstance(expression, Sum):
        if not isinstance(type, SumType):
            return False
        if(expression.choice == SumChoice.INL):
            return check_with_context(expression.expr, type.t1, context)
        else:
            return check_with_context(expression.expr, type.t2, context)
    elif isinstance(expression, And):
        if not isinstance(type, ConjunctiveSum):
            return False
        context_copy = deepcopy(context)
        return check_with_context(expression.e1, type.t1, context) and check_with_context(expression.e1, type.t1, context_copy)


# Testing
e1, t1 = Unit(), UnitType() # passes
e2, t2 = Abstraction(Variable("x"), Unit()), Type(t1=UnitType(), t2=UnitType()) # fails because we do not use the fact that x is of the Unit Type (as desired)
e3, t3 = Abstraction(Variable("x"), Variable("x")), Type(t1=UnitType(), t2=UnitType()) # passes as we use x
e4, t4 = Abstraction(Variable("x"), Product(Variable("x"), Variable("x"))), Type(UnitType(), ConjunctiveProduct(UnitType(), UnitType())) # fails as we use x twice
e5, t5 = Abstraction(Variable("x"), And(Variable("x"), Variable("x"))), Type(UnitType(), ConjunctiveSum(UnitType(), UnitType()))
print(check_with_context(e1, t1))
print(check_with_context(e2, t2))
print(check_with_context(e3, t3))
print(check_with_context(e4, t4))
print(check_with_context(e5, t5))