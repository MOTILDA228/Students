"""Генераторы для уроков 28–70 Димы (задания ОГЭ на «3»). Формат как в tasks.py."""
from fractions import Fraction as Fr
import math
from tasks import num, ans, M, T, G as GF, d

CD, DG = "\\cdot", "^\\circ"


def p(x):
    """Отрицательное число в скобках."""
    return f"({num(x)})" if Fr(x) < 0 else num(x)


# ---------- 28, 29: отрицательные числа ----------
def neg_add(r, lv):
    a, b = r.randint(-30, 30), r.randint(-30, 30)
    while a >= 0 and b >= 0: a = -r.randint(1, 30)
    if a < 0 and b < 0:
        why = f"Оба отрицательные: складываем «долги» и ставим минус: {M(f'-({abs(a)} + {abs(b)}) = {a+b}')}."
    else:
        why = f"Знаки разные: из большего модуля вычитаем меньший, знак — как у числа с большим модулем: {M(f'{a} + {p(b)} = {a+b}')}."
    return T(f"Вычислите {M(f'{a} + {p(b)}')}.", why, a + b, f"{a}+({b})")


def neg_sub(r, lv):
    a, b = r.randint(-30, 30), r.randint(-30, 30)
    if b >= 0 and r.random() < .5: b = -b - 1
    return T(f"Вычислите {M(f'{a} - {p(b)}')}.",
             f"Вычитание — это прибавление противоположного: {M(f'{a} - {p(b)} = {a} + {p(-b)} = {a-b}')}.", a - b, f"{a}-({b})")


def neg_addsub(r, lv):
    return (neg_add if r.random() < .5 else neg_sub)(r, lv)


def neg_mul(r, lv):
    a, b = r.randint(-12, 12) or 3, r.randint(-12, 12) or -4
    if a > 0 and b > 0: a = -a
    sign = "«+»" if a * b > 0 else "«−»"
    return T(f"Вычислите {M(f'{a}{CD}{p(b)}')}.",
             f"Знаки {'одинаковые' if (a<0)==(b<0) else 'разные'} → результат {sign}: {M(f'{a}{CD}{p(b)} = {a*b}')}.", a * b, f"{a}*({b})")


def neg_div(r, lv):
    b, q = r.choice([-9, -8, -7, -6, -5, -4, -3, -2, 2, 3, 4, 5, 6, 7, 8, 9]), r.randint(-12, 12) or -5
    a = b * q
    return T(f"Вычислите {M(f'{a} : {p(b)}')}.",
             f"Знаки {'одинаковые → «+»' if (a<0)==(b<0) else 'разные → «−»'}: {M(f'{a} : {p(b)} = {q}')}.", q, f"F({a},{b})")


def neg_expr(r, lv):
    a, b, c = r.randint(2, 9), -r.randint(2, 9), r.randint(-20, 20)
    res = a * b + c
    return T(f"Вычислите {M(f'{a}{CD}{p(b)} + {p(c)}')}.",
             f"Сначала умножение: {M(f'{a}{CD}{p(b)} = {a*b}')}; потом {M(f'{a*b} + {p(c)} = {res}')}.", res, f"{a}*({b})+({c})")


def neg_power(r, lv):
    a, n = r.randint(2, 5), r.choice([2, 3])
    if r.random() < .5:
        return T(f"Вычислите {M(f'(-{a})^{n}')}.",
                 f"Минус в скобках возводится: {M(f'(-{a})^{n} = {(-a)**n}')} ({'чётная степень — плюс' if n % 2 == 0 else 'нечётная — минус'}).", (-a) ** n, f"(-{a})**{n}")
    return T(f"Вычислите {M(f'-{a}^{n}')}.", f"Без скобок минус НЕ возводится: {M(f'-{a}^{n} = -{a**n}')}.", -a ** n, f"-({a}**{n})")


def neg_dec(r, lv):
    a, b = Fr(-r.randint(11, 99), 10), Fr(r.randint(11, 99), 10)
    if r.random() < .5:
        return T(f"Вычислите {M(f'{d(a)} + {d(b)}')}.", f"Знаки разные — вычитаем модули: {M(d(a + b))}.", a + b, f"F('{float(a)}')+F('{float(b)}')")
    return T(f"Вычислите {M(f'{d(a)} - {d(b)}')}.", f"Оба «долга» складываются: {M(d(a - b))}.", a - b, f"F('{float(a)}')-F('{float(b)}')")


def neg_oge6(r, lv):
    a = Fr(-r.randint(1, 9), 10)
    x = -10
    k, m = r.randint(1, 5), r.randint(10, 90)
    res = a * x ** 3 + k * x ** 2 - m
    return T(f"Найдите значение выражения {M(f'{d(a)}{CD}(-10)^3 + {k}{CD}(-10)^2 - {m}')}.",
             f"\\((-10)^3 = -1000\\), \\((-10)^2 = 100\\): {M(f'{d(a*-1000)} + {k*100} - {m} = {num(res)}')}.", res, f"F('{float(a)}')*(-10)**3+{k}*(-10)**2-{m}")


# ---------- 30: Пифагор ----------
TRIPLES = [(3, 4, 5), (6, 8, 10), (5, 12, 13), (8, 15, 17), (9, 12, 15), (12, 16, 20), (7, 24, 25), (20, 21, 29), (9, 40, 41), (15, 20, 25), (10, 24, 26), (12, 35, 37)]


def pyth_hyp(r, lv):
    a, b, c = r.choice(TRIPLES[:6] if lv == 1 else TRIPLES)
    return T(f"Катеты прямоугольного треугольника равны {a} и {b}. Найдите гипотенузу.",
             f"\\(c^2 = {a}^2 + {b}^2 = {a*a} + {b*b} = {c*c}\\), \\(c = \\sqrt{{{c*c}}} = {c}\\).", c, f"hyp({a},{b})")


def pyth_leg(r, lv):
    a, b, c = r.choice(TRIPLES[:6] if lv == 1 else TRIPLES)
    return T(f"Гипотенуза прямоугольного треугольника равна {c}, один катет {a}. Найдите другой катет.",
             f"\\(b^2 = {c}^2 - {a}^2 = {c*c} - {a*a} = {b*b}\\), \\(b = {b}\\).", b, f"leg({c},{a})")


def squares(r, lv):
    n = r.randint(4, 20)
    if r.random() < .5:
        return T(f"Вычислите {M(f'{n}^2')}.", f"{M(f'{n}{CD}{n} = {n*n}')}.", n * n, f"{n}**2")
    return T(f"Вычислите {M(f'\\sqrt{{{n*n}}}')}.", f"Какое число в квадрате даёт {n*n}? {M(f'{n}^2 = {n*n}')} → {n}.", n, f"sqrt({n*n})")


def grid_pyth(r, lv):
    a, b, c = r.choice([(3, 4, 5), (6, 8, 10), (5, 12, 13), (8, 6, 10), (4, 3, 5)])
    fig = f"@fig grid={a+2}x{b+2}\nP A 1 1 dot\nP B {a+1} {b+1} dot\nseg A B\n@end"
    return GF("Найдите длину отрезка \\(AB\\) на клетчатой бумаге (клетка \\(1\\times1\\)).",
              f"Достраиваем прямоугольный треугольник: катеты {a} и {b} клеток. \\(AB = \\sqrt{{{a*a} + {b*b}}} = {c}\\).", c, f"hyp({a},{b})", fig)


def rect_diag(r, lv):
    a, b, c = r.choice(TRIPLES)
    return T(f"Стороны прямоугольника {a} и {b}. Найдите его диагональ.", f"Диагональ — гипотенуза: \\(\\sqrt{{{a*a} + {b*b}}} = {c}\\).", c, f"hyp({a},{b})")


def iso_height(r, lv):
    a, b, c = r.choice(TRIPLES[:8])
    return T(f"В равнобедренном треугольнике боковая сторона {c}, основание {2*a}. Найдите высоту, проведённую к основанию.",
             f"Высота делит основание пополам: {a}. \\(h = \\sqrt{{{c*c} - {a*a}}} = {b}\\).", b, f"leg({c},{a})")


# ---------- 31: уравнения со скобками и подобными ----------
def eq_similar(r, lv):
    a, b, x = r.randint(2, 9), r.randint(1, 7), r.randint(-6, 12) or 4
    return T(f"Решите уравнение {M(f'{a}x + {b}x = {(a+b)*x}')}.",
             f"Приводим подобные: {M(f'{a+b}x = {(a+b)*x}')}; {M(f'x = {(a+b)*x} : {a+b} = {x}')}.", x, f"F({(a+b)*x},{a+b})")


def eq_both(r, lv):
    a, c = r.randint(3, 9), r.randint(1, 8)
    while c == a: c = r.randint(1, 8)
    x = r.randint(-8, 10) or 2
    b = r.randint(-15, 15)
    dd = a * x + b - c * x
    return T(f"Решите уравнение {M(f'{a}x + {p(b)} = {c}x + {p(dd)}')}.",
             f"Иксы — влево, числа — вправо (при переносе знак меняется): {M(f'{a}x - {c}x = {dd} - {p(b)}')}; {M(f'{a-c}x = {dd-b}')}; {M(f'x = {num(Fr(dd-b, a-c))}')}.",
             Fr(dd - b, a - c), f"F({dd}-({b}),{a}-{c})")


def eq_open(r, lv):
    a, b, x = r.randint(2, 6), r.randint(1, 9), r.randint(-5, 10) or 3
    c = r.randint(1, 9)
    rhs = a * (x - b) + c
    return T(f"Решите уравнение {M(f'{a}(x - {b}) + {c} = {rhs}')}.",
             f"Раскрываем скобки: {M(f'{a}x - {a*b} + {c} = {rhs}')}; {M(f'{a}x = {rhs} + {a*b} - {c} = {rhs + a*b - c}')}; {M(f'x = {x}')}.", x, f"F({rhs}+{a*b}-{c},{a})")


def eq_lin_mix(r, lv):
    return r.choice([eq_similar, eq_both, eq_open])(r, lv)


# ---------- 32: проценты ----------
def pct_of(r, lv):
    pc, n = r.choice([10, 20, 25, 50, 5, 15, 30, 40, 75]), r.randint(2, 40) * 20
    return T(f"Найдите {pc}% от {n}.", f"{M(f'{n}{CD}\\frac{{{pc}}}{{100}} = {num(Fr(n*pc,100))}')}.", Fr(n * pc, 100), f"{n}*F({pc},100)")


def pct_discount(r, lv):
    pc, price = r.choice([10, 20, 25, 15, 30, 40]), r.randint(5, 60) * 100
    new = price * (100 - pc) // 100
    return T(f"Товар стоит {price} руб. Сколько он будет стоить со скидкой {pc}%?",
             f"Остаётся {100-pc}%: {M(f'{price}{CD}{num(Fr(100-pc,100))} = {new}')} руб.", new, f"{price}*F(100-{pc},100)")


def pct_up(r, lv):
    pc, price = r.choice([10, 20, 25, 5, 15, 30]), r.randint(5, 60) * 100
    new = price * (100 + pc) // 100
    return T(f"Цена {price} руб. повысилась на {pc}%. Какой стала цена?",
             f"Стало {100+pc}%: {M(f'{price}{CD}{num(Fr(100+pc,100))} = {new}')} руб.", new, f"{price}*F(100+{pc},100)")


def pct_what(r, lv):
    whole = r.choice([20, 25, 40, 50, 200, 400, 500])
    part = whole * r.choice([10, 20, 25, 30, 40, 50, 60, 75]) // 100
    return T(f"Сколько процентов составляет {part} от {whole}?", f"{M(f'\\frac{{{part}}}{{{whole}}}{CD}100\\% = {num(Fr(part*100,whole))}\\%')}.", Fr(part * 100, whole), f"F({part}*100,{whole})")


def pct_whole(r, lv):
    pc = r.choice([10, 20, 25, 50, 5])
    whole = r.randint(3, 40) * 20
    part = whole * pc // 100
    return T(f"{pc}% числа равны {part}. Найдите это число.", f"1% — это {M(f'{part} : {pc} = {num(Fr(part,pc))}')}; 100% — {M(f'{num(Fr(part,pc))}{CD}100 = {whole}')}.", whole, f"F({part}*100,{pc})")


def pct_mix(r, lv):
    return r.choice([pct_of, pct_discount, pct_up, pct_what, pct_whole])(r, lv)


# ---------- 33: окружность ----------
def circ_rd(r, lv):
    rr = r.randint(2, 30)
    if r.random() < .5:
        return T(f"Радиус окружности {rr}. Найдите диаметр.", f"Диаметр — два радиуса: {2*rr}.", 2 * rr, f"2*{rr}")
    return T(f"Диаметр окружности {2*rr}. Найдите радиус.", f"Радиус — половина диаметра: {rr}.", rr, f"{2*rr}//2")


def circ_len(r, lv):
    rr = r.randint(1, 10)
    L = Fr(314, 100) * 2 * rr
    return T(f"Найдите длину окружности радиуса {rr}. Считайте \\(\\pi \\approx 3{{,}}14\\).", f"\\(C = 2\\pi R = 2{CD}3{{,}}14{CD}{rr} = {d(L)}\\).", L, f"2*F('3.14')*{rr}")


def circ_area(r, lv):
    rr = r.randint(1, 10)
    S = Fr(314, 100) * rr * rr
    return T(f"Найдите площадь круга радиуса {rr}. Считайте \\(\\pi \\approx 3{{,}}14\\).", f"\\(S = \\pi R^2 = 3{{,}}14{CD}{rr*rr} = {d(S)}\\).", S, f"F('3.14')*{rr}**2")


def circ_inscribed(r, lv):
    c = r.randrange(40, 200, 2)
    if r.random() < .5:
        return T(f"Центральный угол равен {M(f'{c}{DG}')}. Найдите вписанный угол, опирающийся на ту же дугу.", f"Вписанный — половина центрального: {M(f'{c//2}{DG}')}.", c // 2, f"{c}//2")
    return T(f"Вписанный угол равен {M(f'{c//2}{DG}')}. Найдите центральный угол, опирающийся на ту же дугу.", f"Центральный — в 2 раза больше: {M(f'{c}{DG}')}.", c, f"2*{c//2}")


def circ_diam_angle(r, lv):
    a = r.randint(15, 75)
    return T(f"\\(AB\\) — диаметр окружности, \\(C\\) — точка на ней, \\(\\angle CAB = {a}^\\circ\\). Найдите \\(\\angle CBA\\).",
             f"Угол на диаметр \\(\\angle ACB = 90^\\circ\\). \\(\\angle CBA = 90 - {a} = {90-a}^\\circ\\).", 90 - a, f"90-{a}")


def grid_circle(r, lv):
    rr = r.randint(2, 5)
    fig = f"@fig grid={2*rr+2}x{2*rr+2}\nP O {rr+1} {rr+1} dot\nP A {2*rr+1} {rr+1} dot\ncircle O A\n@end"
    q = "Найдите радиус окружности с центром \\(O\\), проходящей через точку \\(A\\)." if r.random() < .5 else "Найдите диаметр окружности с центром \\(O\\), проходящей через точку \\(A\\)."
    if "радиус" in q:
        return GF(q, f"От \\(O\\) до \\(A\\) — {rr} клеток.", rr, f"{rr}", fig)
    return GF(q, f"Радиус {rr} клеток, диаметр {2*rr}.", 2 * rr, f"2*{rr}", fig)


# ---------- 34: вероятность ----------
def prob_simple(r, lv):
    n = r.choice([10, 20, 25, 40, 50, 100, 200, 500])
    m = r.randint(1, n - 1)
    while (Fr(m, n).denominator not in (1, 2, 4, 5, 10, 20, 25, 50, 100, 200, 500)): m = r.randint(1, n - 1)
    thing = r.choice([("В лотерее {n} билетов, выигрышных {m}.", "билет выигрышный"), ("В коробке {n} ручек, из них {m} красных.", "ручка красная"),
                      ("В сборнике {n} билетов, в {m} из них есть вопрос о дробях.", "попадётся вопрос о дробях")])
    return T(thing[0].format(n=n, m=m) + f" Найдите вероятность того, что {thing[1]}.",
             f"\\(P = \\frac{{{m}}}{{{n}}} = {d(Fr(m,n))}\\).", Fr(m, n), f"F({m},{n})")


def prob_not(r, lv):
    n = r.choice([20, 25, 50, 100, 200, 400, 1000]); m = r.randint(1, n // 4)
    while Fr(n - m, n).denominator not in (1, 2, 4, 5, 8, 10, 20, 25, 40, 50, 100, 200, 250, 500, 1000): m = r.randint(1, n // 4)
    return T(f"Из {n} фонариков {m} неисправны. Найдите вероятность того, что случайно выбранный фонарик исправен.",
             f"Исправных {n-m}: \\(P = \\frac{{{n-m}}}{{{n}}} = {d(Fr(n-m,n))}\\).", Fr(n - m, n), f"F({n}-{m},{n})")


def prob_rest(r, lv):
    n = r.choice([20, 25, 40, 50]); a = r.randint(2, n // 3); b = r.randint(2, n // 3)
    while Fr(n - a - b, n).denominator not in (1, 2, 4, 5, 8, 10, 20, 25, 40, 50): a = r.randint(2, n // 3)
    return T(f"В классе {n} учеников: {a} занимаются футболом, {b} — плаванием (каждый одним видом), остальные не занимаются спортом. Найдите вероятность того, что случайный ученик не занимается спортом.",
             f"Не занимаются: \\({n} - {a} - {b} = {n-a-b}\\). \\(P = \\frac{{{n-a-b}}}{{{n}}} = {d(Fr(n-a-b,n))}\\).", Fr(n - a - b, n), f"F({n}-{a}-{b},{n})")


def prob_dice(r, lv):
    k = r.randint(1, 5)
    q = r.choice([("больше", lambda v: v > k), ("меньше", lambda v: v < k + 1)])
    good = [v for v in range(1, 7) if q[1](v)]
    while Fr(len(good), 6).denominator not in (1, 2): k = r.randint(1, 5); good = [v for v in range(1, 7) if q[1](v)]
    thr = k if q[0] == "больше" else k + 1
    return T(f"Бросают игральный кубик. Найдите вероятность того, что выпадет число {q[0]} {thr}.",
             f"Подходят: {', '.join(map(str, good))} — {len(good)} из 6: \\({d(Fr(len(good),6))}\\).", Fr(len(good), 6), f"F({len(good)},6)")


def prob_mix(r, lv):
    return r.choice([prob_simple, prob_not, prob_rest])(r, lv)


# ---------- 35: формулы ----------
FORMULAS = [
    ("S = vt", "путь \\(S\\) (км), скорость \\(v\\) (км/ч), время \\(t\\) (ч)", ("v", "t"), lambda v, t: v * t, "S"),
    ("P = 2(a + b)", "периметр прямоугольника", ("a", "b"), lambda a, b: 2 * (a + b), "P"),
    ("C = 150 + 11(t - 5)", "стоимость поездки на такси \\(C\\) (руб.) длительностью \\(t\\) мин", ("t",), lambda t: 150 + 11 * (t - 5), "C"),
    ("F = 1{,}8C + 32", "температура по Фаренгейту через Цельсий", ("C",), lambda c: Fr(18, 10) * c + 32, "F"),
    ("A = Pt", "работа тока \\(A\\) (Дж), мощность \\(P\\) (Вт), время \\(t\\) (с)", ("P", "t"), lambda P, t: P * t, "A"),
]


def formula_sub(r, lv):
    f, desc, vars_, fn, res = r.choice(FORMULAS)
    vals = [r.randint(6, 40) if v == "t" and "такси" in desc else r.randint(2, 30) for v in vars_]
    if "Фаренгейт" in desc: vals = [r.randint(-20, 40)]
    out = fn(*vals)
    given = ", ".join(f"\\({v} = {x}\\)" for v, x in zip(vars_, vals))
    sub = f
    return T(f"Формула \\({f}\\) — {desc}. Найдите \\({res}\\), если {given}.",
             f"Подставляем: {given} → \\({res} = {num(out)}\\).", out, f"{num(out).replace('{,}', '.')}" if Fr(out).denominator == 1 else f"F('{float(out)}')")


def formula_find(r, lv):
    v, t = r.randint(3, 90), r.randint(2, 9)
    if r.random() < .5:
        return T(f"По формуле \\(S = vt\\) найдите \\(t\\) (в часах), если \\(S = {v*t}\\) км, \\(v = {v}\\) км/ч.",
                 f"\\({v*t} = {v}{CD}t\\) — неизвестный множитель: \\(t = {v*t} : {v} = {t}\\).", t, f"{v*t}//{v}")
    a, b = r.randint(2, 30), r.randint(2, 30)
    return T(f"По формуле \\(P = 2(a + b)\\) найдите \\(b\\), если \\(P = {2*(a+b)}\\), \\(a = {a}\\).",
             f"\\({2*(a+b)} = 2(a + b)\\) → \\(a + b = {a+b}\\) → \\(b = {a+b} - {a} = {b}\\).", b, f"{2*(a+b)}//2-{a}")


def formula_find2(r, lv):
    a, b, x = r.randint(2, 9), r.randint(10, 200), r.randint(3, 40)
    return T(f"Стоимость заказа считают по формуле \\(C = {b} + {a}n\\), где \\(n\\) — число предметов. Сколько предметов заказали, если \\(C = {b+a*x}\\)?",
             f"\\({b+a*x} = {b} + {a}n\\) → \\({a}n = {a*x}\\) → \\(n = {x}\\).", x, f"({b+a*x}-{b})//{a}")


# ---------- 36: четырёхугольники ----------
def quad_area(r, lv):
    k = r.choice(["par", "rhomb", "trap", "square"])
    if k == "par":
        a, h = r.randint(3, 20), r.randint(2, 15)
        return T(f"Сторона параллелограмма {a}, высота к ней {h}. Найдите площадь.", f"\\(S = ah = {a}{CD}{h} = {a*h}\\).", a * h, f"{a}*{h}")
    if k == "rhomb":
        d1, d2 = r.randint(2, 20) * 2, r.randint(3, 20)
        return T(f"Диагонали ромба {d1} и {d2}. Найдите площадь.", f"\\(S = \\frac{{d_1d_2}}{{2}} = \\frac{{{d1}{CD}{d2}}}{{2}} = {d1*d2//2}\\).", d1 * d2 // 2, f"{d1}*{d2}//2")
    if k == "trap":
        a, b, h = r.randint(2, 12), r.randint(6, 20), r.randint(2, 10)
        S = Fr((a + b) * h, 2)
        return T(f"Основания трапеции {a} и {b}, высота {h}. Найдите площадь.", f"\\(S = \\frac{{a + b}}{{2}}{CD}h = \\frac{{{a+b}}}{{2}}{CD}{h} = {num(S)}\\).", S, f"F(({a}+{b})*{h},2)")
    a = r.randint(2, 15)
    return T(f"Периметр квадрата {4*a}. Найдите его площадь.", f"Сторона \\({4*a} : 4 = {a}\\), \\(S = {a}^2 = {a*a}\\).", a * a, f"({4*a}//4)**2")


def quad_angle(r, lv):
    a = r.randint(30, 85)
    k = r.choice(["adj", "opp", "rhomb"])
    if k == "adj":
        return T(f"Один угол параллелограмма {M(f'{a}{DG}')}. Найдите соседний с ним угол.", f"Соседние углы в сумме \\(180^\\circ\\): {180-a}°.", 180 - a, f"180-{a}")
    if k == "opp":
        return T(f"Один угол параллелограмма {M(f'{a}{DG}')}. Найдите противоположный ему угол.", f"Противоположные углы равны: {a}°.", a, f"{a}")
    return T(f"Сумма двух углов параллелограмма {M(f'{2*a}{DG}')}. Найдите один из оставшихся углов.", f"Равные углы по {a}°, оставшиеся по {180-a}°.", 180 - a, f"180-{2*a}//2")


def grid_par(r, lv):
    a, h, s = r.randint(3, 6), r.randint(2, 4), r.randint(1, 3)
    fig = f"@fig grid={a+s+2}x{h+2}\npoly 1,1 {a+1},1 {a+s+1},{h+1} {s+1},{h+1} fill\n@end"
    return GF("Найдите площадь параллелограмма на клетчатой бумаге (клетка \\(1\\times1\\)).",
              f"Основание {a}, высота {h} (по вертикали): \\(S = {a*h}\\).", a * h, f"area((1,1),({a+1},1),({a+s+1},{h+1}),({s+1},{h+1}))", fig)


def grid_trap(r, lv):
    a, b, h = r.randint(5, 8), r.randint(1, 4), r.randint(2, 4)
    off = r.randint(1, a - b)
    fig = f"@fig grid={a+2}x{h+2}\npoly 1,1 {a+1},1 {off+b+1},{h+1} {off+1},{h+1} fill\n@end"
    S = Fr((a + b) * h, 2)
    return GF("Найдите площадь трапеции на клетчатой бумаге (клетка \\(1\\times1\\)).",
              f"Основания {a} и {b}, высота {h}: \\(S = \\frac{{{a}+{b}}}{{2}}{CD}{h} = {num(S)}\\).", S, f"area((1,1),({a+1},1),({off+b+1},{h+1}),({off+1},{h+1}))", fig)


# ---------- 37: №6 ----------
def oge6_frac(r, lv):
    pairs = [(2, 5), (3, 4), (1, 4), (3, 5), (7, 10), (1, 2), (4, 5), (9, 20), (3, 25)]
    (a1, b1), (a2, b2) = r.sample(pairs, 2)
    k = r.choice([2, 4, 5, 10, 20])
    res = (Fr(a1, b1) + Fr(a2, b2)) * k
    return T(f"Найдите значение выражения {M(f'\\left(\\frac{{{a1}}}{{{b1}}} + \\frac{{{a2}}}{{{b2}}}\\right){CD}{k}')}.",
             f"Скобка: {M(num(Fr(a1,b1)+Fr(a2,b2)))}; умножаем на {k}: {M(d(res))}.", res, f"(F({a1},{b1})+F({a2},{b2}))*{k}")


def oge6_dec(r, lv):
    a, b, c = Fr(r.randint(11, 99), 10), Fr(r.randint(2, 9), 10), Fr(r.randint(2, 9), 1)
    res = (a - b) * c if r.random() < .5 else None
    if res is not None:
        return T(f"Найдите значение выражения {M(f'({d(a)} - {d(b)}){CD}{c}')}.", f"Скобка {M(d(a-b))}; {M(f'{d(a-b)}{CD}{c} = {d(res)}')}.", res, f"(F('{float(a)}')-F('{float(b)}'))*{c}")
    q = r.randint(2, 30)
    b = Fr(r.randint(2, 9), 10)
    a = b * q
    return T(f"Найдите значение выражения {M(f'\\frac{{{d(a)}}}{{{d(b)}}}')}.", f"Переносим запятую: {M(f'{d(a*10)} : {d(b*10)} = {q}')}.", q, f"F('{float(a)}')/F('{float(b)}')")


def oge6_mix(r, lv):
    return r.choice([oge6_frac, oge6_dec, neg_expr, neg_oge6])(r, lv)


# ---------- 42: степени ----------
def pow_eval(r, lv):
    a, n = r.choice([(2, r.randint(2, 6)), (3, r.randint(2, 4)), (5, 2), (5, 3), (10, r.randint(2, 4)), (4, 2), (4, 3)])
    return T(f"Вычислите {M(f'{a}^{n}')}.", f"{M(f'{a}^{n} = ' + CD.join([str(a)]*n) + f' = {a**n}')}.", a ** n, f"{a}**{n}")


def pow_rule(r, lv):
    a = r.choice([2, 3, 5])
    m, n = r.randint(2, 6), r.randint(2, 5)
    k = r.choice(["mul", "div"])
    if k == "mul" and m + n <= 7:
        return T(f"Вычислите {M(f'{a}^{m}{CD}{a}^{n} : {a}^{m+n-2}')}.", f"Показатели: \\({m} + {n} - {m+n-2} = 2\\): \\({a}^2 = {a*a}\\).", a * a, f"{a}**{m}*{a}**{n}//{a}**{m+n-2}")
    big = m + n
    return T(f"Вычислите {M(f'\\frac{{{a}^{{{big}}}}}{{{a}^{{{big-2}}}}}')}.", f"При делении показатели вычитаются: \\({a}^{{{big}-{big-2}}} = {a}^2 = {a*a}\\).", a * a, f"F({a}**{big},{a}**{big-2})")


def pow_dec(r, lv):
    a = Fr(r.randint(1, 9), 10)
    return T(f"Вычислите {M(f'{d(a)}^2')}.", f"\\({d(a)}{CD}{d(a)} = {d(a*a)}\\) (после запятой две цифры).", a * a, f"F('{float(a)}')**2")


def pow_subst(r, lv):
    a, b = r.randint(2, 5), r.randint(-4, 4) or 2
    res = 3 * a * a - b ** 3
    return T(f"Найдите значение выражения \\(3a^2 - b^3\\) при \\(a = {a}\\), \\(b = {b}\\).",
             f"\\(3{CD}{a*a} - {p(b)}^3 = {3*a*a} - {p(b**3)} = {res}\\).", res, f"3*{a}**2-({b})**3")


# ---------- 43: тангенс, средняя линия ----------
def grid_tan(r, lv):
    a, b = r.choice([(4, 2), (2, 4), (5, 1), (4, 1), (3, 3), (2, 1), (4, 3), (5, 2), (1, 2)])
    fig = f"@fig grid={a+3}x{b+2}\nP O 1 1 hide\nP A {a+2} 1 hide\nP B {a+1} {b+1} hide\nseg O A thick\nseg O B thick\nangle A O B r=18\n@end"
    return GF("Найдите тангенс угла на клетчатой бумаге.",
              f"Опускаем перпендикуляр: противолежащий катет {b}, прилежащий {a}. \\(\\operatorname{{tg}} = \\frac{{{b}}}{{{a}}} = {d(Fr(b,a))}\\).", Fr(b, a), f"F({b},{a})", fig)


def midline(r, lv):
    if r.random() < .5:
        a = r.randint(4, 40)
        return T(f"Сторона треугольника равна {a}. Найдите среднюю линию, параллельную этой стороне.", f"Средняя линия — половина стороны: {num(Fr(a,2))}.", Fr(a, 2), f"F({a},2)")
    a, b = r.randint(2, 20), r.randint(5, 30)
    return T(f"Основания трапеции {a} и {b}. Найдите её среднюю линию.", f"Полусумма оснований: \\(\\frac{{{a} + {b}}}{{2}} = {num(Fr(a+b,2))}\\).", Fr(a + b, 2), f"F({a}+{b},2)")


def grid_midline(r, lv):
    a = r.randint(2, 4) * 2
    t = r.randint(0, a)
    fig = f"@fig grid={a+2}x5\nP A 1 1\nP B {t+1} 4\nP C {a+1} 1\npoly A B C\n@end"
    return GF("Найдите длину средней линии треугольника \\(ABC\\), параллельной стороне \\(AC\\) (клетка \\(1\\times1\\)).",
              f"\\(AC = {a}\\), средняя линия — половина: {a//2}.", a // 2, f"{a}//2", fig)


# ---------- 44: координатная прямая ----------
def cmp_frac(r, lv):
    opts = r.sample([Fr(1, 2), Fr(2, 5), Fr(3, 4), Fr(3, 5), Fr(7, 10), Fr(1, 4), Fr(4, 5), Fr(9, 20), Fr(13, 20), Fr(3, 8)], 4)
    big = r.random() < .5
    target = max(opts) if big else min(opts)
    i = opts.index(target) + 1
    lst = "; ".join(f"{k}) \\({num(x)}\\)" for k, x in enumerate(opts, 1))
    return T(f"Какое из чисел {'наибольшее' if big else 'наименьшее'}: {lst}? В ответ запишите номер.",
             "Переводим в десятичные: " + "; ".join(f"\\({d(x)}\\)" for x in opts) + f". Ответ: {i}.", i,
             f"(lambda v: v.index({'max' if big else 'min'}(v))+1)([{', '.join(f'F({x.numerator},{x.denominator})' for x in opts)}])")


def sqrt_between(r, lv):
    n = r.choice([x for x in range(5, 120) if int(math.isqrt(x)) ** 2 != x])
    k = math.isqrt(n)
    return T(f"Между какими соседними целыми числами находится \\(\\sqrt{{{n}}}\\)? В ответ запишите меньшее.",
             f"\\({k}^2 = {k*k} < {n} < {(k+1)**2} = {k+1}^2\\), значит \\({k} < \\sqrt{{{n}}} < {k+1}\\).", k, f"int(sqrt({n}))")


def numline_point(r, lv):
    vals = sorted(r.sample([Fr(x, 10) for x in range(-30, 40, 5) if x], 4))
    target = r.choice(vals)
    i = vals.index(target) + 1
    pts = "\n".join(f"pt {float(v)} {L}" for v, L in zip(vals, "ABCD"))
    fig = f"@numline -4 4 width=320\n{pts}\nmark 0 0\nmark 1 1\n@end"
    t = dict(q=f"На прямой отмечены точки \\(A, B, C, D\\). Какая из них соответствует числу \\({d(target)}\\)? Ответ: \\(A\\) — 1, \\(B\\) — 2, \\(C\\) — 3, \\(D\\) — 4.",
             sol=f"Точки идут по возрастанию слева направо; \\({d(target)}\\) — {i}-я по счёту.", ans=str(i), check=f"{i}", fig=fig)
    return t


# ---------- 47: пропорции, дробные коэффициенты ----------
def proportion(r, lv):
    a, b, k = r.randint(2, 9), r.randint(2, 9), r.randint(2, 6)
    c = a * k
    return T(f"Решите уравнение \\(\\frac{{x}}{{{b*k}}} = \\frac{{{a}}}{{{b}}}\\).",
             f"Крест-накрест: \\({b}x = {b*k}{CD}{a}\\), \\(x = {a*k}\\).", a * k, f"F({b*k}*{a},{b})")


def eq_frac_coef(r, lv):
    a, b = r.choice([(2, 3), (3, 4), (2, 5), (4, 6), (3, 6), (2, 4)])
    L = a * b // math.gcd(a, b)
    x = L * r.randint(1, 5)
    rhs = Fr(x, a) + Fr(x, b)
    return T(f"Решите уравнение \\(\\frac{{x}}{{{a}}} + \\frac{{x}}{{{b}}} = {num(rhs)}\\).",
             f"Умножаем всё на {L}: \\({L//a}x + {L//b}x = {num(rhs*L)}\\); \\({L//a + L//b}x = {num(rhs*L)}\\); \\(x = {x}\\).", x, f"F({rhs.numerator}*{L},{rhs.denominator}*({L//a}+{L//b}))")


def word_proportion(r, lv):
    a, b, c = r.randint(2, 6), r.randint(10, 40), r.randint(3, 12)
    return T(f"За {a} кг яблок заплатили {a*b} руб. Сколько стоят {c} кг таких яблок?",
             f"1 кг — \\({a*b} : {a} = {b}\\) руб.; {c} кг — \\({b}{CD}{c} = {b*c}\\) руб.", b * c, f"{a*b}//{a}*{c}")


# ---------- 48: арифметическая прогрессия ----------
def ap_next(r, lv):
    a1, dd = r.randint(-10, 20), r.choice([-5, -3, -2, 2, 3, 4, 5, 7])
    seq = [a1 + i * dd for i in range(4)]
    return T(f"Найдите следующий член последовательности: {', '.join(map(str, seq))}, …",
             f"Каждый раз прибавляем {dd}: {seq[-1]} + {p(dd)} = {seq[-1]+dd}.", seq[-1] + dd, f"{seq[-1]}+({dd})")


def ap_nth(r, lv):
    a1, dd, n = r.randint(-10, 20), r.choice([-4, -3, -2, 2, 3, 4, 5]), r.randint(5, 20)
    return T(f"Арифметическая прогрессия: \\(a_1 = {a1}\\), \\(d = {dd}\\). Найдите \\(a_{{{n}}}\\).",
             f"\\(a_n = a_1 + (n - 1)d = {a1} + {n-1}{CD}{p(dd)} = {a1+(n-1)*dd}\\).", a1 + (n - 1) * dd, f"ap({a1},{dd},{n})")


def ap_word(r, lv):
    a1, dd, n = r.randint(3, 20), r.randint(1, 5), r.randint(5, 15)
    return T(f"В первом ряду кинотеатра {a1} мест, а в каждом следующем на {dd} больше. Сколько мест в {n}-м ряду?",
             f"\\(a_{{{n}}} = {a1} + {n-1}{CD}{dd} = {a1+(n-1)*dd}\\).", a1 + (n - 1) * dd, f"ap({a1},{dd},{n})")


def ap_sum_small(r, lv):
    a1, dd, n = r.randint(1, 10), r.randint(1, 4), r.randint(4, 8)
    seq = [a1 + i * dd for i in range(n)]
    return T(f"Спортсмен в первый день пробежал {a1} км, а каждый следующий — на {dd} км больше. Сколько км он пробежит за {n} дней?",
             f"Выпишем: {', '.join(map(str, seq))}. Сумма {sum(seq)}.", sum(seq), f"aps({a1},{dd},{n})")


# ---------- 52: квадратные уравнения (простые) ----------
def quad_pure(r, lv):
    a = r.randint(2, 15)
    return T(f"Решите уравнение \\(x^2 = {a*a}\\). Если корней несколько, запишите больший.", f"\\(x = \\pm{a}\\). Больший {a}.", a, f"sqrt({a*a})")


def quad_factor(r, lv):
    a = r.randint(2, 12)
    return T(f"Решите уравнение \\(x^2 - {a}x = 0\\). Если корней несколько, запишите больший.", f"Выносим \\(x\\): \\(x(x - {a}) = 0\\) → \\(x = 0\\) или \\(x = {a}\\).", a, f"max(roots(1,-{a},0))")


def quad_full(r, lv):
    x1, x2 = r.randint(-8, 9), r.randint(-8, 9)
    while x1 == x2: x2 = r.randint(-8, 9)
    b, c = -(x1 + x2), x1 * x2
    big = max(x1, x2)
    D = b * b - 4 * c
    sb = f"+ {b}x" if b > 0 else (f"- {-b}x" if b < 0 else "")
    sc = f"+ {c}" if c > 0 else (f"- {-c}" if c < 0 else "")
    return T(f"Решите уравнение \\(x^2 {sb} {sc} = 0\\). Если корней несколько, запишите больший.",
             f"\\(D = {b}^2 - 4{CD}{p(c)} = {D}\\), \\(\\sqrt{{D}} = {math.isqrt(D)}\\). \\(x = \\frac{{{-b} \\pm {math.isqrt(D)}}}{{2}}\\): {x1} и {x2}. Больший {big}.",
             big, f"max(roots(1,{b},{c}))")


# ---------- 54: линейные неравенства ----------
def ineq_simple(r, lv):
    a, x0 = r.randint(2, 9), r.randint(-6, 8)
    b = r.randint(-10, 10)
    c = a * x0 + b
    return T(f"Решите неравенство \\({a}x + {p(b)} > {c}\\). В ответ запишите наименьшее целое решение.",
             f"\\({a}x > {c} - {p(b)} = {c-b}\\); \\(x > {x0}\\). Наименьшее целое: {x0+1}.", x0 + 1, f"min(x for x in range(-50,50) if {a}*x+({b}) > {c})")


def ineq_neg(r, lv):
    a, x0 = r.randint(2, 6), r.randint(-5, 6)
    c = -a * x0
    return T(f"Решите неравенство \\(-{a}x \\ge {c}\\). В ответ запишите наибольшее целое решение.",
             f"Делим на \\(-{a}\\) — <b>знак переворачивается</b>: \\(x \\le {x0}\\). Наибольшее целое {x0}.", x0, f"max(x for x in range(-50,50) if -{a}*x >= {c})")


def ineq_choice(r, lv):
    a, x0 = r.randint(2, 6), r.randint(-4, 5)
    b = r.randint(1, 9)
    c = a * x0 + b
    opts = [f"(-\\infty;\\ {x0})", f"({x0};\\ +\\infty)", f"(-\\infty;\\ {x0}]", f"[{x0};\\ +\\infty)"]
    return T(f"Укажите решение неравенства \\({a}x + {b} \\ge {c}\\).<div class=\"ls-opts\">" + "".join(f"<span>{i}) \\({o}\\)</span>" for i, o in enumerate(opts, 1)) + "</div>",
             f"\\({a}x \\ge {c-b}\\), \\(x \\ge {x0}\\) — точка закрашена, квадратная скобка: вариант 4.", 4,
             f"which(lambda x: {a}*x+{b} >= {c}, lambda x: x < {x0}, lambda x: x > {x0}, lambda x: x <= {x0}, lambda x: x >= {x0})")


# ---------- 58: графики ----------
def lin_value(r, lv):
    k, b, x = r.randint(-5, 5) or 2, r.randint(-10, 10), r.randint(-5, 5)
    return T(f"Функция задана формулой \\(y = {k}x + {p(b)}\\). Найдите \\(y\\) при \\(x = {x}\\).", f"\\(y = {k}{CD}{p(x)} + {p(b)} = {k*x+b}\\).", k * x + b, f"{k}*({x})+({b})")


def lin_kb(r, lv):
    k, b = r.choice([1, 2, 3, -1, -2, -3]), r.randint(-3, 3)
    fig = f"@plot -4 4 -5 5 scale=20\nf {k}*x + ({b})\n@end"
    t = dict(q="По графику функции \\(y = kx + b\\) определите \\(b\\) (где прямая пересекает ось \\(y\\)).", sol=f"Прямая пересекает ось \\(y\\) в точке {b}: \\(b = {b}\\).", ans=ans(b), check=f"{b}", fig=fig)
    return t


def graph_match(r, lv):
    par = r.choice([("x*x", "y = x^2"), ("-x*x", "y = -x^2"), ("x*x-2", "y = x^2 - 2")])
    hyp = r.choice([("2/x", "y = \\frac{2}{x}"), ("-2/x", "y = -\\frac{2}{x}")])
    lin = r.choice([("2*x+1", "y = 2x + 1"), ("-x+2", "y = -x + 2"), ("x-1", "y = x - 1")])
    three = [par, hyp, lin]; r.shuffle(three)
    order = three[:]; r.shuffle(order)
    figs = "".join(f"<figure>\n@plot -3 3 -3 3 scale=16\nf {f}\n@end\n<figcaption>{L}</figcaption></figure>" for (f, _), L in zip(order, "АБВ"))
    q = "Установите соответствие между графиками и формулами: " + "; ".join(f"{i}) \\({tex}\\)" for i, (_, tex) in enumerate(three, 1)) + f'.<div class="ls-figs">{figs}</div>'
    answer = "".join(str(three.index(o) + 1) for o in order)
    sol = "Парабола — есть \\(x^2\\), гипербола — \\(x\\) в знаменателе, прямая — \\(kx + b\\). " + ", ".join(f"{L} → {three.index(o)+1}" for o, L in zip(order, "АБВ")) + "."
    chk = f"match([{', '.join('lambda x: ' + o[0] for o in order)}], [{', '.join('lambda x: ' + t[0] for t in three)}])"
    return dict(q=q, sol=sol, ans=answer, check=chk)


GEN2 = {k: v for k, v in globals().items() if callable(v) and not k.startswith("_") and k not in ("num", "ans", "M", "T", "GF", "d", "Fr", "p")}
