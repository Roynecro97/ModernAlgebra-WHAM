from __future__ import annotations
import math
from typing import Optional
import number_theory_functions

from random import randrange

class RSA():
    def __init__(self, public_key, private_key = None):
        self.public_key = public_key
        self.private_key = private_key

    @staticmethod
    def generate(digits = 10) -> RSA:
        """
        Creates an RSA encryption system object

        Parameters
        ----------
        digits : The number of digits N should have

        Returns
        -------
        RSA: The RSA system containing:
        * The public key (N,e)
        * The private key (N,d)
        """
        prime_length = randrange(1, digits)
        p = number_theory_functions.generate_prime(prime_length)
        q = number_theory_functions.generate_prime(digits - prime_length)
        while not p:
            p = number_theory_functions.generate_prime(prime_length)
        while not q:
            q = number_theory_functions.generate_prime(digits - prime_length)
        return RSA.from_primes(p, q)

    @staticmethod
    def from_primes(p: int, q: int) -> RSA:
        """
        Creates an RSA encryption system object from two primes.

        Parameters
        ----------
        p : A prime number
        q : A different prime number

        Returns
        -------
        RSA: The RSA system containing:
        * The public key (N,e)
        * The private key (N,d)
        """
        N = p * q
        K = (p - 1) * (q - 1)
        e = randrange(1, K)
        while math.gcd(e, K) != 1:
            e = randrange(1, K)
        d = number_theory_functions.modular_inverse(e, K)
        return RSA((N, e), (N, d))

    def encrypt(self, m: int) -> Optional[int]:
        """
        Encrypts the plaintext m using the RSA system

        Parameters
        ----------
        m : The plaintext to encrypt

        Returns
        -------
        c : The encrypted ciphertext
        """
        if not self.private_key:
            return None
        return number_theory_functions.modular_exponent(m, self.private_key[1], self.private_key[0])

    def decrypt(self, c: int) -> int:
        """
        Decrypts the ciphertext c using the RSA system

        Parameters
        ----------
        c : The ciphertext to decrypt

        Returns
        -------
        m : The decrypted plaintext
        """
        return number_theory_functions.modular_exponent(c, self.public_key[1], self.public_key[0])
