# T2I Prompt Research

Исследование длины промптов / captions и систем **re-prompt (prompt enhancement)** для text-to-image.

Основные отчёты лежат **в корне**. Технические артефакты (JSON, YAML, корпусы, citation trees) — в [`research/`](./research/).

---

## С чего начать

| Приоритет | Файл | О чём |
|-----------|------|--------|
| **0** | [`fundamental_questions_text_conditioning.md`](./fundamental_questions_text_conditioning.md) | **Фундаментальные вопросы** (пересмотр): критика старого списка + 6 фальсифицируемых Q |
| **0★** | [`mechanism_stack_structured_reprompt.md`](./mechanism_stack_structured_reprompt.md) | **Стек механизмов** «почему structure re-prompt лучше»: L0–L7, hierarchical shuffle, лестница экспериментов |
| **0★★** | [`open_questions_v2_and_latent_dualtrain.md`](./open_questions_v2_and_latent_dualtrain.md) | **Новые вопросы Q7–Q18** + разбор идеи «user→латенты без текста, joint train» |
| **0★★** | [`open_questions_v2_and_latent_dualtrain.md`](./open_questions_v2_and_latent_dualtrain.md) | **Открытые вопросы v2 (Q7–Q18)** + разбор идеи «латент вместо переписанного текста» с совместным обучением (E1–E7, вердикт) |
| **0a** | [`ideas_t2i_conditioning_stage.md`](./ideas_t2i_conditioning_stage.md) | **5 идей** связной прозой (info-matched NL↔SP и др.) |
| **0b** | [`ideas_t2i_conditioning_narrative.md`](./ideas_t2i_conditioning_narrative.md) | **Шаблон (1)–(4), ранжирование, нарратив статьи + план проверки** |
| **0c** | [`training_bytedance_context_scaling.md`](./training_bytedance_context_scaling.md) | **Как учили в Seed/ByteDance Context Scaling** (annotation, diffuser, prompter) |
| **0d** | [`take_should_we_train_reprompter.md`](./take_should_we_train_reprompter.md) | **Как учат репромптер:** данные, эффект, недостатки по конкретным работам |
| **0d′** | [`ideas_reprompter_training_bakeoff.md`](./ideas_reprompter_training_bakeoff.md) | **Bakeoff обучения re-prompter: SFT / RL / agents** + якоря статей |
| **0d″** | [`take_what_to_put_in_prompt.md`](./take_what_to_put_in_prompt.md) | **Что писать в промпте:** типы фактов, позиции, что не писать |
| **0d‴** | [`take_specify_a_vs_b.md`](./take_specify_a_vs_b.md) | **Указывать A лучше B?** поиск + как мерить (packing) |
| **0d⁴** | [`take_sp_length.md`](./take_sp_length.md) | **Длина SP:** что известно про NL, применимо ли к SP, открытые дыры |
| **0d⁵** | [`take_reprompt_format.md`](./take_reprompt_format.md) | **Формат re-prompt:** проза / шаблон / JSON / регионы / что придумать |
| **0d⁵′** | [`take_reprompt_output_dofs.md`](./take_reprompt_output_dofs.md) | **Степени свободы выхода re-prompt:** что варьировать в артефакте (SOTA vs open) |
| **0d⁶** | [`take_prompt_compression.md`](./take_prompt_compression.md) | **Сжатие канала:** LLM→LLM (текст / gist / KV / packing) |
| **0e** | [`literature_notes_user_survey.md`](./literature_notes_user_survey.md) | **Ваш обзор статей** (длина/captions, re-prompt, что не про то) + стыковка с идеями |
| **0f** | [`mechanism_stack_structured_reprompt.md`](./mechanism_stack_structured_reprompt.md) | **Почему структурный re-prompt работает:** стек L0–L7, иерархические shuffle-контроли, лестница S1–S6 |
| **1** | [`report_open_problems_autonomous_audit.md`](./report_open_problems_autonomous_audit.md) | **Полный аудит:** T1–T12 статусы + 24 новые проблемы + ложные закрытия |
| **2** | [`report_open_research_questions_reprompt_bridge.md`](./report_open_research_questions_reprompt_bridge.md) | Короткая карта «куда копать» |
| **3** | [`reading_list_reprompter_latent_and_alt_channels.md`](./reading_list_reprompter_latent_and_alt_channels.md) | Re-prompter→G: латентный/векторный канал и альтернативы |
| **4** | [`report_reprompter_nontextual_channels.md`](./report_reprompter_nontextual_channels.md) | Нетекстовые каналы enrichment для T2I |
| **5** | [`report_bridge_methods_taxonomy.md`](./report_bridge_methods_taxonomy.md) | Таксономия F1–F6 + pros/cons |
| **6** | [`fundamental_papers_reprompt_reading_list.md`](./fundamental_papers_reprompt_reading_list.md) | Современное ядро textual PE 2025–26 |
| **7** | [`report_reprompt_system_architecture_2026.md`](./report_reprompt_system_architecture_2026.md) | Архитектура textual bridge |

---

## Все отчёты в корне

### Bridge / re-prompter channels
- [`fundamental_questions_text_conditioning.md`](./fundamental_questions_text_conditioning.md) — фундаментальные вопросы (пересмотр после критики)
- [`ideas_t2i_conditioning_stage.md`](./ideas_t2i_conditioning_stage.md) — идеи связной прозой
- [`ideas_t2i_conditioning_narrative.md`](./ideas_t2i_conditioning_narrative.md) — шаблон (1)–(4), выбор лучшей, нарратив + план проверки
- [`training_bytedance_context_scaling.md`](./training_bytedance_context_scaling.md) — как учили в ByteDance Context Scaling
- [`take_should_we_train_reprompter.md`](./take_should_we_train_reprompter.md) — как учат репромптер в конкретных работах: данные, цифры, где ломается
- [`ideas_reprompter_training_bakeoff.md`](./ideas_reprompter_training_bakeoff.md) — сравнение SFT / RL / agents для re-prompter
- [`take_what_to_put_in_prompt.md`](./take_what_to_put_in_prompt.md) — какие поля и позиции дают выигрыш, чего не писать
- [`take_specify_a_vs_b.md`](./take_specify_a_vs_b.md) — можно ли сказать «указывать это лучше, чем то»: поиск по деревьям + протокол измерения
- [`take_sp_length.md`](./take_sp_length.md) — длина структурного промпта: что известно про NL, почему нельзя переносить напрямую, открытые дыры
- [`take_reprompt_format.md`](./take_reprompt_format.md) — формат записи re-prompt: какие оболочки пробовали, что работает, что изобрести
- [`take_reprompt_output_dofs.md`](./take_reprompt_output_dofs.md) — степени свободы на выходе репромптера: settled vs open
- [`take_prompt_compression.md`](./take_prompt_compression.md) — сжатие промпта как codec между двумя LLM
- [`literature_notes_user_survey.md`](./literature_notes_user_survey.md) — рабочий обзор статей (ваш проход)
- [`mechanism_stack_structured_reprompt.md`](./mechanism_stack_structured_reprompt.md) — стек механизмов структурного re-prompt (L0–L7) + контроли и лестница экспериментов
- [`open_questions_v2_and_latent_dualtrain.md`](./open_questions_v2_and_latent_dualtrain.md) — открытые вопросы Q7–Q18 + латентный канал с совместным обучением (программа E1–E7, шорт-лист)
- [`report_open_problems_autonomous_audit.md`](./report_open_problems_autonomous_audit.md) — **полный аудит открытых проблем (2026-08)**
- [`report_open_research_questions_reprompt_bridge.md`](./report_open_research_questions_reprompt_bridge.md) — короткая research agenda
- [`reading_list_reprompter_latent_and_alt_channels.md`](./reading_list_reprompter_latent_and_alt_channels.md) — статьи: латентный re-prompter + другие каналы
- [`report_reprompter_nontextual_channels.md`](./report_reprompter_nontextual_channels.md) — нетекстовые каналы enrichment → G
- [`report_bridge_methods_taxonomy.md`](./report_bridge_methods_taxonomy.md) — таксономия F1–F6 + pros/cons
- [`fundamental_papers_reprompt_reading_list.md`](./fundamental_papers_reprompt_reading_list.md) — textual PE ядро
- [`report_reprompt_system_architecture_2026.md`](./report_reprompt_system_architecture_2026.md) — архитектура textual bridge
- [`report_reprompt_systems.md`](./report_reprompt_systems.md) — широкий дайджест PE
- _(смежное)_ [`reading_list_latent_and_bridge_channels.md`](./reading_list_latent_and_bridge_channels.md), [`report_latent_transfer_agents_and_reprompt.md`](./report_latent_transfer_agents_and_reprompt.md) — MAS latent (не основной фокус)

### Длина промпта и captions
- [`relevant_papers_prompt_caption_design.md`](./relevant_papers_prompt_caption_design.md) — краткие P/M/R
- [`report_around_brack_2506_16679.md`](./report_around_brack_2506_16679.md) — вокруг Brack et al. (контролируемые captions)
- [`report_dalle3_prompt_reprompt_descendants.md`](./report_dalle3_prompt_reprompt_descendants.md) — потомки DALL·E 3 Better Captions
- [`combined_report_prompt_length_300.md`](./combined_report_prompt_length_300.md) — сводный отчёт (~300)

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

1. **Длина ≠ информация:** NL length saturates; масштабируется structured / image-grounded info (`2607.29679`). Рецепты train (Brack/i1/FIBO/SP) всё ещё без head-to-head.
2. **Bridge ≠ только текст:** F1 rewrite · F2 embeddings · F3 layout · F4 schema · F5 endogenous · F6 action — bakeoff @ matched FLOPs открыт.
3. **Re-prompt:** иногда вредит; predictive gating и oracle-gap — топ дырка; eval vs **original** prompt.
4. **Практика:** читать аудит → выбрать пакет A–E → не делать always-on aesthetic rewriter.

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
