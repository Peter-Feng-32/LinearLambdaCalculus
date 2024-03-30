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
    
class Type:
    def __init__(self, is_unit, t1=None, t2=None):
        self.is_unit = is_unit
        self.t1 = t1
        self.t2 = t2
    def __eq__(self, other):
        return self.is_unit == other.is_unit and self.t1 == other.t1 and self.t2 == other.t2