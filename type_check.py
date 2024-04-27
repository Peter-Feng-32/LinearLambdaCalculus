from base import *
from copy import deepcopy

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

def allow_check(expression, type, context={}):
    if isinstance(expression, Unit):
        return isinstance(type, UnitType)
    elif isinstance(expression, Variable):
        if not (expression in context and context[expression] == type):
            return False
        context.pop(expression)
        return True
    
    elif isinstance(expression, Abstraction):
        context[expression.param] = type.t1
        return allow_check(expression.body, type.t2, context)
    elif isinstance(expression, Application):
        if not allow_check(expression.function, type.t1, context):
            return False
        
        return allow_check(expression.argument, type.t2, context)
    elif isinstance(expression, Product):
        if not isinstance(type, ConjunctiveProduct):
            return False
        elif not allow_check(expression.e1, type.t1, context):
            return False
        return allow_check(expression.e2, type.t2, context)
    elif isinstance(expression, ConsumeBoth):
        if not isinstance(expression.e1, Product):
            return False
        elif not isinstance(expression.e2, Abstraction):
            return False
        elif not allow_check(expression.e1, type.t1, context):
            return False
        return allow_check(expression.e2, type.t2, context)
    
    elif isinstance(expression, Sum):
        if not isinstance(type, SumType):
            return False
        if (expression.choice == SumChoice.INL):
            return allow_check(expression.expr, type.t1, context)
        else:
            return allow_check(expression.expr, type.t2, context)
    elif isinstance(expression, Case):
        if not isinstance(type, CaseType):
            return False
        elif not allow_check(expression.sum, type.t1, context):
            return False
        else:
            context_copy = deepcopy(context)
            answer = allow_check(expression.f1, Type(type.t1.t1, type.t2), context) and allow_check(expression.f1, Type(type.t1.t2, type.t2), context)
            for key in context.keys():
                if key not in context_copy:
                    context.pop(key)
            return answer

    elif isinstance(expression, And):
        if not isinstance(type, ConjunctiveSum):
            return False
        context_copy = deepcopy(context)
        answer = allow_check(expression.e1, type.t1, context) and allow_check(expression.e1, type.t1, context_copy)
        for key in context.keys():
            if key not in context_copy:
                context.pop(key)
        return answer
    elif isinstance(expression, ConsumeOne):
        if not isinstance(type, DestructConjunctiveSum):
            return False
        return allow_check(expression.e, type.t1, context)

def check_with_context(expression, type, context={}):
    if isinstance(expression, Unit):
        return isinstance(type, UnitType) and not context
    elif isinstance(expression, Variable):
        return expression in context and context[expression] == type and len(context.keys()) == 1
    
    elif isinstance(expression, Abstraction):
        context[expression.param] = type.t1
        return check_with_context(expression.body, type.t2, context)
    elif isinstance(expression, Application):
        if not allow_check(expression.function, type.t1, context):
            return False
        
        return check_with_context(expression.argument, type.t2, context)
    
    elif isinstance(expression, Product):
        if not isinstance(type, ConjunctiveProduct):
            return False
        if not allow_check(expression.e1, type.t1, context):
            return False
        return check_with_context(expression.e2, type.t2, context)
    elif isinstance(expression, ConsumeBoth):
        if not isinstance(type, DestructConjunctiveProduct):
            return False
        elif not allow_check(expression.e1, type.t1, context):
            return False
        return check_with_context(expression.e2, type.t2, context)
    
    elif isinstance(expression, Sum):
        if not isinstance(type, SumType):
            return False
        if(expression.choice == SumChoice.INL):
            return check_with_context(expression.expr, type.t1, context)
        else:
            return check_with_context(expression.expr, type.t2, context)
    elif isinstance(expression, Case):
        if not isinstance(type, CaseType):
            return False
        elif not allow_check(expression.sum, type.t1, context):
            return False
        else:
            context_copy = deepcopy(context)
            return check_with_context(expression.f1, Type(type.t1.t1, type.t2), context) and check_with_context(expression.f1, Type(type.t1.t2, type.t2), context)
        
    elif isinstance(expression, And):
        if not isinstance(type, ConjunctiveSum):
            return False
        context_copy = deepcopy(context)
        return check_with_context(expression.e1, type.t1, context) and check_with_context(expression.e1, type.t1, context_copy)
    elif isinstance(expression, ConsumeOne):
        if not isinstance(type, DestructConjunctiveSum):
            return False
        return check_with_context(expression.e, type.t1, context)
    