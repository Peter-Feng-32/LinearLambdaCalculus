from base import Type, UnitType, Expression, Product, Unit, Variable, Abstraction, Application, Sum, SumChoice, SumType, ConjunctiveProduct, ConjunctiveSum, And
from type_check import check_with_context

# Testing
e1, t1 = Unit(), UnitType() # passes
e2, t2 = Abstraction(Variable("x"), Unit()), Type(t1=UnitType(), t2=UnitType()) # fails because we do not use the fact that x is of the Unit Type (as desired)
e3, t3 = Abstraction(Variable("x"), Variable("x")), Type(t1=UnitType(), t2=UnitType()) # passes as we use x
e4, t4 = Abstraction(Variable("x"), Product(Variable("x"), Variable("x"))), Type(UnitType(), ConjunctiveProduct(UnitType(), UnitType())) # fails as we use x twice
e5, t5 = Application(Abstraction(Variable("x"), And(Variable("x"), Variable("x"))), Unit()), Type(Type(UnitType(), ConjunctiveSum(UnitType(), UnitType())), UnitType()) # passes
print(check_with_context(e1, t1))
print(check_with_context(e2, t2))
print(check_with_context(e3, t3))
print(check_with_context(e4, t4))
print(check_with_context(e5, t5))