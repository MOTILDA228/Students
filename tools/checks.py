"""Автопроверка ответов: строки @check в .lesson.

В @check пишется выражение на Python, которое заново считает ответ из условия
задачи (а не копирует его). Сборщик сравнивает результат с тем, что написано в @ans.
Доступны: F (обыкновенная дробь), sqrt, roots, hyp, leg, sind/cosd/tand,
ap/aps (арифм. прогрессия), gp/gps (геом. прогрессия), comb, solve2 (система 2×2), which (выбор варианта
в №13 по множеству решений), match (соответствие графиков и формул в №11), pi, math.
"""
import math
import re
from fractions import Fraction

F = Fraction


def sqrt(x):
    return math.sqrt(x)


def roots(a, b, c):
    """Корни ax² + bx + c = 0 по возрастанию; пустой список, если корней нет."""
    if a == 0:
        return [-c / b] if b else []
    d = b * b - 4 * a * c
    if d < 0:
        return []
    r = math.sqrt(d)
    return sorted({(-b - r) / (2 * a), (-b + r) / (2 * a)})


def hyp(a, b):
    """Гипотенуза по двум катетам."""
    return math.hypot(a, b)


def leg(c, a):
    """Катет по гипотенузе c и другому катету a."""
    return math.sqrt(c * c - a * a)


def sind(g):
    return math.sin(math.radians(g))


def cosd(g):
    return math.cos(math.radians(g))


def tand(g):
    return math.tan(math.radians(g))


def ap(a1, d, n):
    """n-й член арифметической прогрессии."""
    return a1 + (n - 1) * d


def aps(a1, d, n):
    """Сумма первых n членов арифметической прогрессии."""
    return F(2 * a1 + (n - 1) * d) * n / 2


def gp(b1, q, n):
    """n-й член геометрической прогрессии."""
    return b1 * F(q) ** (n - 1)


def gps(b1, q, n):
    """Сумма первых n членов геометрической прогрессии."""
    q = F(q)
    return b1 * n if q == 1 else b1 * (q ** n - 1) / (q - 1)


def comb(n, k):
    return math.comb(n, k)


def solve2(a, b, c, d, e, f):
    """Система a·x + b·y = c, d·x + e·y = f → [x, y] (обыкновенные дроби)."""
    det = F(a) * e - F(b) * d
    return [(F(c) * e - F(b) * f) / det, (F(a) * f - F(c) * d) / det]


def which(truth, *options):
    """Номер варианта (с 1), чьё множество совпадает с truth(x) на сетке точек от −50 до 50 с шагом 1/8.

    Для №13: which(lambda x: 3*x - 2 >= 4*x + 1, lambda x: x >= -3, lambda x: x <= -3, ...) → 2.
    """
    xs = [i / 8 for i in range(-400, 401)]
    hits = [k for k, opt in enumerate(options, 1) if all(bool(truth(x)) == bool(opt(x)) for x in xs)]
    return hits[0] if len(hits) == 1 else f"подходит вариантов: {len(hits)}"


def match(graphs, formulas, xs=(-3, -1.5, -0.5, 0.5, 1.5, 3)):
    """№11: для графиков А, Б, В (функции в том же порядке, что на рисунках) номера подходящих
    формул одной строкой, например «312»."""
    out = ""
    for g in graphs:
        hits = [k for k, f in enumerate(formulas, 1) if all(abs(g(x) - f(x)) < 1e-9 for x in xs)]
        out += str(hits[0]) if len(hits) == 1 else "?"
    return out


NS = {"F": F, "sqrt": sqrt, "roots": roots, "hyp": hyp, "leg": leg, "sind": sind, "cosd": cosd,
      "tand": tand, "ap": ap, "aps": aps, "gp": gp, "gps": gps, "comb": comb, "solve2": solve2, "which": which, "match": match, "pi": math.pi,
      "math": math, "abs": abs, "round": round, "min": min, "max": max, "sum": sum, "range": range,
      "len": len, "sorted": sorted, "int": int, "str": str, "float": float}


def parse_answer(text):
    """«\\(-2; 3\\)», «2,75», «\\(1\\frac{7}{12}\\)» → список значений."""
    s = text.replace("\\(", "").replace("\\)", "").replace("−", "-").replace("–", "-")
    s = s.replace("{,}", ".").replace("\\,", "")
    vals = []
    for part in s.split(";"):
        part = re.sub(r"^\s*[а-яa-z]\)\s*", "", part)  # «а) 81; б) 32» — подписи пунктов
        p = part.strip().replace(" ", "").replace(",", ".")
        m = re.fullmatch(r"(-?)(\d*)\\frac\{(\d+)\}\{(\d+)\}", p)
        if m:
            v = int(m.group(2) or 0) + F(int(m.group(3)), int(m.group(4)))
            vals.append(-v if m.group(1) else v)
            continue
        try:
            vals.append(F(p))
        except (ValueError, ZeroDivisionError):
            vals.append(part.strip())
    return vals


def verify(expr, answer):
    """(совпало?, пояснение) — сравнивает @check с @ans."""
    env = dict(NS, __builtins__={})  # NS — глобальные имена, чтобы работали и лямбды
    got = eval(expr, env)
    expected = list(got) if isinstance(got, (list, tuple, set)) else [got]
    given = parse_answer(answer)
    if len(expected) != len(given):
        return False, f"посчитано {expected}, в ответе {given}"
    try:
        e = sorted(float(v) for v in expected)
        g = sorted(float(v) for v in given)
    except (TypeError, ValueError):
        ok = sorted(str(v) for v in expected) == sorted(str(v) for v in given)
        return ok, f"посчитано {expected}, в ответе {given}"
    ok = all(abs(a - b) <= 1e-6 * max(1.0, abs(a)) for a, b in zip(e, g))
    return ok, f"посчитано {[round(v, 6) for v in e]}, в ответе {[round(v, 6) for v in g]}"
