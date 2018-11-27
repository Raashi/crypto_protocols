import sys
import copy
import random
from operator import add
from functools import reduce

from utils import read, read_struct, write, ratio, cleanup
from prime import gen_prime


def solve(mat_orig, d, p, check_for_dependence):
    mat = copy.deepcopy(mat_orig)
    d = d[:]
    k = len(mat)
    for i in range(k):
        aii = mat[i][i]
        for j in range(len(mat[0])):
            mat[i][j] = ratio(mat[i][j], aii, p)
        d[i] = ratio(d[i], aii, p)
        if check_for_dependence and mat[i][i] == 0:
            return False
        assert mat[i][i] == 1
        for row in range(k):
            if row != i:
                coeff = -mat[row][i] % p
                d[row] = (d[row] + d[i] * coeff) % p
                for col in range(len(mat[0])):
                    mat[row][col] = (mat[row][col] + mat[i][col] * coeff) % p
                if check_for_dependence and not any(mat[row]):
                    if i < k - 1:
                        return False
    return True if check_for_dependence else d


def gen_parts(p_size, m, n, k):
    with open(m, 'rb') as f:
        msg = int.from_bytes(f.read(), byteorder='big')

    msg_size = msg.bit_length()
    if p_size <= msg_size:
        p_size = msg_size + 1
        print('Размер модуля изменен до размера сообщения {} бит'.format(p_size))
    p = gen_prime(p_size)
    if msg >= p:
        raise ValueError('Сообщение больше модуля: msg={} > p={}'.format(msg, p))
    q = [msg] + [random.randint(0, p - 1) for _idx in range(k - 1)]

    while True:
        parts = []
        mat, ds = [], []
        for i in range(n):
            coeffs = [random.randint(0, p - 1) for _idx in range(k)]
            d = -reduce(add, map(lambda ax: ax[0] * ax[1] % p, zip(coeffs, q))) % p
            parts.append(tuple(coeffs + [d]))
            mat.append(coeffs), ds.append(-d % p)

        if not solve(mat, ds, p, True):
            break

    write('p.txt', p), write('k.txt', k)
    for idx, part in enumerate(parts):
        write('part_{}.txt'.format(idx + 1), part)


def check_secret(p, parts):
    mat = [list(part)[:-1] for part in parts]
    d = [-part[-1] % p for part in parts]
    sol = solve(mat, d, p, False)
    x = sol[0]
    secret = bytes.fromhex(hex(x)[2:]).decode('windows-1251')
    print('Секрет =', secret)


def main():
    if sys.argv[1] == '-g':
        p_size, msg, n, k = int(sys.argv[2]), sys.argv[3], int(sys.argv[4]), int(sys.argv[5])
        gen_parts(p_size, msg, n, k)
    elif sys.argv[1] == '-c':
        idx_parts = list(map(lambda idx: int(idx), sys.argv[2:]))
        if len(set(idx_parts)) != len(idx_parts):
            print('Дупликаты в массиве индексов')
            return
        parts = [read_struct('part_{}.txt'.format(idx)) for idx in idx_parts]
        check_secret(read('p.txt'), parts)
    elif sys.argv[1] == '-clean':
        cleanup()
    else:
        print('Неверный код операции')


if __name__ == '__main__':
    main()
    # mat = [
    #     [1, 1, 1],
    #     [2, 2, 2],
    #     [2, 3, 2],
    #     [1, 3, 4]
    # ]
    # d = [1, 2, 3, 4]
    # print(solve(mat, d, 5, True))
