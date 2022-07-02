from decimal import *

getcontext().prec = 30

def one_step( n: Decimal, a: Decimal ) -> Decimal:
    x = n /( a*a ) - Decimal('1') # |x| must be less than 1
    return a * (Decimal('1') + x/Decimal('2'))

def hint( n: Decimal ) -> Decimal:
    if n>Decimal('1'):
        return n
    else:
        return Decimal('1')

n = Decimal('10')
a = hint(n)
print(a)

a = one_step(n,a)
print(a)

a = one_step(n,a)
print(a)

a = one_step(n,a)
print(a)

a = one_step(n,a)
print(a)

a = one_step(n,a)
print(a)

a = one_step(n,a)
print(a)