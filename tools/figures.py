"""Рисунки для уроков: короткое текстовое описание → inline SVG.

Линии рисуются цветом currentColor, заливки берутся из CSS-переменных урока,
поэтому рисунки работают и в светлой, и в тёмной теме. У каждого SVG свой
номер: id штриховок и обрезок не пересекаются, даже если рисунков на странице много.

Синтаксис описан в tools/LESSON_FORMAT.md (раздел «Рисунки»).
"""
import html
import itertools
import math
import re
import shlex

_uid = itertools.count(1)
FLAGS = {"fill", "dash", "thick", "hide", "dot", "nolabel", "flip", "nounit", "nogrid"}
LABEL_FONT = 'font-family="Times New Roman, Georgia, serif" font-style="italic" font-size="17"'
DIRS = {"n": (0, -1), "s": (0, 1), "e": (1, 0), "w": (-1, 0),
        "ne": (0.71, -0.71), "nw": (-0.71, -0.71), "se": (0.71, 0.71), "sw": (-0.71, 0.71)}
MATH = {name: getattr(math, name) for name in ("sqrt", "sin", "cos", "tan", "pi", "exp", "log")}
MATH["abs"] = abs


def num(v):
    """Подпись числа: 2.5 → «2,5», -3 → «−3»."""
    if abs(v - round(v)) < 1e-9:
        s = str(int(round(v)))
    else:
        s = f"{v:.3f}".rstrip("0").rstrip(".")
    return s.replace("-", "−").replace(".", ",")


def _f(v):
    return f"{v:.1f}".rstrip("0").rstrip(".")


def _esc(s):
    return html.escape(s, quote=False)


def _label(s):
    """«A_1» → A с нижним индексом 1."""
    if "_" in s:
        base, sub = s.split("_", 1)
        return f'{_esc(base)}<tspan dy="5" font-size="12">{_esc(sub)}</tspan>'
    return _esc(s)


def _parse(line):
    pos, opts, flags = [], {}, set()
    for t in shlex.split(line):
        if "=" in t:
            k, v = t.split("=", 1)
            opts[k] = v
        elif t in FLAGS:
            flags.add(t)
        else:
            pos.append(t)
    return pos, opts, flags


def _unit(x, y):
    d = math.hypot(x, y)
    return (x / d, y / d) if d > 1e-9 else (0.0, 0.0)


def _text(x, y, s, size=15, extra=""):
    return (f'<text x="{_f(x)}" y="{_f(y)}" text-anchor="middle" dominant-baseline="central" '
            f'font-size="{size}" fill="currentColor"{extra}>{_esc(s)}</text>')


def _svg(w, h, body):
    return (f'<svg class="ls-fig" viewBox="0 0 {_f(w)} {_f(h)}" width="{_f(w)}" height="{_f(h)}" '
            f'xmlns="http://www.w3.org/2000/svg" role="img">{body}</svg>')


def render(kind, header, lines):
    uid = next(_uid)
    if kind == "fig":
        return _fig(header, lines)
    if kind == "numline":
        return _numline(header, lines, uid)
    if kind == "plot":
        return _plot(header, lines, uid)
    raise ValueError(f"неизвестный рисунок @{kind}")


# ---------------------------------------------------------------- @fig

def _fig(header, lines):
    _, hopts, _ = _parse(header)
    pts, cmds = {}, []
    for raw in lines:
        line = raw.strip()
        if not line or line.startswith("%"):
            continue
        word = line.split(None, 1)[0]
        if word in ("text", "len"):
            parts = line.split(None, 3)
            cmds.append((word, parts[1:], {}, set()))
            continue
        pos, opts, flags = _parse(line)
        if word == "P":
            pts[pos[1]] = (float(pos[2]), float(pos[3]))
        cmds.append((word, pos[1:], opts, flags))

    def at(tok):
        if tok in pts:
            return pts[tok]
        if "," in tok:
            x, y = tok.split(",")
            return float(x), float(y)
        raise ValueError(f"рисунок: неизвестная точка «{tok}»")

    def radius(center, tok):
        if tok in pts:
            return math.dist(center, pts[tok])
        return float(tok)

    def extended(a, b, ext):
        ux, uy = _unit(b[0] - a[0], b[1] - a[1])
        return (a[0] - ux * ext, a[1] - uy * ext), (b[0] + ux * ext, b[1] + uy * ext)

    xs, ys = [p[0] for p in pts.values()], [p[1] for p in pts.values()]
    for word, args, opts, flags in cmds:
        if word == "circle":
            c = at(args[0])
            r = radius(c, args[1])
            xs += [c[0] - r, c[0] + r]
            ys += [c[1] - r, c[1] + r]
        elif word in ("poly", "seg"):
            for a in args:
                x, y = at(a)
                xs.append(x)
                ys.append(y)
        elif word == "line":
            for x, y in extended(at(args[0]), at(args[1]), float(opts.get("ext", 0.8))):
                xs.append(x)
                ys.append(y)
        elif word == "text":
            xs.append(float(args[0]))
            ys.append(float(args[1]))
    grid = hopts.get("grid")
    if grid:
        gw, gh = (int(v) for v in grid.lower().split("x"))
        xs += [0, gw]
        ys += [0, gh]
    x0, x1, y0, y1 = min(xs), max(xs), min(ys), max(ys)
    span = max(x1 - x0, y1 - y0, 1e-9)
    s = float(hopts.get("scale", 26 if grid else min(70, 280 / span)))
    m = float(hopts.get("margin", 12 if grid else 26))
    w, h = (x1 - x0) * s + 2 * m, (y1 - y0) * s + 2 * m

    def X(x):
        return m + (x - x0) * s

    def Y(y):
        return m + (y1 - y) * s

    def P(p):
        return X(p[0]), Y(p[1])

    if pts:
        cx = sum(X(p[0]) for p in pts.values()) / len(pts)
        cy = sum(Y(p[1]) for p in pts.values()) / len(pts)
    else:
        cx, cy = w / 2, h / 2

    out = []
    if grid:
        for i in range(gw + 1):
            out.append(f'<line x1="{_f(X(i))}" y1="{_f(Y(0))}" x2="{_f(X(i))}" y2="{_f(Y(gh))}" '
                       f'stroke="var(--ls-grid)" stroke-width="1"/>')
        for j in range(gh + 1):
            out.append(f'<line x1="{_f(X(0))}" y1="{_f(Y(j))}" x2="{_f(X(gw))}" y2="{_f(Y(j))}" '
                       f'stroke="var(--ls-grid)" stroke-width="1"/>')

    def stroke(flags, width=2.0):
        wdt = 3 if "thick" in flags else width
        dash = ' stroke-dasharray="6 4"' if "dash" in flags else ""
        return f'stroke="currentColor" stroke-width="{wdt}"{dash}'

    for word, args, opts, flags in cmds:
        if word == "P":
            continue
        if word == "poly":
            coords = " ".join(f"{_f(X(x))},{_f(Y(y))}" for x, y in (at(a) for a in args))
            fill = "var(--ls-fig-fill)" if "fill" in flags else "none"
            out.append(f'<polygon points="{coords}" fill="{fill}" {stroke(flags)} stroke-linejoin="round"/>')
        elif word in ("seg", "line"):
            a, b = at(args[0]), at(args[1])
            if word == "line":
                a, b = extended(a, b, float(opts.get("ext", 0.8)))
            out.append(f'<line x1="{_f(X(a[0]))}" y1="{_f(Y(a[1]))}" x2="{_f(X(b[0]))}" '
                       f'y2="{_f(Y(b[1]))}" {stroke(flags)} stroke-linecap="round"/>')
        elif word == "circle":
            c = at(args[0])
            r = radius(c, args[1]) * s
            fill = "var(--ls-fig-fill)" if "fill" in flags else "none"
            out.append(f'<circle cx="{_f(X(c[0]))}" cy="{_f(Y(c[1]))}" r="{_f(r)}" fill="{fill}" {stroke(flags)}/>')
        elif word == "arc":
            (cx0, cy0), (ax, ay), (qx, qy) = (P(at(a)) for a in args[:3])
            r = math.hypot(ax - cx0, ay - cy0)
            a1 = math.atan2(ay - cy0, ax - cx0)
            a2 = math.atan2(qy - cy0, qx - cx0)
            d = (a2 - a1 + math.pi) % (2 * math.pi) - math.pi
            if "flip" in flags:
                d -= math.copysign(2 * math.pi, d)
            pts_ = " ".join(f"{_f(cx0 + r * math.cos(a1 + d * t / 60))},{_f(cy0 + r * math.sin(a1 + d * t / 60))}"
                            for t in range(61))
            out.append(f'<polyline points="{pts_}" fill="none" {stroke(flags)}/>')
        elif word == "angle":
            (ax, ay), (bx, by), (qx, qy) = (P(at(a)) for a in args[:3])
            a1 = math.atan2(ay - by, ax - bx)
            a2 = math.atan2(qy - by, qx - bx)
            d = (a2 - a1 + math.pi) % (2 * math.pi) - math.pi
            if "flip" in flags:
                d -= math.copysign(2 * math.pi, d)
            r, n = float(opts.get("r", 20)), int(opts.get("n", 1))
            for k in range(n):
                rr = r + 4 * k
                arc = " ".join(f"{_f(bx + rr * math.cos(a1 + d * t / 24))},{_f(by + rr * math.sin(a1 + d * t / 24))}"
                               for t in range(25))
                out.append(f'<polyline points="{arc}" fill="none" stroke="currentColor" stroke-width="1.5"/>')
            if "label" in opts:
                mid, rr = a1 + d / 2, r + 4 * (n - 1) + 14
                out.append(_text(bx + rr * math.cos(mid), by + rr * math.sin(mid), opts["label"], 14))
        elif word == "right":
            (ax, ay), (bx, by), (qx, qy) = (P(at(a)) for a in args[:3])
            ux, uy = _unit(ax - bx, ay - by)
            vx, vy = _unit(qx - bx, qy - by)
            a = float(opts.get("size", 11))
            p1 = (bx + a * ux, by + a * uy)
            p2 = (p1[0] + a * vx, p1[1] + a * vy)
            p3 = (bx + a * vx, by + a * vy)
            out.append(f'<polyline points="{_f(p1[0])},{_f(p1[1])} {_f(p2[0])},{_f(p2[1])} '
                       f'{_f(p3[0])},{_f(p3[1])}" fill="none" stroke="currentColor" stroke-width="1.5"/>')
        elif word == "ticks":
            (ax, ay), (bx, by) = P(at(args[0])), P(at(args[1]))
            k = int(args[2]) if len(args) > 2 else 1
            ux, uy = _unit(bx - ax, by - ay)
            nx, ny = -uy, ux
            mx, my = (ax + bx) / 2, (ay + by) / 2
            for i in range(k):
                off = (i - (k - 1) / 2) * 5
                tx, ty = mx + ux * off, my + uy * off
                out.append(f'<line x1="{_f(tx - nx * 6)}" y1="{_f(ty - ny * 6)}" x2="{_f(tx + nx * 6)}" '
                           f'y2="{_f(ty + ny * 6)}" stroke="currentColor" stroke-width="1.6"/>')
        elif word == "len":
            (ax, ay), (bx, by) = P(at(args[0])), P(at(args[1]))
            ux, uy = _unit(bx - ax, by - ay)
            nx, ny = -uy, ux
            mx, my = (ax + bx) / 2, (ay + by) / 2
            if nx * (mx - cx) + ny * (my - cy) < 0:
                nx, ny = -nx, -ny
            label = args[2] if len(args) > 2 else ""
            out.append(_text(mx + nx * 13, my + ny * 13, label, 14))
        elif word == "text":
            out.append(_text(X(float(args[0])), Y(float(args[1])), args[2] if len(args) > 2 else "", 14))
        else:
            raise ValueError(f"рисунок: неизвестная команда «{word}»")

    for word, args, opts, flags in cmds:
        if word != "P":
            continue
        px, py = P(pts[args[0]])
        if "dot" in flags:
            out.append(f'<circle cx="{_f(px)}" cy="{_f(py)}" r="3.2" fill="currentColor"/>')
        if "hide" in flags:
            continue
        if opts.get("pos") in DIRS:
            dx, dy = DIRS[opts["pos"]]
        else:
            dx, dy = _unit(px - cx, py - cy)
            if dx == dy == 0:
                dx, dy = DIRS["sw"]
        label = opts.get("label", args[0])
        out.append(f'<text x="{_f(px + dx * 14)}" y="{_f(py + dy * 14)}" text-anchor="middle" '
                   f'dominant-baseline="central" {LABEL_FONT} fill="currentColor">{_label(label)}</text>')
    return _svg(w, h, "".join(out))


# ---------------------------------------------------------------- @numline

def _nl_value(tok):
    """«2.5» → (2.5, «2,5»); «1.41:√2» → (1.41, «√2»)."""
    if ":" in tok:
        v, lab = tok.split(":", 1)
        return float(v), lab
    v = float(tok)
    return v, num(v)


def _numline(header, lines, uid):
    pos, opts, _ = _parse(header)
    lo, hi = float(pos[0]), float(pos[1])
    w = float(opts.get("width", 340))
    m, y0, h = 30.0, 30.0, 62.0

    def X(v):
        return m + (v - lo) / (hi - lo) * (w - 2 * m)

    hatch = f"ls-hatch-{uid}"
    out = [f'<defs><pattern id="{hatch}" patternUnits="userSpaceOnUse" width="7" height="7" '
           f'patternTransform="rotate(45)"><line x1="0" y1="0" x2="0" y2="7" stroke="currentColor" '
           f'stroke-width="1.4"/></pattern></defs>',
           f'<line x1="6" y1="{_f(y0)}" x2="{_f(w - 8)}" y2="{_f(y0)}" stroke="currentColor" stroke-width="1.6"/>',
           f'<polygon points="{_f(w - 4)},{_f(y0)} {_f(w - 14)},{_f(y0 - 4)} {_f(w - 14)},{_f(y0 + 4)}" '
           f'fill="currentColor"/>']
    ends, top = [], []
    has_int = False
    for raw in lines:
        line = raw.strip()
        if not line or line.startswith("%"):
            continue
        word, _, rest = line.partition(" ")
        rest = rest.strip()
        if word == "int":
            has_int = True
            for part in re.split(r"\s*(?:\bU\b|∪)\s*", rest):
                mt = re.fullmatch(r"([\[\(])\s*(.+?)\s*;\s*(.+?)\s*([\]\)])", part.strip())
                if not mt:
                    raise ValueError(f"числовая прямая: не понял промежуток «{part}»")
                lb, a, b, rb = mt.groups()
                xa = 6.0 if "inf" in a else X(_nl_value(a)[0])
                xb = w - 16 if "inf" in b else X(_nl_value(b)[0])
                out.append(f'<rect x="{_f(xa)}" y="{_f(y0 - 15)}" width="{_f(xb - xa)}" height="15" '
                           f'fill="url(#{hatch})"/>')
                for tok, closed in ((a, lb == "["), (b, rb == "]")):
                    if "inf" not in tok:
                        v, lab = _nl_value(tok)
                        ends.append((X(v), closed, lab))
        elif word in ("pt", "mark"):
            v, _, lab = rest.partition(" ")
            x = X(float(v))
            if word == "pt":
                top.append(f'<circle cx="{_f(x)}" cy="{_f(y0)}" r="3.5" fill="currentColor"/>')
                top.append(_text(x, y0 - 13, lab.strip(), 15, ' font-style="italic"'))
            else:
                top.append(f'<line x1="{_f(x)}" y1="{_f(y0 - 5)}" x2="{_f(x)}" y2="{_f(y0 + 5)}" '
                           f'stroke="currentColor" stroke-width="1.6"/>')
                top.append(_text(x, y0 + 17, lab.strip(), 14))
        else:
            raise ValueError(f"числовая прямая: неизвестная команда «{word}»")
    for x, closed, lab in ends:
        fill = "currentColor" if closed else "var(--ls-card)"
        out.append(f'<circle cx="{_f(x)}" cy="{_f(y0)}" r="4.5" fill="{fill}" stroke="currentColor" stroke-width="1.6"/>')
        if lab:
            out.append(_text(x, y0 + 18, lab, 14))
    out += top
    if has_int:
        out.append(_text(w - 10, y0 + 17, "x", 15, ' font-style="italic"'))
    return _svg(w, h, "".join(out))


# ---------------------------------------------------------------- @plot

def _plot(header, lines, uid):
    pos, opts, flags = _parse(header)
    xmin, xmax, ymin, ymax = (float(v) for v in pos[:4])
    s = float(opts.get("scale", 24))
    m = 18.0
    w, h = (xmax - xmin) * s + 2 * m, (ymax - ymin) * s + 2 * m

    def X(x):
        return m + (x - xmin) * s

    def Y(y):
        return m + (ymax - y) * s

    clip = f"ls-clip-{uid}"
    out = [f'<defs><clipPath id="{clip}"><rect x="{_f(m)}" y="{_f(m)}" width="{_f(w - 2 * m)}" '
           f'height="{_f(h - 2 * m)}"/></clipPath></defs>']
    if "nogrid" not in flags:
        for i in range(math.ceil(xmin), math.floor(xmax) + 1):
            out.append(f'<line x1="{_f(X(i))}" y1="{_f(Y(ymin))}" x2="{_f(X(i))}" y2="{_f(Y(ymax))}" '
                       f'stroke="var(--ls-grid)" stroke-width="1"/>')
        for j in range(math.ceil(ymin), math.floor(ymax) + 1):
            out.append(f'<line x1="{_f(X(xmin))}" y1="{_f(Y(j))}" x2="{_f(X(xmax))}" y2="{_f(Y(j))}" '
                       f'stroke="var(--ls-grid)" stroke-width="1"/>')
    if ymin <= 0 <= ymax:
        yy = Y(0)
        out.append(f'<line x1="{_f(X(xmin))}" y1="{_f(yy)}" x2="{_f(X(xmax) + 10)}" y2="{_f(yy)}" '
                   f'stroke="currentColor" stroke-width="1.5"/>')
        out.append(f'<polygon points="{_f(X(xmax) + 14)},{_f(yy)} {_f(X(xmax) + 5)},{_f(yy - 4)} '
                   f'{_f(X(xmax) + 5)},{_f(yy + 4)}" fill="currentColor"/>')
        out.append(_text(X(xmax) + 6, yy + 15, "x", 15, ' font-style="italic"'))
    if xmin <= 0 <= xmax:
        xx = X(0)
        out.append(f'<line x1="{_f(xx)}" y1="{_f(Y(ymin))}" x2="{_f(xx)}" y2="{_f(Y(ymax) - 10)}" '
                   f'stroke="currentColor" stroke-width="1.5"/>')
        out.append(f'<polygon points="{_f(xx)},{_f(Y(ymax) - 14)} {_f(xx - 4)},{_f(Y(ymax) - 5)} '
                   f'{_f(xx + 4)},{_f(Y(ymax) - 5)}" fill="currentColor"/>')
        out.append(_text(xx - 12, Y(ymax) - 6, "y", 15, ' font-style="italic"'))
    if xmin <= 0 <= xmax and ymin <= 0 <= ymax:
        out.append(_text(X(0) - 9, Y(0) + 13, "0", 13))
        if "nounit" not in flags:
            if xmax >= 1:
                out.append(_text(X(1), Y(0) + 13, "1", 13))
            if ymax >= 1:
                out.append(_text(X(0) - 9, Y(1), "1", 13))
    for raw in lines:
        line = raw.strip()
        if not line or line.startswith("%"):
            continue
        word, _, rest = line.partition(" ")
        if word == "f":
            parts = [p.strip() for p in rest.split("|")]
            expr = parts[0]
            code = compile(expr, "<plot>", "eval")
            n = int((xmax - xmin) * 60) + 1
            runs, cur, prev = [], [], None
            for i in range(n):
                x = xmin + (xmax - xmin) * i / (n - 1)
                try:
                    y = float(eval(code, {"__builtins__": {}}, dict(MATH, x=x)))
                except (ZeroDivisionError, ValueError, OverflowError):
                    y = None
                if y is not None and not math.isfinite(y):
                    y = None
                if y is not None:
                    y = max(ymin - 40, min(ymax + 40, y))
                if y is None or (prev is not None and abs(Y(y) - Y(prev)) > h):
                    if len(cur) > 1:
                        runs.append(cur)
                    cur = []
                if y is not None:
                    cur.append(f"{_f(X(x))},{_f(Y(y))}")
                prev = y
            if len(cur) > 1:
                runs.append(cur)
            for run in runs:
                out.append(f'<polyline points="{" ".join(run)}" fill="none" stroke="var(--ls-accent)" '
                           f'stroke-width="2.2" clip-path="url(#{clip})"/>')
            if len(parts) > 1 and parts[1]:
                ax = float(parts[2]) if len(parts) > 2 else xmax - 1
                ay = float(eval(code, {"__builtins__": {}}, dict(MATH, x=ax)))
                half = len(parts[1]) * 3.9  # примерная половина ширины подписи
                lx = min(max(X(ax) + 6, half + 2), w - half - 2)
                ly = min(max(Y(ay) - 12, 10), h - 10)
                out.append(_text(lx, ly, parts[1], 14, ' font-style="italic"'))
        elif word == "pt":
            p = rest.split(None, 2)
            px, py = X(float(p[0])), Y(float(p[1]))
            out.append(f'<circle cx="{_f(px)}" cy="{_f(py)}" r="3.5" fill="currentColor"/>')
            if len(p) > 2:
                out.append(_text(px + 10, py - 11, p[2], 14))
        elif word == "seg":
            p = rest.split()
            dash = ' stroke-dasharray="5 4"' if "dash" in p else ""
            out.append(f'<line x1="{_f(X(float(p[0])))}" y1="{_f(Y(float(p[1])))}" x2="{_f(X(float(p[2])))}" '
                       f'y2="{_f(Y(float(p[3])))}" stroke="currentColor" stroke-width="1.5"{dash}/>')
        elif word == "text":
            p = rest.split(None, 2)
            out.append(_text(X(float(p[0])), Y(float(p[1])), p[2] if len(p) > 2 else "", 14))
        else:
            raise ValueError(f"график: неизвестная команда «{word}»")
    return _svg(w, h, "".join(out))
