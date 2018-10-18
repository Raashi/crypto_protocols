import random

from utils import *
import prime
import hashlib

DEFAULT_PQ_SIZE = 128
DEFAULT_KEY_SIZE = 10
DEFAULT_FILENAME = 'ztest.txt'
crypto_hash = hashlib.sha1


def gen_params(pq_size, k):
    p = prime.gen_prime(pq_size)
    q = prime.gen_prime(pq_size)
    n = p * q

    s = []
    while len(s) < k:
        si = random.randint(1, n - 1)
        if prime.gcd(si, n) == 1:
            s.append(si)
    v = [pow(get_inverse(si, n), 2, n) for si in s]

    write('n.txt', n)
    write('k.txt', k)
    write('s_key.txt', s)
    write('v_key.txt', v)


def sign_r(n):
    r = random.randint(1, n - 1)
    write('r.txt', r)


def sign_u(n, r):
    u = pow(r, 2, n)
    write('u.txt', u)


def sign_e(m, u):
    e = crypto_hash(m + u.to_bytes(len(bin(u)) - 2, byteorder='big')).digest()
    write_bytes('e.bin', e)


def sign(n, r, k, s, e):
    ek = get_bits(e, k)
    s_sign = r
    for (si, ei) in zip(s, ek):
        s_sign = s_sign * pow(si, ei, n) % n
    write('s.txt', s_sign)


def check_w(n, k, s, v, e):
    ek = get_bits(e, k)
    w = pow(s, 2, n)
    for (vi, ei) in zip(v, ek):
        w = w * pow(vi, ei, n) % n
    write('w.txt', w)


def check_e(m, w):
    es = crypto_hash(m + w.to_bytes(len(bin(w)) - 2, byteorder='big')).digest()
    write_bytes('es.bin', es)


def check(e, es):
    if e == es:
        print('Подпись подлинная')
    else:
        print('Подпись недействительна')


def main():
    operation = sys.argv[1]

    if operation == '-gp':
        pq_size = DEFAULT_PQ_SIZE if len(sys.argv) < 3 else int(sys.argv[2])
        key_size = DEFAULT_KEY_SIZE if len(sys.argv) < 4 else int(sys.argv[3])
        gen_params(pq_size, key_size)
    # SIGNING
    elif operation == '-sr':
        sign_r(read('n.txt'))
    elif operation == '-su':
        sign_u(*read_multiple('n.txt', 'r.txt'))
    elif operation == '-se':
        filename = DEFAULT_FILENAME if len(sys.argv) < 3 else sys.argv[2]
        sign_e(read_bytes(filename), read('u.txt'))
    elif operation == '-s':
        sign(*read_multiple('n.txt', 'r.txt', 'k.txt'), read_arr('s_key.txt'), read_bytes('e.bin'))
    # CHECKING SIGN
    elif operation == '-cw':
        check_w(*read_multiple('n.txt', 'k.txt', 's.txt'), read_arr('v_key.txt'), read_bytes('e.bin'))
    elif operation == '-ces':
        filename = DEFAULT_FILENAME if len(sys.argv) < 3 else sys.argv[2]
        check_e(read_bytes(filename), read('w.txt'))
    elif operation == '-c':
        check(read_bytes('e.bin'), read_bytes('es.bin'))


if __name__ == '__main__':
    main()
