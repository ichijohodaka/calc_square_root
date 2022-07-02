from decimal import *

getcontext().prec = 30 # you want to use many digits to calc

def one_step( a: Decimal ) -> Decimal:
    x = Decimal('3') /( a*a ) - Decimal('1') # |x| must be less than 1
    return a * ( Decimal('1') + x/Decimal('2'))

a = 3
print(a)
a = one_step(a)
print(a)
a = one_step(a)
print(a)
a = one_step(a)
print(a)
a = one_step(a)
print(a)
a = one_step(a)
print(a)
a = one_step(a)
print(a)

