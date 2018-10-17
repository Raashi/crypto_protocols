import os
import sys
import random

import prime

size_default = 128

OPERATIONS = ['-gp', '-gk', '-gx', '-gc', '-gs', '-a']
NAME_PROTOCOL = os.path.basename(__file__)[:-3]


def read(filename):
    with open(os.path.join('files_' + NAME_PROTOCOL, filename)) as f:
        return int(f.read())


def read_arr(*filenames):
    return (read(arg) for arg in filenames)


def write(filename, value):
    with open(os.path.join('files_' + NAME_PROTOCOL, filename), 'w') as f:
        f.write(str(value))


def gen_params(size):
    p, q, g = prime.gen_pq(size)
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
        gen_keys(*read_arr('p.txt', 'q.txt', 'g.txt'))
    elif operation == '-gx':
        gen_x(*read_arr('p.txt', 'q.txt', 'g.txt'))
    elif operation == '-gc':
        gen_c(read('q.txt'))
    elif operation == '-gs':
        gen_s(*read_arr('q.txt', 'r.txt', 'c.txt', 'a.txt'))
    elif operation == '-a':
        validate(*read_arr('p.txt', 'g.txt', 'v.txt', 's.txt', 'c.txt', 'x.txt'))
    else:
        raise ValueError('Возможные команды: -gp, -gk, -a')


if __name__ == '__main__':
    main()
