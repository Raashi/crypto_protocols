import random

from utils import *
import prime

size_default = 128

OPERATIONS = ['-gp', '-gk', '-gx', '-gc', '-gs', '-a']


def gen_params(size):
    p, q, g = prime.gen_schnorr(size)
    write('p.txt', p)
    write('q.txt', q)
    write('g.txt', g)


def gen_keys(p, q, g):
    a = random.randint(2, q - 1)
    v = pow(g, (-a) % q, p)
    write('a.txt', a)
    write('v.txt', v)


def gen_x(p, q, g):
    r = random.randint(1, q - 1)
    x = pow(g, r, p)
    write('r.txt', r)
    write('x.txt', x)


def gen_c(q):
    c = random.randint(1, q - 1)
    write('c.txt', c)


def gen_s(q, r, c, a):
    s = (r + c * a) % q
    write('s.txt', s)


def validate(p, g, v, s, c, x):
    if (pow(g, s, p) * pow(v, c, p)) % p == x:
        print('Аутентификация пройдена')
        return True
    else:
        print('Ошибка аутентификации')
        return False


def main():
    operation = sys.argv[1]
    size = size_default if len(sys.argv) < 3 else int(sys.argv[2])

    if operation == '-gp':
        gen_params(size)
    elif operation == '-gk':
        gen_keys(*read_mul('p.txt', 'q.txt', 'g.txt'))
    elif operation == '-gx':
        gen_x(*read_mul('p.txt', 'q.txt', 'g.txt'))
    elif operation == '-gc':
        gen_c(read('q.txt'))
    elif operation == '-gs':
        gen_s(*read_mul('q.txt', 'r.txt', 'c.txt', 'a.txt'))
    elif operation == '-a':
        validate(*read_mul('p.txt', 'g.txt', 'v.txt', 's.txt', 'c.txt', 'x.txt'))
    else:
        raise ValueError('Возможные команды: {}'.format(OPERATIONS))


if __name__ == '__main__':
    main()
