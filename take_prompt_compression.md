# Сжатие промпта: как передать информацию от одной LLM к другой

Связано с [`take_reprompt_format.md`](./take_reprompt_format.md), [`take_sp_length.md`](./take_sp_length.md), [`report_latent_transfer_agents_and_reprompt.md`](./report_latent_transfer_agents_and_reprompt.md) и [`reading_list_latent_and_bridge_channels.md`](./reading_list_latent_and_bridge_channels.md).

Артефакты поиска: [`research/prompt-compression/`](./research/prompt-compression/).

---

## В чём задача

Репромптер — decoder LLM. Text encoder генератора — тоже языковая модель (T5, Qwen-VL, CLIP-text, иногда тот же семейный decoder). Сейчас канал почти всегда такой:

репромптер думает в hidden states → **декодирует в токены** → encoder **заново вчитывает** эти токены.

Сжатие здесь не «сделать текст короче, чтобы дешевле API». Это **codec**: какой bitrate и какой алфавит выбрать, чтобы вторая модель восстановила нужные факты. Survey [Beyond Tokens](https://arxiv.org/abs/2606.05711) формулирует то же для агентов: decode→tokens→encode теряет информацию и стоит compute.

Два ограничения, без которых NLP-сжатие нельзя слепо перенести на T2I:

1. **Получатель не обязан уметь «распаковать» телеграф.** LLMLingua рассчитывает, что GPT-класс восстановит выброшенные союзы. Frozen CLIP-77 или Qwen2.5-VL, на котором учили diffuser, этого может не делать.
2. **Пространства обычно разные.** Hidden Qwen3.5-397B ≠ hidden Qwen2.5-VL-7B ≠ T5-XXL. Без проектора KV/activations не стыкуются. [LI-DiT](https://arxiv.org/abs/2406.11831): naive LLM-as-encoder ломает alignment.

---

## Способы (по носителю)

### 1. Короче тот же дискретный текст

Алфавит не меняется: токены. Сжимаем redundancy.

**Выкинуть малоинформативные токены.** [LLMLingua](https://arxiv.org/abs/2310.05736) / [LongLLMLingua](https://arxiv.org/abs/2310.06839) / LLMLingua-2: маленький LM считает perplexity, выкидывает предсказуемое; до 20× на ICL/RAG. LongLLMLingua ещё переставляет куски, чтобы обойти lost-in-the-middle.

Для нашего JSON это почти «выбросить скобки, кавычки, служебные слова». Seed уже жмёт одинарные кавычки. Риск: encoder, который ел полный JSON, не узнает дырявый. На schema-native модели (Ideogram) сжатый JSON может стать невалидным.

**Пересказать короче на естественном языке.** Summarizer / «Learning to Compress Prompt in Natural Language Formats». Это не сжатие SP, а смена покрытия: легко выкинуть bbox и relations. Вода не помогает — мы это уже приняли; сжатие NL без потери фактов = packing coverage, не verbosity.

**Компактная сериализация.** YAML, markdown-список, s-expression при **тех же ключах**. Синтаксис дешевле JSON, алфавит всё ещё текст. Никто не снял bakeoff.

**Схема как сжатие.** JSON-чеклист сам по себе компрессор относительно прозы: именованный слот вместо предложения. Sparse filled-only (нет ключа = нет факта) — ещё один шаг.

Когда годится: разные модели, нужен audit, portable API. Потолок: дискретизация в BPE.

### 2. Мягкие токены (тот же decoder, другой алфавит)

Не слова, а k непрерывных векторов в пространстве **той же** модели.

- [Gisting](https://arxiv.org/abs/2304.08467) (Mu et al.): attention mask заставляет сжать prompt в gist-токены; до 26× на LLaMA и FLAN-T5.
- [ICAE](https://arxiv.org/abs/2307.06945): in-context autoencoder, memory slots.
- AutoCompressor (Chevalier et al.): рекурсивно сжимает контекст в summary vectors.
- Activation Beacon: сжимает KV в beacon-токены по ходу длинного контекста.

Для T2I ближайшие:

- [ELLA](https://arxiv.org/abs/2403.05135), SUR-adapter: LLM → connector → continuous conditioning, **без** выдачи rewritten text.
- [Think-Then-Generate](https://arxiv.org/abs/2601.10332): reasoning есть, в DiT идут embeddings.
- [SoftREPA](https://arxiv.org/abs/2503.08250): soft tokens для alignment text–image, не для сжатия re-prompt. Показывает, что DiT ест непрерывное.
- [FIBO DimFusion](https://arxiv.org/abs/2511.06876): длинные промежуточные слои LLM **склеивают по embedding-dim**, число токенов не растёт. Это сжатие *внутри* encoder генератора, не между двумя LLM.

Когда годится: получатель — та же модель или есть обученный decoder слотов. Не годится из коробки: промптер Qwen3.5, encoder CLIP.

### 3. Hidden / KV напрямую (минуя decode)

Алфавит = активации отправителя.

- Coconut: last hidden снова на вход, latent CoT внутри одной модели.
- Cache-to-Cache, KVComm, Interlat, LatentMAS: LLM↔LLM через KV/hidden. Interlat заявляет сильное ускорение за счёт сжатия last hidden.

Для стека Seed это соблазнительно: промптер Qwen3.5, encoder Qwen2.5-VL — одно семейство, но **не одни веса и не один размер**. Нужен обученный проектор слой-к-слою. Без него это другой язык.

Когда годится: white-box, один (или aligned) backbone, не нужен human-readable mid-artifact. Когда нет: API без hidden, безопасность (latent channels атакуемы), разные архитектуры без проектора.

### 4. Выученный интерлингва / проектор

Отдельная маленькая сеть: hidden_A → conditioning_B.

Это ELLA/SUR в чистом виде. Учить на: «предскажи эмбеддинг, который даёт эталонная подпись» (дистилляция encoder) плюс опционально diffusion loss. [`open_questions_v2_and_latent_dualtrain.md`](./open_questions_v2_and_latent_dualtrain.md) описывает этот коннектор как стадию 1 dual-train.

Потолок качества — насколько пространства вообще стыкуются. LI-DiT предупреждает: просто взять LLM как encoder мало.

### 5. Сжатие не текста, а набора фактов

Feature selection / packing: меньше **ключей**, не меньше букв. Это другой codec — typical set визуальных переменных. Связано с [`take_specify_a_vs_b.md`](./take_specify_a_vs_b.md). На дискретном канале это лучший bitrate: каждый оставшийся токен несёт слот, а не «the» и `{`.

---

## Что из NLP-сжатия переносится, а что нет

| Метод | Переносится на T2I re-prompt? |
|-------|-------------------------------|
| LLMLingua token drop | Только если encoder генератора умеет читать дырявый текст **того же диалекта**, на котором учили. Для schema-JSON — сначала проверить валидность схемы. |
| NL summarization | Легко спутать с выкидыванием фактов. Мерить атомами fact table, не длиной. |
| Gist / ICAE | Да, если сжимать **внутри encoder генератора** (один decoder). Между промптером и чужим encoder — нет без проектора. |
| KV / hidden inject | Да при одном семействе + проектор (Qwen→Qwen-VL). Нет для FLUX+T5 и внешнего GPT-rewriter. |
| SoftREPA-класс | Чинит alignment на стороне генератора, не заменяет re-prompt. Можно ставить *после* любого канала. |
| DimFusion | Сжатие длинного LLM-encoder внутри генератора; ортогонально сжатию выхода промптера. |

Rate-distortion рамка есть: *Fundamental Limits of Prompt Compression* (black-box). Для нас искажение = падение atom compliance / reconstruction, не GSM8K.

---

## Практическая развилка для нашего стека

Три рабочих протокола, от самого portable к самому плотному.

**A. Дискретный codec.** Промптер пишет IR (граф/схема). Компилятор сериализует в диалект генератора максимально плотно (sparse YAML/JSON). Сжатие = packing полей + дешёвый синтаксис. Audit полный. Это продолжение формата и длины SP.

**B. Soft slots на стороне получателя.** Encoder генератора учит gist/memory: длинный SP сжимается в k токенов *перед* DiT. Промптер по-прежнему пишет текст. Выигрыш — compute DiT и окно encoder, не латентность LLM-rewrite.

**C. Прямой канал.** Last hidden / KV промптера → проектор → conditioning DiT. Текст наружу только короткий summary для человека. Нужны веса промптера, стыковка размерностей, калибровка. Ближайшие якоря: ELLA, Think-Then-Generate, Interlat как protocol.

Гибрид, который обычно лучше продукта: человек и отладка видят слой A; генератор ест B или C.

---

## Что придумать (не закрыто)

1. **Gist внутри Qwen-VL encoder** на Seed-SP: k слотов vs полный JSON, reconstruction/compliance. Это B на открытом стеке.
2. **Проектор Qwen3.5 last hidden → Qwen2.5-VL prefix**, teacher = эмбеддинг канонического SP. Сравнение с текстовым JSON при matched facts.
3. **LLMLingua на SP** с ограничением «не ломать ключи»: сжимать только values, ключи неприкосновенны. Проверка, читает ли schema-native модель дырявые значения.
4. Не ставить SoftREPA и textual PE в один bakeoff без метки канала: они чинят разные звенья.

---

## Тейк

С учётом двух decoder'ов сжатие — это выбор алфавита канала. Текст: portable, lossy, вторая модель должна уметь распаковать ваш диалект. Soft/gist: плотный, но внутри одной модели. Hidden/KV: ещё плотнее, нужен проектор и white-box. Схема и packing сжимают **факты**, не буквы — это ортогональный и часто более честный рычаг, чем LLMLingua на прозе.

NLP-сжатие (Lingua, Gisting, ICAE) не отвечает «выброси половину JSON, картинка останется». Оно отвечает «вторая *такая же* LLM восстановит связность». У T2I получатель другой и часто заморожен. Поэтому сначала решить, стыкуются ли пространства; потом выбирать codec. Подробная карта latent-канала уже в [`report_latent_transfer_agents_and_reprompt.md`](./report_latent_transfer_agents_and_reprompt.md); здесь — как это стыкуется со сжатием.
