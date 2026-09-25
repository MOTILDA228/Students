#!/usr/bin/env python3
"""Сборщик уроков.

Исходники: students/<ученик>/lessons/_src/NN-<тема>.lesson  (формат — tools/LESSON_FORMAT.md)
Результат: students/<ученик>/lessons/NN-<тема>.html         (самодостаточные страницы)
           students/<ученик>/lessons/00-index.html          (оглавление по plan.md)

Запуск:    python3 tools/build_lessons.py          — собрать всех учеников
           python3 tools/build_lessons.py dima     — только одного

Каждая строка @check пересчитывается и сверяется с @ans. При расхождении
сборка печатает ОШИБКА и завершается с кодом 1 — такой урок коммитить нельзя.
"""
import html
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import checks  # noqa: E402
import figures  # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parent.parent
SHELL = (ROOT / "tools" / "lesson_shell.html").read_text(encoding="utf-8")
DEFAULT_TITLES = {"theory": "Шпаргалка", "practice": "Практика на уроке", "hw": "Домашнее задание",
                  "teacher": "Для репетитора: план урока"}
TEXT_SECTIONS = ("theory", "card", "teacher")
TASK_SECTIONS = ("practice", "hw", "tasks")


class Task:
    def __init__(self, line):
        self.line = line
        self.q, self.sol = [], []
        self.src = self.rep = self.ans = self.check = None


def parse(path):
    meta = {"title": path.stem, "tags": []}
    sections, cur, task, mode = [], None, None, None
    fig = None  # (kind, header, lines) пока собираем рисунок
    for no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        where = f"{path.name}:{no}"
        if fig is not None:
            if line.strip() == "@end":
                line = figures.render(*fig)
                fig = None
            else:
                fig[2].append(line)
                continue
        elif line.startswith("@"):
            word, _, rest = line[1:].partition(" ")
            rest = rest.strip()
            if word in ("fig", "numline", "plot"):
                fig = (word, rest, [])
                continue
            if word == "title":
                meta["title"] = rest
            elif word == "tags":
                meta["tags"] = [t.strip() for t in rest.split("|") if t.strip()]
            elif word in TEXT_SECTIONS:
                cur = {"kind": word, "title": rest or DEFAULT_TITLES.get(word, ""), "html": []}
                sections.append(cur)
                task = None
            elif word in TASK_SECTIONS:
                cur = {"kind": word, "title": rest or DEFAULT_TITLES.get(word, "Задачи"), "tasks": []}
                sections.append(cur)
                task = None
            elif word == "task":
                if cur is None or "tasks" not in cur:
                    raise SyntaxError(f"{where}: @task вне раздела с задачами")
                task = Task(where)
                cur["tasks"].append(task)
                mode = "q"
            elif word in ("src", "rep", "ans", "check", "sol"):
                if task is None:
                    raise SyntaxError(f"{where}: @{word} вне задачи")
                if word == "sol":
                    mode = "sol"
                else:
                    setattr(task, word, rest)
                    if word == "ans":
                        mode = None
            else:
                raise SyntaxError(f"{where}: неизвестная команда @{word}")
            continue
        if cur is None:
            if line.strip():
                raise SyntaxError(f"{where}: текст до первого раздела")
            continue
        if "html" in cur:
            cur["html"].append(line)
        elif task is not None and mode == "q":
            task.q.append(line)
        elif task is not None and mode == "sol":
            task.sol.append(line)
        elif line.strip():
            raise SyntaxError(f"{where}: текст вне условия/решения задачи")
    if fig is not None:
        raise SyntaxError(f"{path.name}: рисунок @{fig[0]} не закрыт строкой @end")
    return meta, sections


def strip_tags(s):
    return re.sub(r"<[^>]+>", "", s)


def render_task(i, t):
    head = [f'<span class="ls-task-num">{i}.</span>']
    if t.rep:
        rep = f"урок {t.rep}" if t.rep.isdigit() else t.rep
        head.append(f'<span class="ls-rep">Повторение ({rep})</span>')
    if t.src:
        head.append(f'<span class="ls-task-src">{t.src}</span><br>')
    q = "\n".join(t.q).strip()
    sol = "\n".join(t.sol).strip()
    return (f'<div class="ls-task"><div class="ls-task-q">{" ".join(head)} {q}</div>\n'
            f'<details><summary>Решение</summary>{sol}\n'
            f'<p class="ls-answer">Ответ: {t.ans}</p></details></div>')


def render_page(meta, sections, subtitle, prev, nxt):
    tags = "".join(f'<span class="ls-tag">{t}</span>' for t in meta["tags"])
    out = [f'<header class="ls-head"><h1>{meta["title"]}</h1><div class="ls-sub">{subtitle}</div>'
           f'<div class="ls-tags">{tags}</div></header>']
    nav = ['<a href="00-index.html">← Все уроки</a>']
    body = []
    for k, sec in enumerate(sections, 1):
        sid = f"ls-s{k}"
        if sec["kind"] == "teacher":
            body.append(f'<details class="ls-card ls-teacher"><summary>{sec["title"]}</summary>\n'
                        + "\n".join(sec["html"]) + "\n</details>")
            continue
        nav.append(f'<a href="#{sid}">{strip_tags(sec["title"])}</a>')
        inner = ("\n".join(sec["html"]) if "html" in sec
                 else "\n".join(render_task(i, t) for i, t in enumerate(sec["tasks"], 1)))
        body.append(f'<section class="ls-card" id="{sid}">\n<h2>{sec["title"]}</h2>\n{inner}\n</section>')
    nav.append('<button class="ls-btn" type="button" onclick="lsToggleAll(true)">Раскрыть все решения</button>')
    nav.append('<button class="ls-btn" type="button" onclick="lsToggleAll(false)">Свернуть все решения</button>')
    nav.append('<button class="ls-btn" type="button" onclick="lsStudentMode(this)">Режим ученика</button>')
    nav.append('<button class="ls-btn" type="button" onclick="lsPrintStudent()">Печать для ученика</button>')
    out.append('<nav class="ls-nav">' + "".join(nav) + "</nav>")
    out += body
    foot = []
    if prev:
        foot.append(f'<a href="{prev[0]}">← {prev[1]}</a>')
    foot.append('<a href="00-index.html">Все уроки</a>')
    if nxt:
        foot.append(f'<a href="{nxt[0]}">{nxt[1]} →</a>')
    out.append('<nav class="ls-foot">' + "".join(foot) + "</nav>")
    return "\n".join(out)


def validate(name, sections):
    """Ошибки (ломают сборку) и замечания по структуре урока."""
    errors, notes, checked, unchecked = [], [], 0, 0
    for sec in sections:
        if "tasks" not in sec:
            continue
        n = len(sec["tasks"])
        reps = sum(1 for t in sec["tasks"] if t.rep)
        if sec["kind"] == "practice" and not 5 <= n <= 7:
            notes.append(f"в практике {n} задач (норма 5–7)")
        if sec["kind"] == "hw" and not 5 <= n <= 8:
            notes.append(f"в ДЗ {n} задач (норма 5–8)")
        if sec["kind"] == "hw" and not 2 <= reps <= 4:
            notes.append(f"в ДЗ {reps} задач на повторение (норма 2–4)")
        for t in sec["tasks"]:
            if not t.q or not t.sol or not t.ans:
                errors.append(f"{t.line}: у задачи нет условия, решения или ответа")
                continue
            if not t.check:
                unchecked += 1
                continue
            try:
                ok, detail = checks.verify(t.check, t.ans)
            except Exception as exc:  # noqa: BLE001 — показываем любую ошибку в @check
                ok, detail = False, f"не удалось посчитать @check: {exc}"
            if ok:
                checked += 1
            else:
                errors.append(f"{t.line}: ответ не сходится — {detail}")
    return errors, notes, checked, unchecked


def plan_rows(student_dir):
    plan = student_dir / "plan.md"
    rows = []
    if plan.exists():
        for line in plan.read_text(encoding="utf-8").splitlines():
            m = re.match(r"^\|\s*(\d+)\s*\|([^|]*)\|([^|]*)\|([^|]*)\|([^|]*)\|", line)
            if m:
                rows.append([c.strip().replace("**", "") for c in m.groups()])
    return rows


def render_index(student_dir, subtitle, built):
    by_num = {int(re.match(r"\d+", p.name).group()): p.name for p in built}
    rows = plan_rows(student_dir)
    body = [f'<header class="ls-head"><h1>Уроки: {subtitle.split("·")[0].strip()}</h1>'
            f'<div class="ls-sub">{subtitle}</div>'
            f'<div class="ls-tags"><span class="ls-tag">готово уроков: {len(built)}</span>'
            f'<span class="ls-tag">в плане: {len(rows)}</span></div></header>',
            '<section class="ls-card"><h2>План и материалы</h2><div class="ls-table-wrap">'
            '<table class="ls-table ls-index"><thead><tr><th>№</th><th>Тема</th><th>ОГЭ</th>'
            '<th>Тип</th><th>Когда</th></tr></thead><tbody>']
    for num, topic, oge, kind, month in rows:
        n = int(num)
        cls = ' class="ls-row-geo"' if kind.strip() == "Г" else (
            ' class="ls-row-ctrl"' if "контроль" in kind else "")
        cell = f'<a href="{by_num[n]}">{html.escape(topic)}</a>' if n in by_num else html.escape(topic)
        body.append(f'<tr{cls}><td>{n}</td><td class="ls-left">{cell}</td><td>{oge}</td>'
                    f'<td>{kind}</td><td>{month}</td></tr>')
    body.append('</tbody></table></div><p class="ls-muted">Г — геометрия. Ссылка на теме — урок готов.</p></section>')
    return "\n".join(body)


def page(title, body):
    return SHELL.replace("{{TITLE}}", html.escape(strip_tags(title))).replace("{{BODY}}", body)


def build_student(student_dir):
    src_dir = student_dir / "lessons" / "_src"
    if not src_dir.is_dir():
        return 0
    sub_file = src_dir / "_student.txt"
    subtitle = sub_file.read_text(encoding="utf-8").strip() if sub_file.exists() else student_dir.name
    parsed = []
    for src in sorted(src_dir.glob("*.lesson")):
        meta, sections = parse(src)
        parsed.append((src, meta, sections))
    failed = 0
    built = []
    for i, (src, meta, sections) in enumerate(parsed):
        out = src_dir.parent / (src.stem + ".html")

        def link(item):
            return (item[0].stem + ".html", strip_tags(item[1]["title"]).split(".")[0]) if item else None

        prev = link(parsed[i - 1]) if i > 0 else None
        nxt = link(parsed[i + 1]) if i + 1 < len(parsed) else None
        out.write_text(page(meta["title"], render_page(meta, sections, subtitle, prev, nxt)), encoding="utf-8")
        built.append(out)
        errors, notes, checked, unchecked = validate(src.name, sections)
        status = "ОШИБКА" if errors else "ок"
        extra = f", без @check: {unchecked}" if unchecked else ""
        print(f"[{status}] {out.relative_to(ROOT)} — проверено ответов: {checked}{extra}")
        for e in errors:
            print(f"    ОШИБКА {e}")
        for n in notes:
            print(f"    замечание: {n}")
        failed += bool(errors)
    index = src_dir.parent / "00-index.html"
    index.write_text(page(f"Уроки — {student_dir.name}", render_index(student_dir, subtitle, built)),
                     encoding="utf-8")
    print(f"[ок] {index.relative_to(ROOT)}")
    return failed


def main(argv):
    names = argv[1:]
    dirs = [ROOT / "students" / n for n in names] if names else sorted(
        d for d in (ROOT / "students").iterdir() if d.is_dir() and not d.name.startswith("_"))
    failed = sum(build_student(d) for d in dirs)
    if failed:
        print(f"\nУроков с ошибками: {failed}. Исправьте ответы перед коммитом.")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
