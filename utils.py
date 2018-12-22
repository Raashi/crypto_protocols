import os
import sys
import random

NAME_PROTOCOL = os.path.basename(sys.argv[0])[:-3]
FULL_NAME_PROTOCOL = 'files_' + NAME_PROTOCOL

if not os.path.exists(FULL_NAME_PROTOCOL):
    os.mkdir(FULL_NAME_PROTOCOL)

MAX_PRIMITIVE_ROOT_TRIALS = 10000


def read(filename):
    with open(os.path.join(FULL_NAME_PROTOCOL, filename)) as f:
        return int(f.read())


def read_string(filename):
    with open(os.path.join(FULL_NAME_PROTOCOL, filename)) as f:
        return f.read()


def read_mul(*filenames):
    return (read(arg) for arg in filenames)


def read_struct(filename):
    filename = os.path.join(FULL_NAME_PROTOCOL, filename)
    if not os.path.exists(filename):
        print('ОШИБКА: файл {} не существует'.format(filename))
        exit(1)
    with open(filename) as f:
        return eval(f.read())


def read_bin(filename, subfolder=True):
    filename = os.path.join(FULL_NAME_PROTOCOL, filename) if subfolder else filename
    with open(filename, 'rb') as f:
        return f.read()


def write(filename, value):
    with open(os.path.join(FULL_NAME_PROTOCOL, filename), 'w') as f:
        f.write(str(value))


def cleanup():
    for entry in os.listdir(FULL_NAME_PROTOCOL):
        os.remove(os.path.join(FULL_NAME_PROTOCOL, entry))


def gcd(x, y):
    x, y = max(x, y), min(x, y)
    while y:
        x, y = y, x % y
    return x


def egcd(a, b):
    r0, r1 = a, b
    x0, x1 = 1, 0
    y0, y1 = 0, 1

    q, r2 = r0 // r1, r0 % r1
    while r2 != 0:
        x1, x0 = x0 - q * x1, x1
        y1, y0 = y0 - q * y1, y1

        r1, r0 = r2, r1
        q, r2 = r0 // r1, r0 % r1

    return r1, x1, y1


def get_inverse(a: int, m: int):
    if a == 0:
        return 0
    if gcd(a, m) != 1:
        raise ValueError('Не существует обратного элемента для a={} по модулю m={}'.format(a, m))
    d, x, y = egcd(a, m)
    return x % m


def ratio(p, q, m):
    return p * get_inverse(q, m) % m


def get_bits(e: int, count=-1):
    return [int(bit) for bit in bin(e)[2:count]]


def primitive(p, q2):
    """Только для простых p"""
    degs = [p // qi[0] for qi in q2]
    for _trial in range(MAX_PRIMITIVE_ROOT_TRIALS):
        g = random.randint(2, p - 1)
        if all([pow(g, d, p) != 1 for d in degs]):
            return g
    raise ArithmeticError('Не могу найти примитивный корень в GF({})'.format(p + 1))


def is_primitive(p, h, q2):
    """Только для простых p"""
    degs = [p // qi[0] for qi in q2]
    return all([pow(h, d, p) != 1 for d in degs])
