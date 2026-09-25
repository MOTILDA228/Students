"""Автопроверка ответов: строки @check в .lesson.

В @check пишется выражение на Python, которое заново считает ответ из условия
задачи (а не копирует его). Сборщик сравнивает результат с тем, что написано в @ans.
Доступны: F (обыкновенная дробь), sqrt, roots, hyp, leg, sind/cosd/tand,
ap/aps (арифм. прогрессия), gp/gps (геом. прогрессия), comb, pi, math.
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


NS = {"F": F, "sqrt": sqrt, "roots": roots, "hyp": hyp, "leg": leg, "sind": sind, "cosd": cosd,
      "tand": tand, "ap": ap, "aps": aps, "gp": gp, "gps": gps, "comb": comb, "pi": math.pi,
      "math": math, "abs": abs, "round": round, "min": min, "max": max, "sum": sum, "range": range,
      "len": len, "sorted": sorted, "int": int}


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
