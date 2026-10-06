"""Записи «в столбик» как в тетради в клетку: сложение, вычитание, умножение, деление уголком.

Каждая функция возвращает HTML-таблицу класса ls-col (стили — в tools/lesson_shell.html).
blank=True — «заготовка»: числа условия расставлены, клетки для работы пустые (для печати).
"""


def _grid(rows, width):
    """rows: список строк; строка — список из width ячеек (текст, набор классов)."""
    out = ['<table class="ls-col"><tbody>']
    for row in rows:
        out.append("<tr>" + "".join(f'<td class="{" ".join(sorted(c))}">{t}</td>' if c else f"<td>{t}</td>" for t, c in row) + "</tr>")
    out.append("</tbody></table>")
    return "".join(out)


def _row(width):
    return [["", set()] for _ in range(width)]


def _put(row, s, end, cls=None):
    """Записать строку s так, чтобы последний символ стоял в колонке end."""
    for k, ch in enumerate(s):
        i = end - (len(s) - 1 - k)
        row[i][0] = ch
        if cls: row[i][1] |= set(cls)


def _under(row, start, end):
    for i in range(start, end + 1):
        row[i][1].add("u")


def add_sub(a, b, op="+", blank=False):
    res = a + b if op == "+" else a - b
    w = max(len(str(a)), len(str(b)), len(str(res))) + 1
    end = w - 1
    carry = _row(w)
    if not blank:
        if op == "+":
            c, x, y = 0, a, b
            pos = end
            while x or y or c:
                s = x % 10 + y % 10 + c
                c = s // 10
                if c: carry[pos - 1][0] = "1"; carry[pos - 1][1].add("c")
                x //= 10; y //= 10; pos -= 1
        else:
            borrow, x, y, pos = 0, a, b, end
            while x:
                dx = x % 10 - borrow
                borrow = 1 if dx < y % 10 else 0
                if borrow: carry[pos - 1][0] = "•"; carry[pos - 1][1].add("c")
                x //= 10; y //= 10; pos -= 1
    r1, r2, r3 = _row(w), _row(w), _row(w)
    _put(r1, str(a), end)
    _put(r2, str(b), end)
    r2[end - len(str(max(a, b)))][0] = "−" if op == "-" else op
    _under(r2, end - len(str(max(a, b))) + 1, end)
    if not blank: _put(r3, str(res), end, ["q"])
    return _grid([carry, r1, r2, r3], w)


def mul(a, b, blank=False):
    sa, sb, sr = str(a), str(b), str(a * b)
    parts = [a * int(dig) for dig in reversed(sb)]
    w = max(len(sr), len(sa), len(sb), *(len(str(p)) + i for i, p in enumerate(parts))) + 1
    end = w - 1
    rows = []
    carry = _row(w)
    if not blank and len(sb) == 1:
        c, x, pos = 0, a, end
        while x:
            s = (x % 10) * b + c
            c = s // 10
            if c and x // 10: carry[pos - 1][0] = str(c); carry[pos - 1][1].add("c")
            x //= 10; pos -= 1
    rows.append(carry)
    r1, r2 = _row(w), _row(w)
    _put(r1, sa, end); _put(r2, sb, end)
    r2[end - max(len(sa), len(sb))][0] = "×"
    _under(r2, end - max(len(sa), len(sb)) + 1, end)
    rows += [r1, r2]
    if len(sb) == 1:
        r = _row(w)
        if not blank: _put(r, sr, end, ["q"])
        rows.append(r)
    else:
        for i, pv in enumerate(parts):
            r = _row(w)
            if not blank: _put(r, str(pv), end - i)
            if i == 0: pass
            rows.append(r)
        last = rows[-1]
        if not blank: last[end - len(sr)][0] = "+"
        _under(last, end - len(sr) + 1, end)
        r = _row(w)
        if not blank: _put(r, sr, end, ["q"])
        rows.append(r)
    return _grid(rows, w)


def div(p, d, blank=False):
    """Деление уголком. Слева делимое и вычитания, справа делитель и частное."""
    sp, q = str(p), p // d
    L = len(sp)
    steps, cur, started, qdig = [], 0, False, []
    for i, ch in enumerate(sp):
        cur = cur * 10 + int(ch)
        if not started and cur < d:
            continue
        started = True
        k = cur // d
        qdig.append(str(k))
        if k:
            steps.append((i, cur, k * d))
            cur -= k * d
    rem = cur
    right = max(len(str(d)), len(str(q))) + 1
    w = 1 + L + right
    R0 = 1 + L  # первая колонка правой части
    rows = []
    r0 = _row(w)
    _put(r0, sp, L)
    _put(r0, str(d), R0 + len(str(d)) - 1)
    for i in range(R0, w):
        r0[i][1] |= {"l"} if i == R0 else set()
        r0[i][1].add("u")
    r0[R0][1].add("l")
    rows.append(r0)
    if blank:
        for _ in range(2 * len(steps) + 1):
            r = _row(w)
            if not rows[1:]: r[R0][1].add("l")
            rows.append(r)
        return _grid(rows, w)
    for j, (i, curv, sub) in enumerate(steps):
        if j > 0:
            r = _row(w)
            _put(r, str(curv), i + 1)
            rows.append(r)
        r = _row(w)
        _put(r, str(sub), i + 1)
        r[i + 1 - len(str(sub))][0] = "−"
        _under(r, i + 2 - max(len(str(sub)), len(str(curv))), i + 1)
        if j == 0:
            r[R0][1].add("l")
            _put(r, str(q), R0 + len(str(q)) - 1, ["q"])
        rows.append(r)
    r = _row(w)
    _put(r, str(rem), L)
    rows.append(r)
    return _grid(rows, w)
