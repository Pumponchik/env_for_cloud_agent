# Формат re-prompt: что пробовали, что работает, что придумать

Вопрос не «учить ли репромптер» ([`take_should_we_train_reprompter.md`](./take_should_we_train_reprompter.md)) и не «какие поля писать» ([`take_what_to_put_in_prompt.md`](./take_what_to_put_in_prompt.md)). Здесь только **как записать** уже выбранные факты: проза, шаблон, JSON, граф, регионы, латенты.

Артефакты поиска: [`research/reprompt-format/`](./research/reprompt-format/).

---

## Как искали

arXiv: `structured caption`, `JSON caption`, `YAML prompt text-to-image`, `markdown structured`, `XML prompt image`, `scene graph prompt`, `LayoutGPT`, `LLM-grounded Diffusion`, `PromptEnhancer`, `VisualPrompter`, `TIPO`, `BeautifulPrompt`, `FIBO`, `Recaption`. Плюс документы Ideogram 4, Cosmos 3, Seed.

YAML / XML / markdown как формат conditioning для T2I **почти не встречаются**. Всё живое крутится вокруг прозы, четырёхблочного шаблона, JSON-схемы, региональных подпромптов и нетекстовых каналов.

---

## Какие форматы уже пробовали

Семь семейств. Внутри семейства отличаются схемой, не идеей.

### 1. Плотная проза (natural language recaption)

Репромптер пишет длинный абзац в стиле обучающих подписей.

- [Improving Image Generation with Better Captions](https://cdn.openai.com/papers/dall-e-3.pdf) (DALL·E 3): GPT разворачивает короткий запрос в подробную NL-подпись.
- [A Picture is Worth a Thousand Words: Principled Recaptioning…](https://arxiv.org/abs/2406.07516) (RECAP) и [What If We Recaption Billions…](https://arxiv.org/abs/2406.08418): синтетические NL-подписи на train.
- Wan `prompt_extend`, FLUX.2 prompt upsampling: то же на инференсе, с оговоркой «для `a red car` почти не нужно».
- [PromptEnhancer](https://arxiv.org/abs/2509.04545): цепочка рассуждения, **выход для генератора — обычный текст**, не JSON. CoT нужен переписывателю, не диффузору.
- [TIPO](https://arxiv.org/abs/2411.08127): presampling в духе тегов Stable Diffusion (subject, quality, style).
- [BeautifulPrompt](https://arxiv.org/abs/2312.06027) / Promptist: эстетический NL. На чужих таблицах (TARA) сажает semantic accuracy ниже сырого запроса.

Что это умеет: попасть в распределение train-captions. Что ломает: вода, aesthetic filler, нет явной привязки атрибута к объекту.

### 2. Фиксированный прозаический шаблон (блоки, не дерево)

Один абзац, но всегда в одном порядке слотов.

- [Structured Captions Improve Prompt Adherence…](https://arxiv.org/abs/2507.05300): четыре части — subject, setting, aesthetics, camera. Shuffle тех же слотов хуже фиксированного порядка. Это самое чистое доказательство, что **организация записи** (не только набор слов) load-bearing, если модель на шаблоне училась.

Дешевле JSON: нет скобок и ключей. Слабее JSON: нет id объекта, нет боксов, нельзя точечно править одно поле.

### 3. Типизированный JSON (схема = вход генератора)

Репромптер — компилятор в схему, на которой учили diffuser.

- Seed, [Scaling Properties of Text Conditioning](https://arxiv.org/pdf/2607.29679): nested JSON (intent, scene, elements с bbox/depth, relationships, atmosphere, photography). Сериализация **компактный JSON в одинарных кавычках**, чтобы экономить токены. Thinking репромптера на инференсе **снимают**, в diffuser идёт только JSON.
- [FIBO](https://arxiv.org/abs/2511.06876): длинный JSON (~1160 токенов), те же поля всегда присутствуют; disentanglement «поменял ключ — поменялся один фактор».
- [Cosmos 3](https://arxiv.org/html/2606.02800): авторы явно пишут, что ушли с dense free-form на structured JSON, потому что свободная проза **точная, но неполная** (низкий recall). Upsampler обязан выдать JSON; plain text для генератора не канон.
- Ideogram 4 (docs): `high_level_description`, `style_description`, `compositional_deconstruction` (background + elements с bbox). **Порядок ключей часть протокола**; verifier это проверяет. Magic Prompt = LLM, который пишет этот JSON. Plain text «will not work».

Общее: схема дисциплинирует покрытие. Цена: хрупкость оболочки (синоним ключа, другой порядок), расход токенов на синтаксис, LLM должен уметь заполнить схему без выдумок.

### 4. Атомы / граф, потом сборка в текст

Промежуточное представление — не промпт для диффузора, а список утверждений.

- DSG, TIFA: граф entity–attribute–relation для **оценки**.
- [VisualPrompter](https://arxiv.org/abs/2506.23138): атомы, VLM смотрит картинку, дописывает пропущенное.
- [TARA](https://arxiv.org/abs/2607.18724): атомы чинятся type-aware операторами, затем **компилируются в один короткий исполняемый промпт**. Формат для генератора снова NL, не JSON. Запрет aesthetic filler в инструкции компилятора.

Полезно как язык ремонта. Само по себе не отвечает, в каком синтаксисе кормить diffuser.

### 5. Layout / регионы как отдельный канал

Текст плюс геометрия не внутри JSON-строки, а как второй вход.

- [LayoutGPT](https://arxiv.org/abs/2305.13655): LLM пишет CSS-подобный layout.
- [LLM-grounded Diffusion](https://arxiv.org/abs/2305.13655) (LMD): LLM планирует боксы, потом grounded generation.
- RPG (*Mastering Text-to-Image Diffusion: Recaptioning, Planning, and Generating with Multimodal LLMs*): recaption + план **региональных** подпромптов + complementary regional diffusion.
- Reve 2.0: иерархический layout-посредник.
- GLIGEN / BBQ: боксы как отдельный conditioning, не как числа в тексте.

Это уже не «формат re-prompt», а смена канала. Имеет смысл, если генератор schema-native к layout. Если боксы сериализованы цифрами в JSON, а encoder их не резолвит, это ложная точность (наш старый тейк).

### 6. Не текст

- [SoftREPA](https://arxiv.org/abs/2503.08250): soft-токены, без переписывания подписи.
- Z-Image: выходы PE скормили генератору на train, на инференсе переписыватель выкинули.

Формат re-prompt тогда «никакой»: вопрос снимается.

### 7. Гибрид thinking + payload

Seed и Qwen-Image PE: LLM пишет рассуждение, потом структурированный ответ. Для **генератора** формат — только payload (JSON или NL). Thinking — формат **репромптера**. Смешивать их в одном входе diffuser почти никто не делает (и Seed специально снимает thinking).

---

## Что лучше работает (с ярлыком постановки)

Честного bakeoff «JSON vs YAML vs markdown vs NL при тех же фактах» **нет**. Есть такие факты.

**Формат должен совпадать с train.** Ideogram: plain не работает. Cosmos: eval-промпты тоже прогоняют через rewriter в JSON. Seed matched NL слабее SP, но там ещё и разное покрытие фактов. Практический закон сильнее любого «JSON magically better»: *пиши так, как модель ела*.

**Схема повышает recall, не магию скобок.** Cosmos: free-form точный, но дырявый; predefined structure заставляет закрыть объекты, атрибуты, relations, камеру. Это аргумент за **чеклист полей**, не за JSON как синтаксис. Тот же чеклист можно сериализовать YAML или четырьмя предложениями.

**Порядок записи load-bearing, если на нём учили.** Structured Captions: шаблон > shuffle. Ideogram: порядок ключей в `style_description` и внутри element. Seed сериализует канонически. Если переставлять ключи «для красоты» на schema-native модели — это другой промпт.

**CoT не является форматом картинки.** PromptEnhancer выигрывает наградой AlignEvaluator, не тем, что генератор читает рассуждение. Seed thinking снимает. Не кормить diffuser романом «сначала я подумал…».

**Эстетический формат вредит верности.** BeautifulPrompt / TIPO / quality boosters на TARA ниже raw prompt. Формат «masterpiece, 8k, trending» — отдельный вредный диалект, не нейтральная проза.

**Компактность JSON уже осознана.** Seed: single-quote JSON, чтобы не жечь токены на двойные кавычки. FIBO/Cosmos жрут 1000+ токенов и ставят отдельную архитектуру (DimFusion) или длинный encoder. Значит синтаксис **стоит**. Никто не сравнил тот же набор ключей в YAML или в listese.

**JSON выигрывает как UX правки**, не обязательно как эмбеддинг. FIBO: поменял одно поле, seed тот же, меняется один фактор. TARA/VisualPrompter: чинить атомы проще, чем абзац. Это свойство **адресуемых слотов**, его можно сохранить в любом типизированном формате.

---

## Чего нет

1. Info-matched сравнение оболочек: JSON vs YAML vs markdown-список vs NL-парафраз vs s-expression, **одни факты, один генератор**.
2. Sparse schema: отсутствуют пустые ключи vs всегда полный L10 с null.
3. Синонимы ключей (`bbox` / `position` / `box`) на frozen schema-native модели.
4. Гибрид: глобальная проза + структурированный список объектов (средний путь между Structured Captions и Seed).
5. Нативная типизация в encoder (слот как special token), а не JSON как обычный текст.
6. Формат под packing: какой синтаксис дешевле по токенам при том же coverage (связано с [`take_sp_length.md`](./take_sp_length.md)).

---

## Что можно придумать

Не «ещё один JSON». Дыры выше — это и есть программа.

**1. Компактная сериализация при тех же ключах.**  
Тот же evidence: канонический JSON; YAML; markdown-список (`## scene` / `- obj id=…`); NL-парафраз без слотов; keys-only. Frozen generator, атомы против fact table. Гипотеза: YAML/markdown выиграют у JSON по качеству-на-токен, проиграют JSON по точечной правке только если модель выучила скобки, а не ключи.

**2. Sparse filled-only.**  
Репромптер пишет только заказанные и уверенные поля. Пустые слоты не сериализуются. Против полного L10 с выдуманными atmosphere/depth. Это стык с feature selection: формат поддерживает отсутствие ключа как first-class, а не «null в обязательной схеме».

**3. Двухслойный гибрид.**  
Слой A: 1–2 предложения intent (как Ideogram `high_level_description` / Structured Captions subject+setting). Слой B: типизированный список объектов с привязкой атрибутов. Стиль и камера — опциональный хвост. Мотивация: глобальное читает любой encoder как прозу; binding нуждается в слотах; JSON на всю сцену жрёт бюджет на `{` и `"intent"`.

**4. Слоты как токены, не как текст.**  
Вместо строки `"bbox": [12,40,80,90]` — special tokens `<obj 3>` + непрерывный вектор геометрии (или дискретная сетка 3×3 / 9×9, как spatial variants Seed). Текст остаётся для атрибутов. Это ближе к LayoutGPT/GLIGEN, но с тем же re-prompter UX.

**5. Формат ремонта ≠ формат генерации.**  
Внутри репромптера держать атомный граф (как TARA/DSG). В генератор компилировать **тот синтаксис, на котором учили diffuser**. Компилятор — дешёвое детерминированное правило, не второй LLM. Тогда можно менять выходной диалект (JSON Ideogram vs проза FLUX) без переучивания «понимания сцены».

**6. Канонический порядок как часть схемы, не как эстетика.**  
Если учим на SP — зафиксировать порядок ключей и тестировать shuffle как калибратор хрупкости. Если учим на NL — не притворяться, что JSON-порядок перенесётся.

---

## Энтропия vs выразительность: как сравнивать форматы

Вопрос «какой формат re-prompt» удобнее разложить на две оси, которые литература почти не сравнивает напрямую.

**Выразительность (semantic expressiveness)** — сколько *разных смыслов* можно записать без потери. Для нашей задачи нужен формат, который не ограничивает домен: произвольные объекты, атрибуты, отношения, стиль, камера, текст на картинке.

**Энтропия на факт (entropy per fact)** — сколько *лишней неопределённости* несёт запись при фиксированном наборе фактов: синтаксис, синонимы, порядок слов, вода, неоднозначная привязка атрибута к объекту.

Важно: это **не одно и то же**. NL теоретически безграничен по выразительности, но имеет **высокую энтропию на факт** — один и тот же факт можно написать десятками способов, и encoder не знает, какой из них «канон». JSON с фиксированной схемой имеет **низкую энтропию на факт** (ключи и типы предсказуемы), но выразительность ограничена **схемой**, а не синтаксисом: если в схеме есть nested `elements[]` с `relationships[]`, можно описать почти любую сцену.

### Карта форматов

| Формат | Выразительность | Энтропия на факт | Простота для LLM/человека | Ограничения |
|--------|-----------------|------------------|---------------------------|-------------|
| **NL (проза)** | Максимальная (любой смысл) | Высокая: синонимы, порядок, вода, неявный binding | Привычно, но трудно править точечно | Нет адресуемых слотов; «красная машина слева от дома» — неясно, что красное |
| **Фиксированный шаблон блоков** | Средняя (слоты без id) | Средняя: порядок фикс, но лексика свободна | Очень просто | Нет id объектов, bbox, relations между конкретными id |
| **JSON / typed KV** | Высокая (если схема богатая) | **Низкая**: канонические ключи, типы, порядок | JSON — де-факто стандарт для LLM structured output | Синтаксис дорог по токенам (`{`, `"`, `:`) |
| **YAML / markdown-список** | ≈ JSON (тот же AST) | **Ниже JSON** на те же ключи: меньше кавычек и скобок | YAML читается проще; markdown — ещё проще | Хрупкость отступов (YAML); нет стандарта в T2I |
| **Tuple / listese** | Средняя (flat relations) | **Очень низкая**: `(obj, attr, value)` | Компактно, но nested сцены неудобны | [Structured Information…](https://arxiv.org/html/2509.15962): tuples для spatial relations, append к NL |
| **Scene graph / atom IR** | **Максимальная для relations** | Низкая в IR; зависит от сериализации | Не для генератора напрямую — нужен компилятор | DSG/TIFA/VVisualPrompter/TARA: IR → NL или JSON |
| **Danbooru-теги** | Низкая (атрибуты, не композиция) | Очень низкая | Простейший | Плохо для relations, narrative, camera |
| **Soft tokens / latents** | Зависит от обучения | **Минимальная** (непрерывный канал) | Не human-readable | Нужен aligned backbone; нет audit trail |

**JSON vs NL при тех же фактах** — интуиция пользователя верна по *направлению*, но литература почти никогда не изолирует синтаксис:

- Seed ([Scaling Properties…](https://arxiv.org/abs/2607.29679)): SP = JSON с именованными полями. NL и SP **не лежат на одной length–loss кривой**; GPG/ED растут у SP, а у NL — нет, даже когда длина растёт. Но contrast = content + organization jointly, не «JSON vs проза при matched facts».
- Cosmos 3: free-form NL **точный, но неполный** (низкий recall); JSON как **чеклист** заставляет закрыть поля. Аргумент за структуру, не за скобки.
- FIBO: long JSON (~1160 tok) с полной semantic coverage; disentanglement «один ключ → один фактор».
- Ideogram 4: plain text **will not work** — генератор schema-native.
- [Structured Captions](https://arxiv.org/abs/2507.05300): четыре блока прозы **без JSON**; shuffle хуже фиксированного порядка → **организация** load-bearing.

### Что говорит теория информации (и что не говорит)

**Auth-Prompt Bench / NoxEye** ([OpenReview](https://openreview.net/pdf?id=EYwbHIXJ1k)): prompt entropy \(H(P)\) для **стабильности** T2I — экспертные промпты концентрируют информацию, новичковые размыты. Это про *качество пользовательского ввода*, не про сравнение JSON vs YAML.

**GPG и ED** (Seed): operational proxies для *image-grounded information* в caption. GPG — masked log-likelihood gain под VLM; ED — precision/recall атрибутов. Они измеряют **сколько фактов**, не **как упакованы**. Формат влияет на них косвенно: схема заставляет написать больше фактов (recall), канонические ключи убирают paraphrase-варiance (precision).

**LLMLingua / prompt compression** ([take_prompt_compression.md](./take_prompt_compression.md)): сжатие = codec между LLM. Для T2I получатель другой; выкинуть `{` и `"` рискованно, если encoder учился на полном JSON. Seed уже использует **single-quote JSON** как осознанную экономию токенов.

### Ранжирование под ваши критерии

Критерии: (1) минимальная энтропия на факт, (2) максимальная выразительность, (3) без ограничений по смыслам, (4) простота.

**Практический оптимум для re-prompter → text encoder:**

1. **Typed key-value с фиксированной схемой** (JSON или YAML) — лучший баланс. JSON проще для LLM (structured output API, verifier, JSON Schema). YAML/markdown-list — кандидат на **меньшую syntactic entropy** при том же AST; bakeoff не проводился.

2. **Atom/scene-graph IR внутри репромптера + компилятор в диалект генератора** — максимальная выразительность для relations и repair (TARA, VisualPrompter); снаружи — JSON или NL, что съест diffuser.

3. **Sparse filled-only** — отсутствие ключа = «не заказывали / не уверены», не `null` в обязательной L10-схеме. Снижает энтropию (нет шума от выдуманных atmosphere/depth) и токены.

4. **Гибрид**: 1–2 предложения intent (NL) + typed list объектов. Глобальный контекст encoder читает как прозу; binding — через слоты.

**Не подходят как единственный формат:**

- **Чистая NL** — максимальная энтропия; Seed показал saturation при verbosity без новых фактов.
- **Только теги** — низкая энтropия, но потолок выразительности.
- **Soft tokens** — минимальная энтropия канала, но теряем простоту и audit; нужен train.

### Чего нет в литературе (и что можно сделать)

Прямого исследования «**info-matched** JSON vs YAML vs markdown vs tuple vs NL-paraphrase vs s-expression, один генератор, frozen weights» **нет**. Ближайшие прокси:

| Работа | Что сравнивает | Чего не хватает |
|--------|----------------|-----------------|
| Seed 2607.29679 | NL ladder vs SP ladder L5–L10 | Matched facts, другой синтаксис при тех же ключах |
| FIBO 2511.06876 | Short NL vs long JSON | Разное coverage, не только оболочка |
| Structured Captions 2507.05300 | Fixed template vs shuffle | Нет JSON arm |
| Tuple spatial 2509.15962 | NL + tuples vs NL | Только spatial, append не replace |
| Cosmos 3 | Free-form vs JSON | Recall vs precision, не entropy bakeoff |

**Дешёвый эксперимент:** один набор атомов (50–100 сцен) → сериализовать в 5–6 оболочек → frozen Qwen-Image / Ideogram → compliance + tokens + GPG-proxy. Гипотеза: YAML/markdown < JSON < NL по tokens/fact при равном compliance; JSON ≈ YAML если encoder не overfit на `{`.

---

## Тейк

Форматов re-prompt на практике три рабочих и несколько боковых. Рабочие: **плотная проза под train-captions**; **фиксированный шаблон блоков**; **JSON-схема, на которой учили генератор**. Боковые: атомы для ремонта, регионы/боксы как второй канал, soft-токены вместо текста.

«JSON лучше прозы» в литературе почти всегда означает «схема заставила написать больше фактов» или «генератор ел только JSON». Cosmos это формулирует прямо: структура нужна как **чеклист покрытия**. Structured Captions показывают, что даже без JSON порядок блоков меняет adherence. Seed жмёт JSON в одинарные кавычки — синтаксис уже признан дорогим.

Придумать имеет смысл не восьмую схему полей, а **оболочку при тех же фактах**: компактная сериализация, sparse слоты, гибрид проза+список объектов, компилятор из атомного IR в диалект конкретного генератора. Это дешёвый эксперимент на frozen модели и прямой сосед идеи 1 (info-matched NL↔SP) и packing.
