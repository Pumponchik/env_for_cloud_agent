# Research artifacts

Технические данные исследований. Читаемые отчёты — в **корне репозитория** (см. [`../README.md`](../README.md)).

## `prompt-length/`

Артефакты исследования длины промптов / synthetic captions.

| Path | Contents |
|------|----------|
| `outline.yaml` / `fields.yaml` | План и поля deep-research |
| `results/` | Структурированные JSON по объектам исследования |
| `corpus/` | Каталоги arXiv / отобранные корпуса |
| `citation_tree/` | Деревья цитирований (Brack, DALL·E 3 descendants, …) |
| `generate_report.py` | Скрипт сборки раннего `report.md` |
| `papers/` / `paper_extracts/` | Локальные HTML/PDF и текстовые выдержки (обычно в `.gitignore`) |

## `reprompt-systems/`

Артефакты исследования re-prompt / prompt enhancement.

| Path | Contents |
|------|----------|
| `outline.yaml` / `fields.yaml` | План и поля |
| `corpus/` | Отфильтрованные списки статей, curated reading list |
| `citation_trees/` | S2 trees по seed PE-papers |
| `raw_searches/` | Сырой arXiv dump |
