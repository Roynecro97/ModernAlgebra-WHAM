from __future__ import annotations

from random import randrange
from typing import Optional

def extended_gcd(a: int, b: int) -> tuple[int, int, int]:
    """
    Returns the extended gcd of a and b

    Parameters
    ----------
    a : Input data.
    b : Input data.
    Returns
    -------
    (d, x, y): d = gcd(a,b) = a*x + b*y
    """
    if not a:
        return (b, 0, 1)
    d, y, x = extended_gcd(b % a, a)
    return (d, x - (b // a) * y, y)


def modular_inverse(a: int, n: int) -> Optional[int]:
    """
    Returns the inverse of a modulo n if one exists

    Parameters
    ----------
    a : Input data.
    n : Input data.

    Returns
    -------
    x: such that (a*x % n) == 1 and 0 <= x < n if one exists, else None
    """
    # Fast implementation (using C) in Python 3.8:
    # try:
    #     return pow(a, -1, n)
    # except ValueError:
    #     return None

    # Slow algorithm:
    # If ``gcd(a, n) == 1`` then ``x*a + _*n == 1`` so ``x`` is ``a``'s modular inverse
    d, x, _ = extended_gcd(a, n)
    if d != 1:
        return None
    return x % n


def modular_exponent(a: int, d: int, n: int) -> int:
    """
    Returns a to the power of d modulo n

    Parameters
    ----------
    a : The exponential's base.
    d : The exponential's exponent.
    n : The exponential's modulus.

    Returns
    -------
    b: such that b == (a**d) % n
    """
    # Fast implementation using C:
    return pow(a, d, n)

    # Slow algorithm:
    a = a % n
    p = 1
    print(f'finding {a}**{d} % {n} .. {bin(d)=} .. {bin(d)[2:][::-1]}')
    for i, b in enumerate(bin(d)[2:][::-1]):
        if b == '1':
            print(f'{a} ** (2 ** {i})')
            p = (p * ((a ** (2 ** i)) % n)) % n
    return p


def miller_rabin(n: int) -> bool:
    """
    Checks the primality of n using the Miller-Rabin test

    Parameters
    ----------
    n : The number to check

    Returns
    -------
    b: If n is prime, b is guaranteed to be True.
    If n is not a prime, b has a 3/4 chance at least to be False
    """
    a = randrange(1, n)
    k = 0
    d = n - 1
    while d % 2 == 0:
        k = k + 1
        d = d // 2
    x = modular_exponent(a, d, n)
    if x == 1 or x == n - 1:
        return True
    for _ in range(k):
        x = (x * x) % n
        if x == 1:
            return False
        if x == n - 1:
            return True
    return False


def is_prime(n: int) -> bool:
    """
    Checks the primality of n

    Parameters
    ----------
    n : The number to check

    Returns
    -------
    b: If n is prime, b is guaranteed to be True.
    If n is not a prime, b has a chance of less than 1e-10 to be True
    """
    for _ in range(10):
        if not miller_rabin(n):
            return False
    return True


def generate_prime(digits: int) -> Optional[int]:
    for _ in range(digits * 10):
        n = randrange(10 ** (digits - 1), 10 ** digits)
        if is_prime(n):
            return n
    return None
