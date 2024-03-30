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
    
class Type:
    def __init__(self, is_unit=False, is_product=False, t1=None, t2=None):
        self.is_unit = is_unit
        self.is_product = is_product
        self.t1 = t1
        self.t2 = t2
    def __eq__(self, other):
        return self.is_unit == other.is_unit and self.is_product == other.is_product and self.t1 == other.t1 and self.t2 == other.t2