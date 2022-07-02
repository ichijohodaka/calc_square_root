# square root of 3 = 1.732050807568877293527446341505872366942805253810380628055806979451933016908800037081146186757248576 ...
# use a hint a with a**2 > 3/2
# a=2, a=3, ...e.g. 
# An obvious choice is a = 3
# (1 + x)**(1/2) = 1 + 1/2 * x + ...

def one_step( a: float ) -> float:
    x = 3 /( a**2 ) - 1 # |x| must be less than 1
    return a * (1 + x/2)

a = 3
print(a)

a = one_step( a )
print( a )

a = one_step( a )
print( a )

a = one_step( a )
print( a )

# repeat until satisfied

