# T2I Prompt Research

Исследование длины промптов / captions и систем **re-prompt (prompt enhancement)** для text-to-image.

Основные отчёты лежат **в корне**. Технические артефакты (JSON, YAML, корпусы, citation trees) — в [`research/`](./research/).

---

## С чего начать

| Приоритет | Файл | О чём |
|-----------|------|--------|
| **1** | [`report_bridge_methods_taxonomy.md`](./report_bridge_methods_taxonomy.md) | **Все способы bridge** user→generator: текст / embeddings / layout / schema / endogenous / action; плюсы·минусы |
| **2** | [`fundamental_papers_reprompt_reading_list.md`](./fundamental_papers_reprompt_reading_list.md) | Современное ядро textual PE 2025–26; 23–24 в §D |
| **3** | [`report_reprompt_system_architecture_2026.md`](./report_reprompt_system_architecture_2026.md) | Архитектура textual bridge: IR, длина, gating |
| **4** | [`papers_catalog_bridge_methods.md`](./papers_catalog_bridge_methods.md) | Каталог статей по всем семьям bridge |
| **5** | [`report_reprompt_systems.md`](./report_reprompt_systems.md) | Более широкий академический дайджест PE |
| **6** | [`top_papers_prompt_length_variability.md`](./top_papers_prompt_length_variability.md) | Топ статей по длине и вариативности промпта |

---

## Все отчёты в корне

### Bridge methods (все семьи) и re-prompt
- [`report_bridge_methods_taxonomy.md`](./report_bridge_methods_taxonomy.md) — таксономия F1–F6: текст, embeddings, layout, schema, endogenous, action + pros/cons
- [`papers_catalog_bridge_methods.md`](./papers_catalog_bridge_methods.md) — каталог must-read по семьям bridge
- [`fundamental_papers_reprompt_reading_list.md`](./fundamental_papers_reprompt_reading_list.md) — современный P0/P1 список textual PE; 23–24 в §D
- [`report_reprompt_system_architecture_2026.md`](./report_reprompt_system_architecture_2026.md) — архитектура textual bridge, IR, length, gating
- [`report_reprompt_systems.md`](./report_reprompt_systems.md) — более широкий академический разбор PE
- [`papers_catalog_reprompt.md`](./papers_catalog_reprompt.md) — каталог textual PE

### Длина промпта и captions
- [`top_papers_prompt_length_variability.md`](./top_papers_prompt_length_variability.md) — топ по length/variability
- [`relevant_papers_prompt_caption_design.md`](./relevant_papers_prompt_caption_design.md) — краткие P/M/R
- [`report_around_brack_2506_16679.md`](./report_around_brack_2506_16679.md) — вокруг Brack et al. (контролируемые captions)
- [`report_dalle3_prompt_reprompt_descendants.md`](./report_dalle3_prompt_reprompt_descendants.md) — потомки DALL·E 3 Better Captions
- [`literature_review_modern_prompt_length.md`](./literature_review_modern_prompt_length.md) — обзор современной длины (~150)
- [`combined_report_prompt_length_300.md`](./combined_report_prompt_length_300.md) — сводный отчёт (~300)
- [`report_prompt_length_initial.md`](./report_prompt_length_initial.md) — первый deep-dive отчёт

---

## Технические артефакты

```
research/
  prompt-length/          # корпусы, results JSON, citation trees по длине
  reprompt-systems/       # корпусы, citation trees, outline/fields по PE
  bridge-methods/         # таксономия bridge: corpus, citation trees, outline/fields
```

Подробнее: [`research/README.md`](./research/README.md).

---

## Короткий вывод

1. **Длина:** train–infer match критичен; лучше вариативность длины на обучении или long-train + PE на инференсе.
2. **Bridge ≠ только текст:** F1 rewrite · F2 embeddings · F3 layout · F4 schema · F5 endogenous CoT · F6 action space — выбирать по типу gap и контролю над training.
3. **Re-prompt (F1):** закрывает train↔user captions; нужен gating и оценка vs original; для spatial/count часто лучше F3/F6.
4. **Практика:** назвать gap → выбрать семью → стекать дополняющие рычаги (SCoT: text CoT + boxes).

---

## Окружение Cloud Agent

В этом же репозитории:

| Path | Purpose |
|------|---------|
| `.cursor/skills/` | Cursor project skills |
| `.agents/skills/` | Agents discovery |
| `.claude/skills/` + `.claude/agents/` | Research skills + `web-search-agent` |
| `scripts/cloud-agent-install.sh` | Bootstrap |

```bash
./scripts/cloud-agent-install.sh
```
