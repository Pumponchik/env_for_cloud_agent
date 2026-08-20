# Степени свободы на выходе репромптера

Связано с [`take_reprompt_format.md`](./take_reprompt_format.md), [`take_sp_length.md`](./take_sp_length.md), [`take_prompt_compression.md`](./take_prompt_compression.md).

**Фиксируем пайплайн:** user → re-prompter → **артефакт** → text encoder → diffuser.  
Здесь только то, что можно варьировать в **артефакте** (сериализация / протокол / организация записи). Не: как учить re-prompter, какие факты выбирать, soft-tokens / KV (отдельные оси).

**Правило эксперимента:** сначала канонический proposition graph (одни факты), потом детерминированные сериализации. Без этого измеряете coverage, а не формат.

---

## Что уже ясно (локальный SOTA)

| Степень свободы | Вердикт | Где |
|-----------------|---------|-----|
| **Диалект = train** | Пиши так, как ел генератор. Plain на Ideogram не работает; Cosmos/FIBO/Seed schema-native | Ideogram 4 docs; Cosmos 3; FIBO; Seed |
| **Организация > shuffle** при matched facts | Фиксированный порядок блоков сильнее случайного | Structured Captions `2507.05300` |
| **Порядок ключей** на schema-native | Load-bearing, если на нём учили | Ideogram (CaptionVerifier); Seed канон |
| **Thinking не в encoder** | CoT — для rewriter; в diffuser только payload | Seed снимает thinking; PromptEnhancer выход = NL |
| **Verbose NL без новых фактов** | Saturation; length ≠ information | Seed Figure 3 / GPG–ED |
| **Схема как чеклист recall** | Structure поднимает покрытие полей, не «магия `{`» | Cosmos: free-form точный, но дырявый |
| **Адресуемые слоты** | Поле/ключ → edit locality | FIBO TaBR; Seed field edits |
| **Geometry / regions** | Работают, когда есть controller или train на числах | LMD, LayoutGPT, RPG, BBQ, Ideogram bbox |
| **JSON ≠ доказанный лучший синтаксис** | Нет info-matched bakeoff JSON vs YAML vs tuple vs markdown | Общий gap |

---

## Финальный список степеней свободы

Для каждой: **ось**, **статус** (`settled` / `open` / `boundary`), **что делать**.

### 1. Carrier (оболочка сериализации) — **open ★★★★★**

**Ось:** prose | fixed blocks | JSON | YAML | XML | markdown | tuples/listese | CSV | CSS-layout | S-expr | edge-list.

**Статус:** open. Structured wins как *организация*, не как *синтаксис*. Seed/FIBO/Ideogram не изолировали `{` от content.

**Что делать:** E1 info-matched carrier bakeoff на frozen encoder + E2 train-matched. Гипотеза: YAML/tuple дешевле JSON по токенам при том же AST.

### 2. Raw string vs parsed channels — **open ★★★★★**

**Ось:** encoder видит только текст | парсер поднимает entities/relations/regions в typed conditioning.

**Статус:** open и фундаментально. Без этого «structured prompting» неоднозначен.

**Что делать:** один и тот же артефакт: (a) raw string, (b) parse → sidecar channels. Если (a)≈(b) — структура = паттерн токенов; если (b)>> — нужен compiler, не «красивый JSON».

### 3. Schema topology — **частично settled**

| Подось | Статус | Комментарий |
|--------|--------|-------------|
| Nested vs flat | open | Seed/FIBO nested работают; depth не сравнили |
| Entity-centric vs property-centric | **open ★★★★** | Локальность атрибутов ↔ binding |
| Separate relation layer | directionally yes | Seed relations; tuple paper append |
| Explicit entity IDs | directionally yes | Seed/Ideogram; не изолировано |
| Map vs array of entities | open | порядок vs identity |
| Dedicated text/obj types | locally settled | Ideogram `obj`/`text` |
| Summary + detail | locally common | Ideogram `high_level_description`; CLIP early bias |

### 4. Sparse vs dense instance + absence — **open ★★★★**

**Ось:** emit all keys (FIBO-style) | filled-only | omit vs `null` vs `""` vs `unknown`.

**Статус:** open, high leverage. Пустые поля жрут бюджет и могут случайно кондиционировать.

**Что делать:** matched facts, варьировать только empty overhead + truncation survival.

### 5. Ordering / position — **частично settled**

| Подось | Статус |
|--------|--------|
| Fixed vs shuffle top-level | **settled** (Structured Captions; Ideogram) |
| Optimal fixed order (subject-first vs style-first…) | **open** — сравнили fixed vs random, не все перестановки |
| Summary first / last / both | **open** — CLIP early bias намекает на first |
| Entity order (salience, L→R, depth) | open |
| Truncation-aware order (core-first) | **open ★★★** practically |

### 6. Binding / reference protocol — **open ★★★★**

**Ось:** pronouns | repeated nouns | IDs | JSON pointers; attribute as adj vs slot; ownership as nest vs edge.

**Статус:** проблема известна (CompBench), лучший *формат* решения — нет. Anaphora почти наверняка вредна; ID+slots — гипотеза №1.

**Что делать:** crossed-color / ownership / part-whole scenes (E4), fixed seed, edit one slot.

### 7. Relation encoding — **open ★★★**

**Ось:** prose clause | binary tuple | entity-local link | separate edge list | n-ary event | both directions.

**Статус:** tuple append помогает SDXL (`2509.15962`), но дублирует info; нет bakeoff представлений.

### 8. Geometry dialect — **локально settled, универсально open**

**Ось:** qualitative prep | bbox (`xywh` / corners / CSS) | scale 0–1 / 0–1000 | grid | depth | occlusion graph.

**Статус:** Ideogram 0–1000 + key order — локальный контракт; BBQ numeric после train; LMD/LayoutGPT — controller. Универсальный диалект — нет.

### 9. Linguistic freedoms inside values — **open ★★★**

**Ось:** synonymy | articles | tense | voice | imperative vs declarative | controlled vocab | color names vs hex/RGB.

**Статус:** канон (enum/hex) снижает энтропию; frozen encoder может не знать канон. Ideogram/BBQ: hex/RGB локально.

**Граница:** убрать вольности = format; *какие* факты писать = content.

### 10. Density / compression / budget — **частично settled**

| Подось | Статус |
|--------|--------|
| Verbosity without new facts | **settled harmful** (Seed) |
| Token budget / packing | open ([`take_sp_length`](./take_sp_length.md)) |
| Key overhead (header+rows vs repeat keys) | **open ★★★** |
| BabelTele-like opaque compact | **open ★★** — LLM ok, T2I encoder неизвестно |
| Stopword pruning / telegraphic | open |

### 11. Multi-channel protocol — **частично settled**

| Подось | Статус |
|--------|--------|
| Positive / negative split | channel exists; best use model-specific |
| Global + regional subprompts | RPG/LMD — с controller |
| Attention weights `(word:1.2)` | только если front-end парсит |
| **Encoder-specific payloads** (CLIP short + T5 long) | **open ★★★★** на SD3/Flux-стеках |
| Thinking / chat residue in payload | almost certainly bad; rarely quantified |

### 12. Reliability hygiene — **engineering settled, science thin**

Validation strictness, unknown-key policy, duplicate keys, escape of literal text-in-image, no greetings around payload. Ideogram CaptionVerifier = практический SOTA гигиены; научных абляций мало.

### 13. Content (не формат — держать отдельно)

Число фактов, field coverage L5–L10, hallucination policy, aesthetic filler, world-knowledge expand. Seed GPG/ED — про это. **Не мешать с carrier bakeoff.**

---

## Shortlist: куда бить исследованием

1. **Info-matched carrier bakeoff** (JSON / YAML / markdown / tuple / blocks / prose)  
2. **Raw string vs parsed channels**  
3. **Entity-local IDs + binding layout**  
4. **Sparse filled-only + absence encoding**  
5. **Ordering under position bias + truncation**  
6. **Relation representation bakeoff**  
7. **Multi-encoder payload split**  
8. **Compact/model-native serialization** (осторожно: encoder ≠ LLM)

Последовательность: frozen E1 → train-matched E2 → cross-dialect matrix → binding/edit-locality → budget curves.

---

## Тейк

Степеней свободы на выходе репромптера много больше, чем «JSON или проза». Уже ясно: **совпади с train**, **не shuffle**, **не корми thinking**, **не лей воду**, **слоты помогают правке**. Не ясно и важнее всего: **какой carrier при тех же фактах**, **нужен ли парсер или хватит токенов**, **как кодировать binding/relations/absence**, **как резать бюджет**. Это и есть программа по формату артефакта — отдельно от обучения rewriter и от выбора фактов.
