import sys
import time
import random

from utils import read, write
import prime
prime.k_min = 1
prime.k_max = 10


MAX_PRIMITIVE_ROOT_TRIALS = 10000


def primitive_root(p):
    """Только для простых p"""
    q = p = p - 1
    while q & 2 == 0:
        q >>= 1
    degs = [p // 2, p // q]
    for _trial in range(MAX_PRIMITIVE_ROOT_TRIALS):
        g = random.randint(2, p)
        if all([pow(g, d, p) != 1 for d in degs]):
            return g
    raise ArithmeticError('Не могу найти примитивный корень в GF({})'.format(p + 1))


def gen_params(size):
    start = time.time()
    n, q = prime.gen_diffie(size)
    print('Генерация n заняла {:.3f}'.format(time.time() - start))
    g = primitive_root(n)
    write('n.txt', n), write('g.txt', g)


def gen_x(n, g):
    x = random.randint(1, n - 1)
    ax = pow(g, x, n)
    write('x.txt', x), write('ax.txt', ax)


def gen_y(n, g):
    y = random.randint(1, n - 1)
    by = pow(g, y, n)
    write('y.txt', y), write('by.txt', by)


def compute_ka(n, x, by):
    ka = pow(by, x, n)
    write('ka.txt', ka)


def compute_kb(n, y, ax):
    kb = pow(ax, y, n)
    write('kb.txt', kb)


def main():
    op = sys.argv[1]

    if op == '-gp':
        gen_params(int(sys.argv[2]))
    elif op == '-gx':
        gen_x(read('n.txt'), read('g.txt'))
    elif op == '-gy':
        gen_y(read('n.txt'), read('g.txt'))
    elif op == '-ka':
        compute_ka(read('n.txt'), read('x.txt'), read('by.txt'))
    elif op == '-kb':
        compute_kb(read('n.txt'), read('y.txt'), read('ax.txt'))
    elif op == '-c':
        ka, kb = read('ka.txt'), read('kb.txt')
        print('Ka = {}\nKb = {}'.format(ka, kb))
        print('Ключи одинаковые' if ka == kb else 'Ошибка: ключи разные')
    else:
        print('Wrong operation')


if __name__ == '__main__':
    main()
