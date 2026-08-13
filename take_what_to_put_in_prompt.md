# Что писать в промпте: какие поля и позиции дают выигрыш

Короткий тейк. Связано с packing-бюджетом (идея 4 в [`ideas_t2i_conditioning_narrative.md`](./ideas_t2i_conditioning_narrative.md)), field ablation Seed ([`training_bytedance_context_scaling.md`](./training_bytedance_context_scaling.md)) и стеком порядка ключей ([`mechanism_stack_structured_reprompt.md`](./mechanism_stack_structured_reprompt.md)).

---

## Проблема

Хочется cookbook: укажи объекты, сцену, камеру; не пиши «8k masterpiece»; важные слова ставь в начало. Таких гайдов много. Исследований, которые **причинно** меряют вклад типа факта или позиции при одном генераторе и одном наборе фактов, мало, и они не склеиваются в один рецепт: CLIP-эра про стиль, Seed про train loss на JSON, бенчмарки про ошибки генератора.

Три разных вопроса часто мешают в кучу:

1. **Какой тип факта** писать (сцена, бокс, цвет, relation, стиль).
2. **Куда его поставить** в строке или в схеме (начало / конец / фиксированный порядок блоков).
3. **Чего не дописывать**, потому что это вода, выдумка или хвост, который encoder уже не читает.

---

## Тейк

Рецепта «всегда пиши X» нет. Есть три корпуса, и переносить числа между ними нельзя.

Самое жёсткое причинное измерение — [Seed](https://arxiv.org/pdf/2607.29679) Appendix C.4: при полном L10 и одном бюджете обучения **глобальная сцена** бьёт по train loss сильнее всего, **боксы** вторые, а **depth / relationships / atmosphere-lighting** почти не двигают MSE. Это ответ про *marginal value при уже полном описании*, не про то, что класть первым в лимит 256 токенов, и не про human preference.

Порядок при тех же словах тоже не бесплатный: [Structured Captions](https://arxiv.org/abs/2507.05300) (`2507.05300`) — фиксированный шаблон subject → setting → aesthetics → camera сильнее shuffled тех же слотов. Ideogram держит порядок ключей как часть протокола. Это про геометрию записи, не про содержание.

Чего не писать, литература говорит увереннее, чем чего писать: **вода** (те же факты длиннее) не поднимает reconstruction (Seed Figure 3); **always-on aesthetic filler** и заполнение незаказанных слотов умеют опускать human alignment ([GenEval 2](https://arxiv.org/abs/2512.16853), TARA, VisualPrompter vs BeautifulPrompt); на CLIP-77 стиль в начале съедает субъект.

Открытая дыра — наша идея 4: никто не снял «что выбрасывать первым под токенный лимит» на одном evidence bundle. Seed говорит, какие поля ценны целиком; DetailMaster — что длинное хуже кодируется; пересечение не измерено.

---

## Что писать: типы фактов

Ранжирование только с указанием метрики и постановки.

| Тип | Когда даёт выигрыш | Когда почти мёртв / вреден | Якорь |
|-----|--------------------|----------------------------|--------|
| **Субъект / сущности** | Всегда базис. Конкретные существительные двигают картинку сильнее прилагательных | Размытый «beautiful scene» без объекта | Liu & Chilton CHI `2109.06977`; [Investigating Prompt Engineering](https://arxiv.org/abs/2211.15462) `2211.15462`; GenEval object |
| **Сцена / setting / global context** | Крупнейший одиночный вклад в train MSE при полном SP | Если сцена уже в base fields, повтор той же сцены водой | Seed C.4: снять scene → GPG минус 42, MSE плюс 35.3×10⁻⁴ |
| **Боксы / грубый layout** | Второй вклад в Seed; spatial в GenEval/CompBench | Если G не schema-native и координаты для него чужой язык | Seed C.4: снять bbox → MSE плюс 14.4×10⁻⁴; BBQ/GLIGEN — другой канал |
| **Атрибут, привязанный к владельцу** | Цвет/материал/форма *кого* — ось CompBench/GenEval binding | Атрибут без хозяина даёт leakage; «красивый, детальный» почти не бьёт | T2I-CompBench; Attend-and-Excite; PromptEnhancer visual attributes |
| **Счёт и отрицание** | Если пользователь это сказал — писать явно, модели это ломают | Дописывать «exactly three», когда пользователь не просил | GenEval counting; PromptEnhancer linguistic (negation) |
| **Relations** | Нужны бенчмаркам композиции | У Seed на полном L10 почти не двигают MSE (не больше 1.5×10⁻⁴) | Напряжение: train loss ≠ GenEval Position |
| **Стиль / lighting / camera / artists** | Сильно меняют картинку как *стиль*, не как adherence | Descriptors вроде «beautiful volumetric lighting» слабее nouns/artists; atmosphere в Seed C.4 почти мёртв для MSE | `2211.15462`; Structured Captions слот 3–4; Seed atmosphere |
| **Photography / focal length / «shot on…»** | Community-рецепт photorealism; у Seed это последний L10-слот | Нет field-ablation, что он покупает adherence; легко съесть бюджет | Seed Table 1 L10; гайды, не train-ablation |

Таксономии «что бывает в промпте», но не «что выигрывает»:

- Oppenlaender: subject, image prompt, style, quality boosters, repeating terms, magic terms (`2204.13988`) — практика CLIP-эры.
- DPG-Bench: entity, attribute, relation, global, other — оси **оценки**, не рецепт написания.
- PromptEnhancer AlignEvaluator: 24 keypoints в шести корзинах (linguistic, visual attributes, actions, relations, world knowledge, in-image text) — что rewriter должен *сделать явным*, если генератор это ломает, не список обязательных полей.
- VisualPrompter / TARA: атомы Entity / Attribute / Relation и type-aware ремонт — чинить только сломанное.
- CompGen (`2511.18378`): сложность сцены как \|O\|, \|A\|/\|O\|, \|R\|/\|O\| — учебный curriculum, не «пиши все три всегда».

---

## Куда ставить: позиции

| Наблюдение | Что из этого следует | Чего не следует |
|------------|----------------------|-----------------|
| Structured Captions: фиксированный порядок 4 блоков > shuffle тех же слотов | Если G учился на шаблоне, шаблон load-bearing | Что subject важнее camera по содержанию — там содержание одно, меняли только порядок |
| Ideogram JSON: порядок ключей часть протокола | Не переставлять ключи «для красоты» | Что JSON-ключи — универсальный закон для NL-моделей |
| CLIP-77 / GenEval 2: хвост отрезается | Субъект и жёсткие ограничения в начало, стиль в конец | То же правило для Qwen-VL / T5 с окном в тысячи токенов |
| Catastrophic neglect / attention dilution | Поздние и конкурирующие токены хуже доезжают | U-shape lost-in-the-middle из LLM-QA. Для T2I cross-attention это не тот же протокол |
| Seed JSON order может выучиваться (наш L2) | Shuffle блоков на train vs infer — отдельный тест | Пока не сделан hierarchical shuffle, «ставь scene первым» из C.4 не следует: C.4 снимал поля, не двигал их по строке |

---

## Чего не стоит писать

1. **Вода.** Те же сущности, больше связок. Seed Figure 3: NL-elaboration, reconstruction плоская.
2. **Quality boosters как always-on** («masterpiece, 8k, ultra detailed»). Таксономия Oppenlaender это описывает; TARA / VisualPrompter показывают, что aesthetic rewrite может сесть **ниже** сырого запроса на faithfulness.
3. **Выдуманные слоты.** Пользователь не просил layout — полный L10 его дорисует и схлопнет разнообразие / intent ([GenEval 2](https://arxiv.org/abs/2512.16853); вопрос Q7 про «свободно»).
4. **Физически нереализуемое.** FaithRewriter: text-only upsample дописывает невозможное.
5. **Мёртвый хвост схемы**, если сцена и объекты уже есть, а бюджет жёсткий: depth / relations / atmosphere у Seed почти не двигают MSE. Оговорка: для spatial-бенчмарка relations всё ещё цель, просто это не train-loss рычаг той же величины.
6. **Числа «для солидности»** (depth 0–255, точные px-боксы), если tokenizer и frozen TE их не резолвят — ложная точность, наш прежний тейк про numeric resolution.

---

## Что из этого брать в дизайн, не в гайд для пользователя

Для **re-prompter** при frozen G: сначала закрыть сущности, сцену и привязку атрибутов к владельцу; layout — если G schema-native; стиль/камеру — если не вытесняют субъект и пользователь это хотел. Не заполнять схему до конца «потому что поля есть». Гейт: не переписывать, если запрос уже объектный.

Для **train-подписей**: variable coverage лучше полного L10 всегда (Hunyuan/Brack vs Seed ladder). Field ablation Seed — аргумент не «выброси relations навсегда», а «не жди, что каждый слот одинаково кормит diffusion loss».

Для **нашего стенда**: cookbook закрыт не будет, пока нет packing под лимит (идея 4) и info-matched NL↔SP (идея 1). Без них «сцена важнее relations» остаётся фактом одной лаборатории на полном JSON и MSE.

Два якоря: Seed C.4 + Figure 3 (`2607.29679`); Structured Captions shuffle (`2507.05300`). Рядом, но про другое: `2211.15462` (nouns/artists/lighting vs descriptors) и PromptEnhancer (`2509.04545`) как карта failure modes, не как меню полей.
