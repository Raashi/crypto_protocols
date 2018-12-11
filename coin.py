from utils import *
from prime import gen_diffie


def gen_pq(q_size):
    """Алиса"""
    p, q = gen_diffie(q_size)
    write('p.txt', p)


def gen_ht(p):
    """Боб"""
    h = primitive(p)
    t = primitive(p)
    write('h.txt', h)
    write('t.txt', t)


def gen_y(p, h, t):
    """Алиса"""
    if not is_primitive(p, h):
        print('ОШИБКА: h - не примитивный элемент в GF(p)')
        return
    if not is_primitive(p, t):
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
        gen_ht(read('p.txt'))
    if op == '-gy' or op == 'debug':
        gen_y(*read_mul('p.txt', 'h.txt', 't.txt'))
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
