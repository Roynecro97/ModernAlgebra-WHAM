# ModernAlgebra-WHAM

Modern Algebra RSA project (Winter 2021-2022)

Answers with explanations to the project's riddles.

For a prettier rendering of the answers, see [here](./notebook.ipynb)

## 1. Loki & Spiderman

### Riddle

Loki wants to be paid 1,000,000$ exactly. Spiderman only has coins that are worth 797$ each. Loki suggests providing change but only with 5279$ bills.

Is there a chance for such a transaction? How?

### Answer

The question is if there is a solution to `797 * x = 1000000 (mod 5279)`. We need to find the modular inverse.

```python
from number_theory_functions import modular_inverse

loki_bill = 5279
goal = 1_000_000
spiderman_coin = 797

goal_inverse = modular_inverse(goal, loki_bill)
x = modular_inverse((goal_inverse * spiderman_coin) % loki_bill, loki_bill)
if x is None:
    print("Not Possible")
else:
    change = x * spiderman_coin - goal
    assert change >= 0
    assert change % loki_bill == 0
    change_bills = change // loki_bill
    print(f"Spiderman can pay with {x} coins and get {change_bills} bills ({change}$) as change")
```

> Spiderman can pay with 3977 coins and get 411 bills (2169669$) as change

## 2. Hundreds digit

### Riddle

What is the hundredth digit of the number `(123456)**(7896543**(74365753))`

### Answer

We want to find the result of integer division of `((123456**(7896543**74365753)) % 1000) // 100`.

According to the conclusions from Lagrange's theorem, if `G` is a finite group and `a` is in `G`, then `o(a) | |G|`.

`G = Z_1000` so,
`((123456 % 1000)**((7896543**74365753) % 1000)) % 1000`

```python
from number_theory_functions import modular_exponent

exp = modular_exponent(7896543, 74365753, 1000)
hundreds_digit = modular_exponent(123456, exp, 1000) // 100
print(f"The hundreds digit of 123456**(7896543**74365753) is {hundreds_digit}")
```

> The hundreds digit of 123456**(7896543**74365753) is 0

## 3. Cipher 42

### Riddle

Given a public key `e = 3499`, `N = 12215009`, and an encrypted message `42`. Crack the code.
(Hint: You should first guess the private key, given a magic Crystal ball or wolfram alpha)

### Answer

We know those params:

`e = 3499`

`N = 12215009`

`Me = (M**e) % (phi(N)) = 42`

First, we calculate `phi(N)` with an online Euler's Function calculator:
`phi(N) = 12208020`

Now, we use wolfram alpha to calculate d:
`d = 5425399`

Now, we calculate the cipher by raising `42` to the power of `d`, mod `phi(N)`:
`M = modular_exponent(42, 5425399, 12208020)`

```python
from number_theory_functions import modular_exponent

e = 3499
phi_N = 12208020
Me = 42

M = modular_exponent(Me, e, phi_N)
print(f"Cracked the code! The ciphered code is {M}")
```

> Cracked the code! The ciphered code is 6014508

## 4. Finding the Inverse Function

### Riddle

Look at the function `E(x) = x^e (mod N)` where `e = 11` and `N = 991`.
Is `E` inversible? If so, calculate `D(y) = E(x)^-1`.

### Answer

Based on _RSA_'s algorithm, we're looking for `D(y) = y^d (mod N)` such that `ed === 1 (mod phi(N))`.

`N = 991` is a prime number, therefore `phi(N) = N - 1`.

We'll try to find such `d`:

```python
from number_theory_functions import modular_inverse

e = 11
N = 991

d = modular_inverse(e, N - 1)

if d is None:
    print("D(y) does not exist")
else:
    print("D(y) := (y ** {d}) % {N}")
```

> D(y) does not exist

## 5. Encrypt

### Riddle

Given `q = 6841` and `p = 7919`, choose a message and a public key `e` and encrypt the message.
(Show your original message, the public key and the encrypted message)

### Answer

We can use our RSA implementation to find a valid public key `e` and encrypt the message.

```python
from rsa_functions import RSA

p = 7919
q = 6841

rsa = RSA.from_primes(p, q)

plain = 42
encrypted = rsa.encrypt(plain)
assert encrypted is not None
assert plain == rsa.decrypt(encrypted)

print(f"e = {rsa.public_key[1]}")
print(f"the plain message: {plain}")
print(f"the encrypted message: {rsa.encrypt(plain)}")
```

> e = 33551899
> the plain message: 42
> the encrypted message: 6083595
