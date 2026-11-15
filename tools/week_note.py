"""Renders plan.json + inbox.json into an Obsidian note for one week: python3 tools/week_note.py 2026-11-16 > note.md"""
import json, sys, datetime as dt
start = dt.date.fromisoformat(sys.argv[1])
plan = json.load(open("plan.json")); inbox = json.load(open("inbox.json"))
CAT = {"traffic": "🚀", "audience": "💬", "funnel": "🔻", "project": "🛠"}
WD = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]
RU = ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"]
def line(it):
    n = it.get("count", 1)
    t = it["title"] + (f" ×{n}" if n and n > 1 else "")
    meta = " · ".join(x for x in [it.get("where"), f"чат «{it['chat']}»" if it.get("chat") else None] if x)
    return f"- {CAT.get(it['cat'], '')} {t}" + (f" — *{meta}*" if meta else "")
end = start + dt.timedelta(days=6)
out = [f"# 📅 План недели {start:%d.%m}–{end:%d.%m}", "",
       "> Источник — репозиторий `mykh-tasks` (`plan.json`, `inbox.json`). Меняем план в чате «Штаб», заметка пересобирается оттуда.",
       "> Отметки «сделано» — в боте; здесь только план.", "",
       "## Каждый день", *[line(i) for i in plan["daily"]], ""]
for k in range(7):
    d = start + dt.timedelta(days=k)
    items = [line(i) for i in plan.get("weekdays", {}).get(WD[k], [])]
    items += [line({**i, "cat": i["cat"]}) + " *(разовая)*" for i in inbox if i["date"] == d.isoformat()]
    out += [f"## {RU[k]} {d:%d.%m}", *(items or ["- только ежедневная норма"]), ""]
out += ["## ➕ Если осталось время (кнопка «➕ Ещё задача» в боте)", *[line(i) for i in plan.get("extra", [])], ""]
print("\n".join(out))
