"""Собирает самодостаточные HTML-уроки.

Исходник: students/<ученик>/lessons/_src/NN-<тема>.html
Первая строка исходника: <!-- title: Заголовок -->
Результат: students/<ученик>/lessons/NN-<тема>.html
Запуск: python3 tools/build_lessons.py
"""
import pathlib, re
root = pathlib.Path(__file__).resolve().parent.parent
shell = (root / "tools/lesson_shell.html").read_text(encoding="utf-8")
for src in sorted(root.glob("students/*/lessons/_src/*.html")):
    body = src.read_text(encoding="utf-8")
    m = re.match(r"<!-- title: (.*?) -->", body)
    title = m.group(1) if m else src.stem
    out = src.parent.parent / src.name
    out.write_text(shell.replace("{{TITLE}}", title).replace("{{BODY}}", body), encoding="utf-8")
    print("built", out.relative_to(root))
