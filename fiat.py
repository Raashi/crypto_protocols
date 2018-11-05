import random

from utils import *
import prime
import hashlib

DEFAULT_PQ_SIZE = 128
DEFAULT_KEY_SIZE = 10
DEFAULT_FILENAME = 'test.flac'
crypto_hash = hashlib.sha1


def gen_params(pq_size, k):
    p = prime.gen_prime(pq_size)
    q = prime.gen_prime(pq_size)
    n = p * q
    write('n.txt', n)
    write('k.txt', k)


def gen_keys(n, k):
    s = []
    while len(s) < k:
        si = random.randint(1, n - 1)
        if gcd(si, n) == 1:
            s.append(si)
    v = [pow(get_inverse(si, n), 2, n) for si in s]
    write('s_key.txt', s)
    write('v_key.txt', v)


def sign(n, k, m, sk):
    r = random.randint(1, n - 1)
    u = pow(r, 2, n)
    e = crypto_hash(m + u.to_bytes(len(bin(u)) - 2, byteorder='big')).digest()
    e = int.from_bytes(e, byteorder='big')
    ek = get_bits(e, k)
    s = r
    for (si, ei) in zip(sk, ek):
        s = s * pow(si, ei, n) % n
    write('ds.txt', (e, s))


def check(ds, m, n, k, v):
    e, s = ds
    ek = get_bits(e, k)
    w = pow(s, 2, n)
    for (vi, ei) in zip(v, ek):
        w = w * pow(vi, ei, n) % n
    es = crypto_hash(m + w.to_bytes(len(bin(w)) - 2, byteorder='big')).digest()
    es = int.from_bytes(es, byteorder='big')
    if e == es:
        print('Подпись подлинная')
    else:
        print('Подпись недействительна')


def main():
    operation = sys.argv[1]

    if operation == '-gp':
        gen_params(int(sys.argv[2]), int(sys.argv[3]))
    elif operation == '-gk':
        gen_keys(*read_mul('n.txt', 'k.txt'))
    elif operation == '-s':
        sign(*read_mul('n.txt', 'k.txt'), read_bin(sys.argv[2], False), read_struct('s_key.txt'))
    elif operation == '-c':
        check(read_struct('ds.txt'), read_bin(sys.argv[2], False), read('n.txt'), read('k.txt'), read_struct('v_key.txt'))
    elif operation == '-clean':
        for entry in os.listdir(FULL_NAME_PROTOCOL):
            os.remove(os.path.join(FULL_NAME_PROTOCOL, entry))


if __name__ == '__main__':
    main()
