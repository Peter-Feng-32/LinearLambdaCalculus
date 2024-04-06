from enum import Enum
class Expression:
    pass

class Normal:
    pass

class Unit(Expression):
    def __str__(self) -> str:
        return "<>"

class Variable(Expression):
    def __init__(self, name: str) -> None:
        self.name = name
    def __str__(self) -> str:
        return self.name
    def __eq__(self, other):
        return self.name == other.name
    def __hash__(self):
        return hash(self.name)

class Abstraction(Expression, Normal):
    def __init__(self, param: Expression, body: Expression) -> None:
        self.param = param
        self.body = body
    def __str__(self) -> str:
        return f"(λ({self.param}). ({self.body}))"

class Application(Expression):
    def __init__(self, function: Expression, argument: Expression) -> None:
        self.function = function
        self.argument = argument   
    def __str__(self) -> str:
        return f"(({self.function}) ({self.argument}))"

#Additive - same context, multiplicative - different contexts.
#Todo: There's two types of products to implement.  Multiplicative conjunction(A ⊗ B, both parts of the product must be used, deconstruct by adding both to product), additive conjunction(only one of the product's things must be used(corresponding to elimination with fst and snd)). 
#Additive basically means your context supports both possibilities, but only one at a time, meaning you can't have both parts of the product.  (note: to implement this we may need multiple instances of the same mapping in context.  how to handle?).  Let's us introduce a pair of possibilities and pick one of them later on.

#Note: disjunction aka + operator from class only requires one or the other to be supported by the context - ie. it doesn't have to support both possibilities.
class Product(Expression):
    # Product type is not part of default STLC, it is something we need to add in
    def __init__(self, e1 : Expression, e2: Expression) -> None:
        self.e1 = e1
        self.e2 = e2
    def __str__(self) -> str:
        return f"<{self.e1}, {self.e2}>"
    
class SumChoice(Enum):
    INL = "inl"
    INR = "inr"
class Sum(Expression):
    def __init__(self, expr: Expression, choice: SumChoice):
        self.expr = expr
        self.choice = choice
    def __str__(self):
        return f"{self.choice} {self.expr}"

class And(Expression):
    def __init__(self, e1 : Expression, e2: Expression) -> None:
        self.e1 = e1
        self.e2 = e2
    def __str__(self) -> str:
        return f"<<{self.e1}, {self.e2}>>"
    
class Type:
    def __init__(self, t1=None, t2=None):
        self.t1 = t1
        self.t2 =t2

class UnitType(Type):
    def __init__(self):
        Type.__init__(self)
    
    def __eq__(self, other):
        return True

class ConjunctiveProduct(Type):
    def __init__(self, t1, t2):
        super().__init__(t1, t2)
    
    def __eq__(self, other):
        return self.t1 == other.t1

class SumType(Type):
    def __init__(self, t1, t2):
        super().__init__(t1, t2)

    def __eq__(self, other):
        return self.t1 == other.t1

class ConjunctiveSum(Type):
    def __init__(self, t1, t2):
        super().__init__(t1, t2)

    def __eq__(self, other):
        return self.t1 == other.t1
    