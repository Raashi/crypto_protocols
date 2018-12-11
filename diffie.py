import sys
import time
import random

from utils import read, write, cleanup, primitive
import prime
prime.k_min = 1
prime.k_max = 10


def gen_params(size):
    start = time.time()
    n, q = prime.gen_diffie(size)
    print('Генерация n заняла {:.3f}'.format(time.time() - start))
    g = primitive(n)
    write('n.txt', n), write('g.txt', g)


def gen_x(n, g):
    x = random.randint(1, n - 1)
    ax = pow(g, x, n)
    print('Ax =', ax)
    write('x.txt', x), write('ax.txt', ax)


def gen_y(n, g):
    y = random.randint(1, n - 1)
    by = pow(g, y, n)
    print('By =', by)
    write('y.txt', y), write('by.txt', by)


def compute_ka(n, x, by):
    ka = pow(by, x, n)
    print('Ka =', ka)
    write('ka.txt', ka)


def compute_kb(n, y, ax):
    kb = pow(ax, y, n)
    print('Kb =', kb)
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
    elif op == '-clean':
        cleanup()
        print('Папка очищена')
    else:
        print('Wrong operation')


if __name__ == '__main__':
    main()
