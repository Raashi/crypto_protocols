import random

from utils import *
import prime
import hashlib

size_default = 128
crypto_hash = hashlib.sha1


def gen_n(n_size):
    p = prime.gen_prime(n_size)
    q = prime.gen_prime(n_size)
    print('n сгенерировано\np={}\nq={}'.format(p, q))
    write('n.txt', p * q)


def gen_keys(n):
    pass


if __name__ == '__main__':
    operation = sys.argv[1]
    size = size_default if len(sys.argv) < 3 else int(sys.argv[2])

    if operation == '-gn':
        gen_n(size)
    elif operation == '-gk':
        pass
