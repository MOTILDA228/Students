"""Генераторы однотипных задач для уроков-фундамента Димы (уроки 08–27).

Каждый генератор: g(rnd, level) -> dict(q=условие, sol=решение, ans=ответ, check=выражение).
level: 1 — самые простые, 2 — средние, 3 — уровень цели. Все ответы проверяются сборщиком через @check.
"""
from fractions import Fraction as Fr
import math


def num(x):
    """Число для формулы: десятичная запятая {,}, обыкновенная дробь через \\frac."""
    x = Fr(x)
    if x.denominator == 1:
        return str(x.numerator)
    d = x.denominator
    while d % 2 == 0: d //= 2
    while d % 5 == 0: d //= 5
    if d == 1:
        s = f"{float(x):.6f}".rstrip("0").rstrip(".")
        return s.replace(".", "{,}")
    sign = "-" if x < 0 else ""
    return f"{sign}\\frac{{{abs(x.numerator)}}}{{{x.denominator}}}"


def ans(x):
    """Ответ для @ans."""
    x = Fr(x)
    if x.denominator == 1:
        return str(x.numerator)
    d = x.denominator
    while d % 2 == 0: d //= 2
    while d % 5 == 0: d //= 5
    if d == 1:
        return f"{float(x):.6f}".rstrip("0").rstrip(".").replace(".", ",")
    return f"\\({num(x)}\\)"


def M(s):
    return f"\\({s}\\)"


def T(q, sol, a, check):
    return dict(q=q, sol=sol, ans=ans(a), check=check)


# ---------- 08: таблица умножения и деление ----------
def table_mul(r, lv):
    a, b = r.randint(3 if lv > 1 else 2, 9), r.randint(3 if lv > 1 else 2, 9)
    return T(f"Вычислите {M(f'{a}\\cdot{b}')}.", f"{M(f'{a}\\cdot{b} = {a*b}')}.", a * b, f"{a}*{b}")


def table_div(r, lv):
    a, b = r.randint(2, 9), r.randint(3 if lv > 1 else 2, 9)
    p = a * b
    return T(f"Вычислите {M(f'{p} : {a}')}.",
             f"Вспоминаем «семейство»: {M(f'{a}\\cdot{b} = {p}')}, значит {M(f'{p} : {a} = {b}')}.", b, f"{p}//{a}")


def table_missing(r, lv):
    a, b = r.randint(3, 9), r.randint(3, 9)
    return T(f"Какое число пропущено: {M(f'{a}\\cdot\\square = {a*b}')}?",
             f"Пропущенный множитель: {M(f'{a*b} : {a} = {b}')}.", b, f"{a*b}//{a}")


def family(r, lv):
    a, b = r.randint(3, 9), r.randint(3, 9)
    p = a * b
    return T(f"Запишите «семейство» для {M(f'{a}\\cdot{b} = {p}')} и найдите {M(f'{p} : {b}')}.",
             f"{M(f'{a}\\cdot{b} = {p}')}, {M(f'{b}\\cdot{a} = {p}')}, {M(f'{p} : {a} = {b}')}, {M(f'{p} : {b} = {a}')}. Ответ: {a}.",
             a, f"{p}//{b}")


def mul_2digit(r, lv):
    a, b = r.randint(12, 49 if lv > 1 else 25), r.randint(2, 9)
    t, u = a // 10 * 10, a % 10
    return T(f"Вычислите {M(f'{a}\\cdot{b}')}.",
             f"Разбиваем: {M(f'{a}\\cdot{b} = {t}\\cdot{b} + {u}\\cdot{b} = {t*b} + {u*b} = {a*b}')}.", a * b, f"{a}*{b}")


def div_2digit(r, lv):
    b, q = r.randint(2, 9), r.randint(11, 25 if lv > 1 else 15)
    p = b * q
    t = (p // b // 10) * 10 * b
    return T(f"Вычислите {M(f'{p} : {b}')}.",
             f"Разбиваем делимое на удобные части: {M(f'{p} = {t} + {p-t}')}; {M(f'{t} : {b} = {t//b}')}, {M(f'{p-t} : {b} = {(p-t)//b}')}. Ответ: {q}. Проверка: {M(f'{q}\\cdot{b} = {p}')} ✓.",
             q, f"{p}//{b}")


# ---------- 09, 11: сложение и вычитание ----------
def eq_slag(r, lv):
    a, x = r.randint(5, 30 if lv == 1 else 90), r.randint(5, 30 if lv == 1 else 150)
    b = a + x
    if r.random() < .5:
        q = f"x + {a} = {b}"
    else:
        q = f"{a} + x = {b}"
    return T(f"Решите уравнение {M(q)}.",
             f"Неизвестное слагаемое = сумма − известное слагаемое: {M(f'x = {b} - {a} = {x}')}. Проверка: {M(f'{x} + {a} = {b}')} ✓.",
             x, f"{b}-{a}")


def eq_umen(r, lv):
    a, b = r.randint(5, 40 if lv == 1 else 120), r.randint(5, 40 if lv == 1 else 120)
    return T(f"Решите уравнение {M(f'x - {a} = {b}')}.",
             f"Неизвестное уменьшаемое = разность + вычитаемое: {M(f'x = {b} + {a} = {a+b}')}. Проверка: {M(f'{a+b} - {a} = {b}')} ✓.",
             a + b, f"{b}+{a}")


def eq_vych(r, lv):
    b, x = r.randint(5, 40 if lv == 1 else 120), r.randint(5, 40 if lv == 1 else 120)
    a = b + x
    return T(f"Решите уравнение {M(f'{a} - x = {b}')}.",
             f"Неизвестное вычитаемое = уменьшаемое − разность: {M(f'x = {a} - {b} = {x}')}. Проверка: {M(f'{a} - {x} = {b}')} ✓.",
             x, f"{a}-{b}")


def eq_addsub_mix(r, lv):
    return r.choice([eq_slag, eq_umen, eq_vych])(r, lv)


def word_slag(r, lv):
    a, x = r.randint(12, 60), r.randint(8, 50)
    return T(f"Задумали число, прибавили к нему {a} и получили {a+x}. Какое число задумали? (Составьте уравнение {M(f'x + {a} = {a+x}')}.)",
             f"{M(f'x = {a+x} - {a} = {x}')}.", x, f"{a+x}-{a}")


def word_vych(r, lv):
    a, x = r.randint(40, 120), r.randint(5, 35)
    return T(f"В коробке было {a} карандашей. Когда несколько карандашей раздали, осталось {a-x}. Сколько карандашей раздали? (Уравнение {M(f'{a} - x = {a-x}')}.)",
             f"Неизвестное вычитаемое: {M(f'x = {a} - {a-x} = {x}')}.", x, f"{a}-({a-x})")


# ---------- 12, 14: умножение и деление ----------
def eq_mnozh(r, lv):
    a = r.randint(2, 9)
    x = r.randint(2, 9) if lv == 1 else r.randint(11, 30 if lv == 2 else 60)
    b = a * x
    q = f"{a}\\cdot x = {b}" if r.random() < .7 else f"x\\cdot{a} = {b}"
    return T(f"Решите уравнение {M(q)}.",
             f"Неизвестный множитель = произведение : известный множитель: {M(f'x = {b} : {a} = {x}')}. Проверка: {M(f'{a}\\cdot{x} = {b}')} ✓.",
             x, f"{b}//{a}")


def eq_delim(r, lv):
    a = r.randint(2, 9)
    b = r.randint(2, 9) if lv == 1 else r.randint(11, 30)
    return T(f"Решите уравнение {M(f'x : {a} = {b}')}.",
             f"Неизвестное делимое = частное · делитель: {M(f'x = {b}\\cdot{a} = {a*b}')}. Проверка: {M(f'{a*b} : {a} = {b}')} ✓.",
             a * b, f"{b}*{a}")


def eq_delit(r, lv):
    x = r.randint(2, 9)
    b = r.randint(2, 9) if lv == 1 else r.randint(11, 25)
    a = x * b
    return T(f"Решите уравнение {M(f'{a} : x = {b}')}.",
             f"Неизвестный делитель = делимое : частное: {M(f'x = {a} : {b} = {x}')}. Проверка: {M(f'{a} : {x} = {b}')} ✓.",
             x, f"{a}//{b}")


def eq_muldiv_mix(r, lv):
    return r.choice([eq_mnozh, eq_delim, eq_delit])(r, lv)


def eq_all6(r, lv):
    return r.choice([eq_slag, eq_umen, eq_vych, eq_mnozh, eq_delim, eq_delit])(r, lv)


def word_mnozh(r, lv):
    a, x = r.randint(3, 9), r.randint(12, 40)
    return T(f"{a} одинаковых пачек тетрадей содержат {a*x} тетрадей. Сколько тетрадей в одной пачке? (Уравнение {M(f'{a}\\cdot x = {a*x}')}.)",
             f"Неизвестный множитель: {M(f'x = {a*x} : {a} = {x}')}.", x, f"{a*x}//{a}")


def word_delim(r, lv):
    a, b = r.randint(3, 8), r.randint(6, 25)
    return T(f"Конфеты разложили поровну в {a} пакетов, в каждом оказалось {b} конфет. Сколько было конфет? (Уравнение {M(f'x : {a} = {b}')}.)",
             f"Неизвестное делимое: {M(f'x = {b}\\cdot{a} = {a*b}')}.", a * b, f"{b}*{a}")


# ---------- 15: деление столбиком ----------
def long_div(r, lv):
    d = r.randint(2, 9)
    q = r.randint(100, 400) if lv < 3 else r.randint(100, 999)
    if lv == 1:
        q = r.choice([x for x in range(100, 400) if all(int(c) * d < 10 or True for c in str(x))])
    p = d * q
    steps, rem, out = [], 0, []
    for ch in str(p):
        cur = rem * 10 + int(ch)
        if cur < d and not out:
            rem = cur
            continue
        out.append(str(cur // d))
        steps.append(M(f"{cur} : {d} = {cur//d}") + (f" (остаток {cur % d})" if cur % d else ""))
        rem = cur % d
    return T(f"Вычислите столбиком {M(f'{p} : {d}')}.",
             "По шагам: " + "; ".join(steps) + f". Ответ: {q}. Проверка: {M(f'{q}\\cdot{d} = {p}')} ✓.",
             q, f"{p}//{d}")


def long_div_zero(r, lv):
    d = r.randint(2, 9)
    q = r.choice([x for x in range(101, 999) if '0' in str(x)[1:]])
    p = d * q
    return T(f"Вычислите {M(f'{p} : {d}')}. Осторожно: в частном будет ноль.",
             f"Если очередное число меньше делителя, пишем в частном 0 и сносим следующую цифру. Ответ: {q}. Проверка: {M(f'{q}\\cdot{d} = {p}')} ✓.",
             q, f"{p}//{d}")


def long_div_2(r, lv):
    d = r.randint(11, 25)
    q = r.randint(12, 48)
    p = d * q
    return T(f"Вычислите {M(f'{p} : {d}')}.",
             f"Подбираем цифры частного прикидкой: {M(f'{d}\\cdot{q//10*10} = {d*(q//10*10)}')}, остаётся {p - d*(q//10*10)}, {M(f'{p - d*(q//10*10)} : {d} = {q%10}')}. Ответ: {q}.",
             q, f"{p}//{d}")


def mul_column(r, lv):
    a, b = r.randint(100, 900), r.randint(2, 9)
    return T(f"Вычислите столбиком {M(f'{a}\\cdot{b}')}.",
             f"{M(f'{a}\\cdot{b} = {a*b}')} (умножаем справа налево, переносим десятки).", a * b, f"{a}*{b}")


# ---------- 17: порядок действий ----------
def order1(r, lv):
    a, b, c = r.randint(20, 60), r.randint(2, 6), r.randint(2, 6)
    if r.random() < .5:
        return T(f"Вычислите {M(f'{a} - {b}\\cdot{c}')}.", f"Сначала умножение: {M(f'{b}\\cdot{c} = {b*c}')}; потом {M(f'{a} - {b*c} = {a-b*c}')}.", a - b * c, f"{a}-{b}*{c}")
    return T(f"Вычислите {M(f'{a} + {b}\\cdot{c}')}.", f"Сначала умножение: {b*c}; потом {M(f'{a} + {b*c} = {a+b*c}')}.", a + b * c, f"{a}+{b}*{c}")


def order_br(r, lv):
    b, c = r.randint(2, 15), r.randint(2, 6)
    a = b + r.randint(2, 12)
    return T(f"Вычислите {M(f'({a} - {b})\\cdot{c}')}.", f"Сначала скобки: {M(f'{a} - {b} = {a-b}')}; потом {M(f'{a-b}\\cdot{c} = {(a-b)*c}')}.", (a - b) * c, f"({a}-{b})*{c}")


def order2(r, lv):
    b, q1 = r.randint(2, 9), r.randint(2, 9)
    a = b * q1
    c, d = r.randint(2, 9), r.randint(2, 9)
    return T(f"Вычислите {M(f'{a} : {b} + {c}\\cdot{d}')}.",
             f"Сначала деление и умножение: {M(f'{a} : {b} = {q1}')}, {M(f'{c}\\cdot{d} = {c*d}')}; потом сложение: {q1 + c*d}.", q1 + c * d, f"{a}//{b}+{c}*{d}")


def order3(r, lv):
    a, b, c, d = r.randint(30, 90), r.randint(2, 9), r.randint(10, 30), r.randint(2, 9)
    while a - c <= 0: a += 10
    res = (a - c) * b - d * b
    return T(f"Вычислите {M(f'({a} - {c})\\cdot{b} - {d}\\cdot{b}')}.",
             f"Скобки: {a-c}; умножения: {M(f'{a-c}\\cdot{b} = {(a-c)*b}')}, {M(f'{d}\\cdot{b} = {d*b}')}; вычитание: {res}.", res, f"({a}-{c})*{b}-{d}*{b}")


def order_left(r, lv):
    a, b, c = r.randint(40, 90), r.randint(5, 20), r.randint(3, 15)
    return T(f"Вычислите {M(f'{a} - {b} + {c}')}.", f"Сложение и вычитание — по порядку слева направо: {M(f'{a} - {b} = {a-b}')}, {M(f'{a-b} + {c} = {a-b+c}')}.", a - b + c, f"{a}-{b}+{c}")


def order_mix(r, lv):
    return r.choice([order1, order_br, order2, order3, order_left])(r, lv)


# ---------- 18: уравнения в два шага ----------
def eq2_plus(r, lv):
    a, x = r.randint(2, 9), r.randint(2, 15 if lv < 3 else 30)
    b = r.randint(1, 30)
    c = a * x + b
    return T(f"Решите уравнение {M(f'{a}x + {b} = {c}')}.",
             f"Шаг 1 — «отцепляем» {b} (неизвестное слагаемое): {M(f'{a}x = {c} - {b} = {c-b}')}. Шаг 2 — неизвестный множитель: {M(f'x = {c-b} : {a} = {x}')}. Проверка: {M(f'{a}\\cdot{x} + {b} = {c}')} ✓.",
             x, f"({c}-{b})//{a}")


def eq2_minus(r, lv):
    a, x = r.randint(2, 9), r.randint(2, 15 if lv < 3 else 30)
    b = r.randint(1, 30)
    c = a * x - b
    return T(f"Решите уравнение {M(f'{a}x - {b} = {c}')}.",
             f"Шаг 1 — неизвестное уменьшаемое: {M(f'{a}x = {c} + {b} = {c+b}')}. Шаг 2 — неизвестный множитель: {M(f'x = {c+b} : {a} = {x}')}. Проверка: {M(f'{a}\\cdot{x} - {b} = {c}')} ✓.",
             x, f"({c}+{b})//{a}")


def eq2_bracket(r, lv):
    a, x, b = r.randint(2, 9), r.randint(1, 20), r.randint(1, 15)
    c = a * (x + b)
    return T(f"Решите уравнение {M(f'{a}(x + {b}) = {c}')}.",
             f"Шаг 1 — скобка — неизвестный множитель: {M(f'x + {b} = {c} : {a} = {x+b}')}. Шаг 2 — неизвестное слагаемое: {M(f'x = {x+b} - {b} = {x}')}.",
             x, f"{c}//{a}-{b}")


def eq2_div(r, lv):
    a, q, b = r.randint(2, 6), r.randint(2, 12), r.randint(1, 20)
    x = a * q
    c = q + b
    return T(f"Решите уравнение {M(f'x : {a} + {b} = {c}')}.",
             f"Шаг 1: {M(f'x : {a} = {c} - {b} = {q}')}. Шаг 2 — неизвестное делимое: {M(f'x = {q}\\cdot{a} = {x}')}.",
             x, f"({c}-{b})*{a}")


def eq2_mix(r, lv):
    return r.choice([eq2_plus, eq2_minus, eq2_bracket, eq2_div])(r, lv)


def word_eq2(r, lv):
    a, x, b = r.randint(3, 6), r.randint(20, 60), r.randint(20, 90)
    return T(f"Купили {a} одинаковых тетради и ручку за {b} руб. Всего заплатили {a*x+b} руб. Сколько стоит тетрадь? (Уравнение {M(f'{a}x + {b} = {a*x+b}')}.)",
             f"{M(f'{a}x = {a*x+b} - {b} = {a*x}')}, {M(f'x = {a*x} : {a} = {x}')} руб.", x, f"({a*x+b}-{b})//{a}")


# ---------- 20: делимость ----------
def div_test(r, lv):
    k = r.choice([2, 3, 5, 9, 10])
    n = r.randint(100, 9999)
    if r.random() < .5: n -= n % k
    yes = n % k == 0
    rule = {2: "последняя цифра чётная", 5: "последняя цифра 0 или 5", 10: "последняя цифра 0",
            3: f"сумма цифр ({sum(map(int, str(n)))}) делится на 3", 9: f"сумма цифр ({sum(map(int, str(n)))}) делится на 9"}[k]
    return T(f"Делится ли число {n} на {k}? Ответ: 1 — да, 0 — нет.",
             f"Признак: {rule}. {'Выполняется' if yes else 'Не выполняется'} → {1 if yes else 0}.", 1 if yes else 0, f"int({n}%{k}==0)")


def gcd_t(r, lv):
    g = r.randint(2, 12)
    a, b = g * r.randint(2, 7), g * r.randint(2, 7)
    while math.gcd(a, b) != g or a == b: a, b = g * r.randint(2, 9), g * r.randint(2, 9)
    return T(f"Найдите НОД чисел {a} и {b}.", f"Наибольшее число, на которое делятся оба: {math.gcd(a,b)} ({M(f'{a} = {g}\\cdot{a//g}')}, {M(f'{b} = {g}\\cdot{b//g}')}).",
             math.gcd(a, b), f"math.gcd({a},{b})")


def lcm_t(r, lv):
    a, b = r.choice([(4, 6), (6, 8), (6, 9), (8, 12), (10, 15), (4, 10), (9, 12), (12, 18), (6, 10), (5, 6), (3, 8), (14, 21)])
    l = a * b // math.gcd(a, b)
    return T(f"Найдите НОК чисел {a} и {b} (наименьший общий знаменатель для дробей со знаменателями {a} и {b}).",
             f"Перебираем числа, кратные {max(a,b)}: {', '.join(str(max(a,b)*i) for i in range(1, l//max(a,b)+1))} — первое, которое делится на {min(a,b)}: {l}.",
             l, f"{a}*{b}//math.gcd({a},{b})")


def factor_t(r, lv):
    n = r.choice([12, 18, 20, 24, 28, 30, 36, 40, 42, 45, 48, 50, 54, 60, 72, 84, 90])
    f, m, p = [], n, 2
    while m > 1:
        while m % p == 0: f.append(p); m //= p
        p += 1
    return T(f"Разложите число {n} на простые множители. В ответ запишите самый большой простой множитель.",
             f"{M(f'{n} = ' + '\\cdot'.join(map(str, f)))}. Наибольший: {max(f)}.", max(f), f"max(p for p in range(2,{n}+1) if {n}%p==0 and all(p%k for k in range(2,p)))")


# ---------- 21, 23: дроби ----------
def fr_reduce(r, lv):
    a, b = r.randint(1, 8), r.randint(2, 9)
    while a >= b or math.gcd(a, b) != 1: a, b = r.randint(1, 8), r.randint(2, 9)
    k = r.randint(2, 6)
    return T(f"Сократите дробь {M(f'\\frac{{{a*k}}}{{{b*k}}}')}.",
             f"Числитель и знаменатель делятся на {k}: {M(f'\\frac{{{a*k}}}{{{b*k}}} = \\frac{{{a}}}{{{b}}}')}.", Fr(a, b), f"F({a*k},{b*k})")


def fr_part(r, lv):
    b = r.randint(2, 9); a = r.randint(1, b - 1); n = b * r.randint(2, 12)
    return T(f"Найдите {M(f'\\frac{{{a}}}{{{b}}}')} от числа {n}.",
             f"Одна {b}-я часть: {M(f'{n} : {b} = {n//b}')}; {a} таких частей: {M(f'{n//b}\\cdot{a} = {n//b*a}')}.", Fr(a, b) * n, f"F({a},{b})*{n}")


def fr_add_same(r, lv):
    b = r.randint(5, 15); a1, a2 = r.randint(1, b // 2), r.randint(1, b // 2)
    s = Fr(a1 + a2, b)
    tail = f" {M(f'= {num(s)}')}" if s.denominator != b else ""
    return T(f"Вычислите {M(f'\\frac{{{a1}}}{{{b}}} + \\frac{{{a2}}}{{{b}}}')}.",
             f"Знаменатели одинаковые — складываем числители: {M(f'\\frac{{{a1+a2}}}{{{b}}}')}{tail}.", s, f"F({a1},{b})+F({a2},{b})")


def fr_add(r, lv, sub=False):
    pairs = [(2, 3), (3, 4), (2, 5), (4, 6), (3, 6), (2, 4), (5, 10), (4, 5), (6, 8), (3, 9), (4, 12), (6, 9), (8, 12), (10, 15)]
    b1, b2 = r.choice(pairs)
    a1, a2 = r.randint(1, b1 - 1), r.randint(1, b2 - 1)
    if sub and Fr(a1, b1) <= Fr(a2, b2): a1, b1, a2, b2 = a2, b2, a1, b1
    if sub and Fr(a1, b1) == Fr(a2, b2): a1, a2 = b1 - 1 if b1 > 2 else 1, 1
    if sub and Fr(a1, b1) <= Fr(a2, b2): return fr_add(r, lv, sub)
    L = b1 * b2 // math.gcd(b1, b2)
    n1, n2 = a1 * L // b1, a2 * L // b2
    op = "-" if sub else "+"
    res = Fr(a1, b1) - Fr(a2, b2) if sub else Fr(a1, b1) + Fr(a2, b2)
    raw = n1 - n2 if sub else n1 + n2
    tail = f" {M(f'= {num(res)}')}" if res.denominator != L else ""
    return T(f"Вычислите {M(f'\\frac{{{a1}}}{{{b1}}} {op} \\frac{{{a2}}}{{{b2}}}')}.",
             f"Шаг 1 — общий знаменатель {L}. Шаг 2 — доп. множители: {L//b1} и {L//b2}. Шаг 3: {M(f'\\frac{{{n1}}}{{{L}}} {op} \\frac{{{n2}}}{{{L}}} = \\frac{{{raw}}}{{{L}}}')}{tail}.",
             res, f"F({a1},{b1}){op}F({a2},{b2})")


def fr_sub(r, lv):
    return fr_add(r, lv, sub=True)


def fr_mul(r, lv):
    a1, b1, a2, b2 = r.randint(1, 9), r.randint(2, 9), r.randint(1, 9), r.randint(2, 9)
    res = Fr(a1, b1) * Fr(a2, b2)
    return T(f"Вычислите {M(f'\\frac{{{a1}}}{{{b1}}}\\cdot\\frac{{{a2}}}{{{b2}}}')}.",
             f"Числитель на числитель, знаменатель на знаменатель (сначала сокращаем крест-накрест): {M(f'\\frac{{{a1}\\cdot{a2}}}{{{b1}\\cdot{b2}}} = {num(res)}')}.", res, f"F({a1},{b1})*F({a2},{b2})")


def fr_div(r, lv):
    a1, b1, a2, b2 = r.randint(1, 9), r.randint(2, 9), r.randint(1, 9), r.randint(2, 9)
    res = Fr(a1, b1) / Fr(a2, b2)
    return T(f"Вычислите {M(f'\\frac{{{a1}}}{{{b1}}} : \\frac{{{a2}}}{{{b2}}}')}.",
             f"Деление = умножение на перевёрнутую дробь: {M(f'\\frac{{{a1}}}{{{b1}}}\\cdot\\frac{{{b2}}}{{{a2}}} = {num(res)}')}.", res, f"F({a1},{b1})/F({a2},{b2})")


def fr_mixed(r, lv):
    w, b = r.randint(1, 5), r.randint(2, 9); a = r.randint(1, b - 1)
    k = r.randint(2, 6)
    res = (w + Fr(a, b)) * k
    return T(f"Вычислите {M(f'{w}\\frac{{{a}}}{{{b}}}\\cdot{k}')}.",
             f"Шаг 1 — в неправильную дробь: {M(f'{w}\\frac{{{a}}}{{{b}}} = \\frac{{{w}\\cdot{b} + {a}}}{{{b}}} = \\frac{{{w*b+a}}}{{{b}}}')}. Шаг 2: {M(f'\\frac{{{w*b+a}}}{{{b}}}\\cdot{k} = {num(res)}')}.",
             res, f"(F({w*b+a},{b}))*{k}")


def fr_to_improper(r, lv):
    w, b = r.randint(1, 7), r.randint(2, 9); a = r.randint(1, b - 1)
    return T(f"Запишите {M(f'{w}\\frac{{{a}}}{{{b}}}')} в виде неправильной дроби. В ответ — числитель.",
             f"Целую часть умножаем на знаменатель и прибавляем числитель: {M(f'{w}\\cdot{b} + {a} = {w*b+a}')}. Дробь {M(f'\\frac{{{w*b+a}}}{{{b}}}')}.",
             w * b + a, f"{w}*{b}+{a}")


# ---------- 24, 25: десятичные ----------
def d(x):
    return num(Fr(x).limit_denominator(1000))


def dec_add(r, lv):
    a, b = Fr(r.randint(11, 999), 100), Fr(r.randint(11, 999), 10 if r.random() < .5 else 100)
    return T(f"Вычислите {M(f'{d(a)} + {d(b)}')}.", f"Запятая под запятой, недостающие разряды — нули: {M(f'{d(a+b)}')}.", a + b, f"F('{float(a)}')+F('{float(b)}')")


def dec_sub(r, lv):
    a, b = Fr(r.randint(200, 999), 100), Fr(r.randint(11, 199), 10 if r.random() < .5 else 100)
    return T(f"Вычислите {M(f'{d(a)} - {d(b)}')}.", f"Запятая под запятой: {M(f'{d(a-b)}')}.", a - b, f"F('{float(a)}')-F('{float(b)}')")


def dec_mul_int(r, lv):
    a, k = Fr(r.randint(2, 99), 10 if r.random() < .6 else 100), r.randint(2, 9)
    digits = 1 if a.denominator == 10 or (a * 10).denominator == 1 else 2
    return T(f"Вычислите {M(f'{d(a)}\\cdot{k}')}.",
             f"Умножаем как целые, потом отделяем запятой столько цифр, сколько после запятой в множителе: {M(f'{d(a)}\\cdot{k} = {d(a*k)}')}.", a * k, f"F('{float(a)}')*{k}")


def dec_mul(r, lv):
    a, b = Fr(r.randint(2, 30), 10), Fr(r.randint(2, 30), 10)
    return T(f"Вычислите {M(f'{d(a)}\\cdot{d(b)}')}.",
             f"Умножаем без запятых, в ответе после запятой столько цифр, сколько у обоих множителей вместе: {M(f'{d(a*b)}')}.", a * b, f"F('{float(a)}')*F('{float(b)}')")


def dec_mul10(r, lv):
    a, p = Fr(r.randint(11, 9999), 1000), r.choice([10, 100, 1000])
    if r.random() < .5:
        return T(f"Вычислите {M(f'{d(a)}\\cdot{p}')}.", f"Умножить на {p} — перенести запятую вправо на {len(str(p))-1}: {M(d(a*p))}.", a * p, f"F('{float(a)}')*{p}")
    return T(f"Вычислите {M(f'{d(a)} : {p}')}.", f"Разделить на {p} — перенести запятую влево на {len(str(p))-1}: {M(d(a/p))}.", a / p, f"F('{float(a)}')/{p}")


def dec_div_int(r, lv):
    k, q = r.randint(2, 9), Fr(r.randint(11, 99), 10 if r.random() < .6 else 100)
    a = q * k
    return T(f"Вычислите {M(f'{d(a)} : {k}')}.", f"Делим как обычно; запятую в частном ставим, когда «перешли» запятую в делимом: {M(d(q))}. Проверка: {M(f'{d(q)}\\cdot{k} = {d(a)}')} ✓.", q, f"F('{float(a)}')/{k}")


def dec_div_dec(r, lv):
    b = Fr(r.randint(2, 9), 10 if r.random() < .7 else 100)
    q = r.randint(2, 30)
    a = b * q
    sh = 1 if b.denominator == 10 else 2
    return T(f"Вычислите {M(f'{d(a)} : {d(b)}')}.",
             f"Переносим запятую в обоих числах вправо на {sh}, чтобы делитель стал целым: {M(f'{d(a*10**sh)} : {d(b*10**sh)} = {q}')}.", q, f"F('{float(a)}')/F('{float(b)}')")


def fr_to_dec(r, lv):
    a, b = r.choice([(1, 2), (1, 4), (3, 4), (1, 5), (2, 5), (3, 5), (4, 5), (1, 8), (3, 8), (7, 20), (9, 25), (3, 50), (7, 10), (13, 20)])
    return T(f"Запишите {M(f'\\frac{{{a}}}{{{b}}}')} десятичной дробью.",
             f"Домножаем знаменатель до 10, 100 или 1000 (или делим {a} на {b}): {M(d(Fr(a,b)))}.", Fr(a, b), f"F({a},{b})")


def dec_mixed(r, lv):
    a, b, c = Fr(r.randint(11, 60), 10), Fr(r.randint(2, 9), 10), Fr(r.randint(1, 20), 10)
    res = a * b + c
    return T(f"Вычислите {M(f'{d(a)}\\cdot{d(b)} + {d(c)}')}.", f"Сначала умножение: {M(d(a*b))}; потом сложение: {M(d(res))}.", res, f"F('{float(a)}')*F('{float(b)}')+F('{float(c)}')")


# ---------- геометрия (числа) ----------
def ang_adj(r, lv):
    a = r.randint(20, 160)
    return T(f"Один из смежных углов равен {M(f'{a}^\\circ')}. Найдите другой.", f"Смежные в сумме {M('180^\\circ')}: {M(f'180 - {a} = {180-a}^\\circ')}.", 180 - a, f"180-{a}")


def ang_vert(r, lv):
    a = r.randint(20, 160)
    return T(f"Один из вертикальных углов равен {M(f'{a}^\\circ')}. Найдите другой.", f"Вертикальные углы равны: {M(f'{a}^\\circ')}.", a, f"{a}")


def ang_tri(r, lv):
    a, b = r.randint(20, 80), r.randint(20, 80)
    return T(f"В треугольнике два угла {M(f'{a}^\\circ')} и {M(f'{b}^\\circ')}. Найдите третий.", f"{M(f'180 - {a} - {b} = {180-a-b}^\\circ')}.", 180 - a - b, f"180-{a}-{b}")


def ang_right(r, lv):
    a = r.randint(15, 75)
    return T(f"В прямоугольном треугольнике один острый угол {M(f'{a}^\\circ')}. Найдите другой острый угол.", f"Сумма острых углов {M('90^\\circ')}: {M(f'90 - {a} = {90-a}^\\circ')}.", 90 - a, f"90-{a}")


def ang_iso_base(r, lv):
    v = r.randrange(20, 160, 2)
    return T(f"В равнобедренном треугольнике угол при вершине {M(f'{v}^\\circ')}. Найдите угол при основании.", f"Углы при основании равны: {M(f'(180 - {v}) : 2 = {(180-v)//2}^\\circ')}.", (180 - v) // 2, f"(180-{v})//2")


def ang_iso_top(r, lv):
    b = r.randint(20, 85)
    return T(f"В равнобедренном треугольнике угол при основании {M(f'{b}^\\circ')}. Найдите угол при вершине.", f"{M(f'180 - 2\\cdot{b} = {180-2*b}^\\circ')}.", 180 - 2 * b, f"180-2*{b}")


def ang_ext(r, lv):
    a, b = r.randint(20, 80), r.randint(20, 80)
    return T(f"В треугольнике \\(ABC\\) \\(\\angle A = {a}^\\circ\\), \\(\\angle B = {b}^\\circ\\). Найдите угол, смежный с углом \\(C\\).",
             f"\\(\\angle C = 180 - {a} - {b} = {180-a-b}^\\circ\\); смежный: {M(f'180 - {180-a-b} = {a+b}^\\circ')}.", a + b, f"180-(180-{a}-{b})")


def tri_kind(r, lv):
    a, b = r.randint(15, 100), r.randint(15, 70)
    c = 180 - a - b
    while c <= 0 or c == 90 and r.random() < .7:
        a, b = r.randint(15, 100), r.randint(15, 70); c = 180 - a - b
    mx = max(a, b, c)
    k = 1 if mx < 90 else (2 if mx == 90 else 3)
    name = {1: "остроугольный", 2: "прямоугольный", 3: "тупоугольный"}[k]
    return T(f"Два угла треугольника {M(f'{a}^\\circ')} и {M(f'{b}^\\circ')}. Какой это треугольник? 1 — остроугольный, 2 — прямоугольный, 3 — тупоугольный.",
             f"Третий угол {M(f'{c}^\\circ')}. Наибольший угол {mx}° → {name}.", k, f"(lambda m: 1 if m<90 else (2 if m==90 else 3))(max({a},{b},180-{a}-{b}))")


def perim_rect(r, lv):
    a, b = r.randint(2, 15), r.randint(2, 15)
    if r.random() < .5:
        return T(f"Стороны прямоугольника {a} см и {b} см. Найдите периметр.", f"{M(f'P = 2\\cdot({a} + {b}) = {2*(a+b)}')} см.", 2 * (a + b), f"2*({a}+{b})")
    return T(f"Стороны прямоугольника {a} см и {b} см. Найдите площадь.", f"{M(f'S = {a}\\cdot{b} = {a*b}')} см².", a * b, f"{a}*{b}")


def rect_back(r, lv):
    a, b = r.randint(2, 12), r.randint(2, 12)
    return T(f"Площадь прямоугольника {a*b} см², одна сторона {a} см. Найдите другую сторону.", f"Неизвестный множитель: {M(f'{a*b} : {a} = {b}')} см.", b, f"{a*b}//{a}")


# ---------- клетчатая бумага (с рисунком) ----------
def G(q, sol, a, check, fig):
    t = T(q, sol, a, check); t["fig"] = fig; return t


def grid_rect(r, lv):
    a, b = r.randint(2, 7), r.randint(2, 5)
    x, y = r.randint(1, 2), 1
    fig = f"@fig grid={x+a+1}x{y+b+1}\npoly {x},{y} {x+a},{y} {x+a},{y+b} {x},{y+b} fill\n@end"
    if r.random() < .5:
        return G("На клетчатой бумаге с клеткой \\(1\\times1\\) изображён прямоугольник. Найдите его площадь.",
                 f"Считаем клетки: длина {a}, ширина {b}. {M(f'S = {a}\\cdot{b} = {a*b}')}.", a * b, f"area(({x},{y}),({x+a},{y}),({x+a},{y+b}),({x},{y+b}))", fig)
    return G("На клетчатой бумаге с клеткой \\(1\\times1\\) изображён прямоугольник. Найдите его периметр.",
             f"Длина {a}, ширина {b}: {M(f'P = 2\\cdot({a} + {b}) = {2*(a+b)}')}.", 2 * (a + b), f"2*({a}+{b})", fig)


def grid_seg(r, lv):
    a = r.randint(2, 9)
    if r.random() < .5:
        fig = f"@fig grid={a+2}x3\nP A 1 1 dot\nP B {a+1} 1 dot\nseg A B\n@end"
    else:
        fig = f"@fig grid=3x{a+2}\nP A 1 1 dot\nP B 1 {a+1} dot\nseg A B\n@end"
    return G("Найдите длину отрезка \\(AB\\) (клетка \\(1\\times1\\)).", f"Отрезок идёт по линии сетки — считаем клетки: {a}.", a, f"{a}", fig)


def grid_right_tri(r, lv):
    a, b = r.randint(2, 7), r.randint(2, 5)
    fig = f"@fig grid={a+2}x{b+2}\npoly 1,1 {a+1},1 1,{b+1} fill\n@end"
    return G("Найдите площадь прямоугольного треугольника на клетчатой бумаге (клетка \\(1\\times1\\)).",
             f"Это половина прямоугольника {a}×{b}: {M(f'S = \\frac{{{a}\\cdot{b}}}{{2}} = {num(Fr(a*b,2))}')}.", Fr(a * b, 2), f"area((1,1),({a+1},1),(1,{b+1}))", fig)


def grid_tri(r, lv):
    a, h = r.randint(3, 8), r.randint(2, 5)
    t = r.randint(0, a + 1)
    fig = f"@fig grid={max(a,t)+2}x{h+2}\npoly 1,1 {a+1},1 {t+1},{h+1} fill\n@end"
    return G("Найдите площадь треугольника на клетчатой бумаге (клетка \\(1\\times1\\)).",
             f"Основание (по нижней линии) {a}, высота {h}: {M(f'S = \\frac{{{a}\\cdot{h}}}{{2}} = {num(Fr(a*h,2))}')}.", Fr(a * h, 2), f"area((1,1),({a+1},1),({t+1},{h+1}))", fig)


def grid_lshape(r, lv):
    a, b = r.randint(4, 7), r.randint(3, 5)
    c, e = r.randint(1, a - 2), r.randint(1, b - 1)
    fig = f"@fig grid={a+2}x{b+2}\npoly 1,1 {a+1},1 {a+1},{1+e} {1+c},{1+e} {1+c},{b+1} 1,{b+1} fill\n@end"
    S = a * e + c * (b - e)
    return G("Найдите площадь фигуры на клетчатой бумаге (клетка \\(1\\times1\\)).",
             f"Разрезаем на два прямоугольника: {M(f'{a}\\cdot{e} + {c}\\cdot{b-e} = {S}')}.", S, f"area((1,1),({a+1},1),({a+1},{1+e}),({1+c},{1+e}),({1+c},{b+1}),(1,{b+1}))", fig)


GEN = {k: v for k, v in globals().items() if callable(v) and not k.startswith("_") and k not in ("num", "ans", "M", "T", "G", "d", "Fr")}
