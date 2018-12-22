from operator import mul
from functools import reduce
from utils import *
from prime import gen_diffie


def gen_pq(q_size):
    """Алиса"""
    p, qr = gen_diffie(q_size)
    write('p.txt', p), write('qr.txt', qr)


def gen_ht(p, qr):
    """Боб"""
    pp = reduce(mul, map(lambda qi: qi[0] ** qi[1], qr)) + 1
    if pp != p:
        print('ОШИБКА: разложение p не совпадает с самим p')
    h = primitive(p, qr)
    t = primitive(p, qr)
    write('h.txt', h)
    write('t.txt', t)


def gen_y(p, h, t, qr):
    """Алиса"""
    if not is_primitive(p, h, qr):
        print('ОШИБКА: h - не примитивный элемент в GF(p)')
        return
    if not is_primitive(p, t, qr):
        print('ОШИБКА: t - не примитивный элемент в GF(p)')
        return
    x = random.randint(2, p - 1)
    while gcd(x, p - 1) > 1:
        x = random.randint(2, p - 1)
    y = pow(h, x, p) if random.getrandbits(1) == 0 else pow(t, x, p)
    write('x.txt', x)
    write('y.txt', y)


def guess():
    write('guess.txt', 0 if random.getrandbits(1) == 0 else 1)


def flip(y, h, t, x, p, bit):
    if (bit == 0 and y == pow(h, x, p)) or (bit == 1 and y == pow(t, x, p)):
        coin = 'ОРЕЛ'
    else:
        coin = 'РЕШКА'
    print('Результат броска - {}'.format(coin))
    write('coin.txt', coin)


def check(y, h, t, x, p, bit, coin_real):
    if gcd(x, p - 1) > 1:
        print('ОШИБКА: x и p-1 не взаимно-простые')
        return
    if (bit == 0 and y == pow(h, x, p)) or (bit == 1 and y == pow(t, x, p)):
        coin = 'ОРЕЛ'
    else:
        coin = 'РЕШКА'
    if coin != coin_real:
        print('ОШИБКА: результат броска не совпадает с результатом проверки')
    else:
        print('Бросок верен')


def main():
    op = sys.argv[1]
    if op == '-gp' or op == 'debug':
        gen_pq(int(sys.argv[2]))
    if op == '-ght' or op == 'debug':
        gen_ht(read('p.txt'), read_struct('qr.txt'))
    if op == '-gy' or op == 'debug':
        gen_y(*read_mul('p.txt', 'h.txt', 't.txt'), read_struct('qr.txt'))
    if op == '-g' or op == 'debug':
        guess()
    if op == '-f' or op == 'debug':
        flip(*read_mul('y.txt', 'h.txt', 't.txt', 'x.txt', 'p.txt', 'guess.txt'))
    if op == '-c' or op == 'debug':
        check(*read_mul('y.txt', 'h.txt', 't.txt', 'x.txt', 'p.txt', 'guess.txt'), read_string('coin.txt'))
    if op == '-cleanup':
        cleanup()


if __name__ == '__main__':
    main()
