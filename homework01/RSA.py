def is_prime(n: int) -> bool:
    for i in range(2,n):
        if n % i == 0:
            return False
        else:
            return True

def gcd(a: int, b: int) -> int:
    while (a % b != 0):
        c = a % b
        a = b
        b = c
    return b 

def generate_keypair(p: int, q: int) -> Tuple[Tuple[int, int], Tuple[int, int]]:
    if not (is_prime(p) and is_prime(q)):
        raise ValueError('Both numbers must be prime.')
    elif p == q:
        raise ValueError('p and q cannot be equal')
    n = p*q
    phi = (p-1)*(q-1)
    e = random.randrange(1, phi)
    g = gcd(e, phi)
    while g != 1:
        e = random.randrange(1, phi)
        g = gcd(e, phi)

    # Use Extended Euclid's Algorithm to generate the private key
    d = multiplicative_inverse(e, phi)
    # Return public and private keypair
    # Public key is (e, n) and private key is (d, n)
    return ((e, n), (d, n))


p = int(input("Enter first number"))
q = int(input("Enter second number"))
print(is_prime(p))
