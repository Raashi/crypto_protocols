import random
import operator
import functools

from utils import gcd


small_primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]  # длина - 33 бита
mul_small_primes = functools.reduce(operator.mul, small_primes)

miller_rabin_tests_count = 5

k_min = 1
k_max = 20


def check_len(q, desired_size):
    return len(bin(q)) - 2 == desired_size


def isprime(p):
    q = p - 1
    m = 0
    while q & 1 == 0:
        m += 1
        q //= 2
    s = q

    r = 0
    while r < miller_rabin_tests_count:
        a = random.randint(2, p - 2)
        while gcd(a, p) > 1:
            a = random.randint(2, p - 2)
        b = pow(a, s, p)
        if b == 1:
            continue
        elif b == p - 1:
            r += 1
            continue

        for l in range(1, m):
            c = pow(a, s * pow(2, l), p)
            if c == p - 1:
                r += 1
                break
        else:
            return False
    return True


def gen_odd_q(size):
    q = random.randint(2 ** (size - 1), 2 ** size - 1)
    if q & 1 == 0:
        q += 1
    return q


def gen_relatively_prime(size):
    q = gen_odd_q(size)

    while gcd(q, mul_small_primes) > 1 or q % 4 != 3:
        q += 2
        if not check_len(q, size):
            q = gen_odd_q(size)

    return q


def gen_prime(size):
    diff = 2
    q = gen_odd_q(size)

    if size > 50:
        q = gen_relatively_prime(size)
        diff = mul_small_primes

    while not isprime(q) or q % 4 != 1:
        q += diff
    return q


def gen_schnorr(size):
    while True:
        q = gen_prime(size)
        p = q << (k_min - 1)
        for idx in range(k_min, k_max):
            p <<= 1
            if isprime(p + 1):
                p += 1
                break
        else:
            continue
        break

    while True:
        g = random.randint(1, p - 1)
        if pow(g, q, p) == 1:
            return p, q, g


def gen_diffie(size):
    while True:
        q = gen_prime(size)
        p = q << (k_min - 1)
        for idx in range(k_min, k_max):
            p <<= 1
            if isprime(p + 1):
                p += 1
                break
        else:
            continue
        return p, q
