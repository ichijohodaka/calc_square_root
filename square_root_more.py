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

d = Decimal('.00000000000001')
n = Decimal('3')
a = hint(n)
print(a)

while True:
    a1 = one_step(n, a)
    print(a1)
    z = (a - a1).quantize(d, rounding=ROUND_DOWN)
    if z == Decimal('0'):
        break
    a = a1

# 1.732050807568877293527446341505872366942805253810380628055806979451933016908800037081146186757248576  
