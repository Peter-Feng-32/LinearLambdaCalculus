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

class Product(Expression):
    # Product type is not part of default STLC, it is something we need to add in
    def __init__(self, e1 : Expression, e2: Expression) -> None:
        self.e1 = e1
        self.e2 = e2
    def __str__(self) -> str:
        return f"<{self.e1}, {self.e2}>"
class ConsumeBoth(Expression):
    def __init__(self, e1: Product, e2: Application) -> None:
        self.e1 = e1
        self.e2 = e2
    def __str__(self) -> str:
        return f"destruct {self.e1} as {self.e2}"
    
class SumChoice(Enum):
    INL = "inl"
    INR = "inr"
class Sum(Expression):
    def __init__(self, expr: Expression, choice: SumChoice):
        self.expr = expr
        self.choice = choice
    def __str__(self):
        return f"{self.choice} {self.expr}"
class Case(Expression):
    def __init__(self, sum : Sum, f1 : Abstraction, f2 : Abstraction):
        self.sum = sum
        self.f1 = f1
        self.f2 = f2
    def __str__(self):
        return f"case {self.sum} {self.f1} {self.f2}"

class And(Expression):
    def __init__(self, e1 : Expression, e2: Expression) -> None:
        self.e1 = e1
        self.e2 = e2
    def __str__(self) -> str:
        return f"<<{self.e1}, {self.e2}>>"
class ConsumeOne(Expression):
    def __init__(self, use_first : bool, e: And) -> None:
        self.use_first = use_first
        self.e = e
    def __str__(self) -> str:
        if self.use_first:
            return f"fst {self.e}"
        return f"snd {self.e}"
    

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
        return self.t1 == other.t1 and self.t2 == other.t2

class DestructConjunctiveProduct(Type):
    # t1 is the type of the product, t2 is the type of destroying function
    def __init__(self, t1, t2):
        super().__init__(t1, t2)

    def __eq__(self, other):
        return self.t1 == other.t1 and self.t2 == other.t2

class SumType(Type):
    def __init__(self, t1, t2):
        super().__init__(t1, t2)

    def __eq__(self, other):
        return self.t1 == other.t1 and self.t2 == other.t2
class CaseType(Type):
    # t1 is the sum type, t2 is the output type of both case functions
    def __init__(self, t1, t2):
        super().__init__(t1, t2)

    def __eq__(self, other):
        return self.t1 == other.t1 and self.t2 == other.t2

class ConjunctiveSum(Type):
    def __init__(self, t1, t2):
        super().__init__(t1, t2)

    def __eq__(self, other):
        return self.t1 == other.t1 and self.t2 == other.t2
class DestructConjunctiveSum(Type):
    # t1 is the type of the conjunctive sum
    def __init__(self, t1):
        super().__init__(t1)

    def __eq__(self, other):
        return self.t1 == other.t1
    