def one_step( n: float, a: float ) -> float:
    x = n /( a**2 ) - 1 # |x| must be less than 1
    return a * (1 + x/2)

def hint( n: float ) -> float:
    if n>1:
        return n
    else:
        return 1

n = 3
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