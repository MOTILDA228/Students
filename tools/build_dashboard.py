#!/usr/bin/env python3
"""Главная страница «Журнал учеников»: собирает таблицы из students/*/plan.md
в dashboard/journal.html. Отметки (пройдено, ДЗ, оценка ДЗ 0–10) хранятся не в файле,
а в базе опубликованной страницы (коллекция marks, документ <ученик>-<№>)."""
import json, re, pathlib
ROOT = pathlib.Path(__file__).resolve().parent.parent
NAMES = {"dima": "Дима", "zlata": "Злата"}

def parse(plan):
    goal = ""; rows = []
    for line in plan.read_text(encoding="utf-8").splitlines():
        m = re.match(r"\*\*Цель:\*\*\s*(.*)", line)
        if m: goal = m.group(1)
        c = [x.strip() for x in line.strip().strip("|").split("|")]
        if line.startswith("|") and len(c) >= 5 and c[0].isdigit():
            rows.append({"n": int(c[0]), "t": c[1], "oge": c[2], "type": c[3],
                         "m": c[4].replace("✅", "").strip()})
    return goal, rows

data = []
for d in sorted((ROOT / "students").iterdir()):
    p = d / "plan.md"
    if d.name.startswith("_") or not p.exists(): continue
    goal, rows = parse(p)
    if rows:
        data.append({"id": d.name, "name": NAMES.get(d.name, d.name.capitalize()), "goal": goal, "lessons": rows})
tpl = (ROOT / "tools" / "dashboard_template.html").read_text(encoding="utf-8")
out = ROOT / "dashboard" / "journal.html"
out.write_text(tpl.replace("/*DATA*/[]", json.dumps(data, ensure_ascii=False)), encoding="utf-8")
print(out, sum(len(s["lessons"]) for s in data), "уроков,", len(data), "учеников")
