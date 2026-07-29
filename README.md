# T2I Prompt Research

Исследование длины промптов / captions и систем **re-prompt (prompt enhancement)** для text-to-image.

Основные отчёты лежат **в корне**. Технические артефакты (JSON, YAML, корпусы, citation trees) — в [`research/`](./research/).

---

## С чего начать

| Приоритет | Файл | О чём |
|-----------|------|--------|
| **1** | [`report_reprompt_system_architecture_2026.md`](./report_reprompt_system_architecture_2026.md) | **Главный современный разбор (2025–2026):** зачем re-prompt, какая структура bridge user→model (text/JSON/latent/…), степени свободы, как строить правильно; история — отдельным разделом |
| **2** | [`report_reprompt_systems.md`](./report_reprompt_systems.md) | Более широкий академический дайджест PE |
| **3** | [`papers_catalog_reprompt.md`](./papers_catalog_reprompt.md) | Каталог статей по PE с приоритетами чтения |
| **4** | [`top_papers_prompt_length_variability.md`](./top_papers_prompt_length_variability.md) | Топ статей по длине и вариативности промпта |
| **5** | [`relevant_papers_prompt_caption_design.md`](./relevant_papers_prompt_caption_design.md) | 64 релевантные статьи: проблема / метод / результат |

---

## Все отчёты в корне

### Re-prompt / prompt enhancement
- [`report_reprompt_systems.md`](./report_reprompt_systems.md) — итоговый академический разбор PE
- [`papers_catalog_reprompt.md`](./papers_catalog_reprompt.md) — каталог и маршрут чтения

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
```

Подробнее: [`research/README.md`](./research/README.md).

---

## Короткий вывод

1. **Длина:** train–infer match критичен; лучше вариативность длины на обучении или long-train + PE на инференсе.
2. **Re-prompt:** закрывает разрыв train↔user caption distribution; цель — alignment к train caption law + faithfulness, не max verbosity и не голый aesthetic score.
3. **Практика:** gating (когда не репромптить), оценка против original prompt, decomposed / visual-grounded rewards.

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
