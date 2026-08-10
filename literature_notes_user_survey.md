# Обзор статей (рабочие заметки)

Ниже собран ваш проход по литературе: что прочитали, что не про то, какие числа и выводы важны, и как это стыкуется с нашими идеями. Формулировки поправлены только для читаемости; смысл и скепсис сохранены.

Базовая статья по дизайну synthetic captions: [How to Train Your Text-to-Image Model (Brack et al.)](https://arxiv.org/abs/2506.16679) (`2506.16679`) — её часто цитируют; у нас это якорь по выбору подписей для обучения.

---

## 1. Подписи, длина, распределение train/infer

### DALL·E 3
https://cdn.openai.com/papers/dall-e-3.pdf  

Рецепт, который все потом повторяют: обучить captioner на длинные детальные синтетические подписи к train-картинкам; на inference — LLM prompt upsampler, который переписывает короткий user prompt в стиль train-подписей. В самом PDF мало инженерии самой caption-модели — важнее постановка «выровнять inference под train distribution».

### RECAP — A Picture is Worth a Thousand Words
https://arxiv.org/abs/2310.16656  

Ablation short / long / mix в режиме CLIP-77:
- short (1–2 предложения) — лучше FID, быстрее сходимость;
- long — лучше семантика, хуже FID;
- mix 50/50 — лучший баланс;
- подписи длиннее 77 токенов почти отбрасывались (меньше 1%).

Вывод под жёсткий бюджет энкодера: mix short+long лучше любого одного режима. Имеет смысл смотреть, как у них устроен paraphraser и кого они цитируют.

### Brack et al. — How to Train…
https://arxiv.org/abs/2506.16679  

Базовая открытая работа по дизайн-выборам synthetic training captions (плотность, вариативность длины и т.д.). То, на что опираются последующие рецепты.

### i1 — Simple and Fully Open Recipe
https://arxiv.org/abs/2606.11289  

Проблема: SOTA T2I не раскрывают данные и ablation.  
Метод: открытый рецепт, T5Gemma-2B с усечением до 256 токенов; контролируемые опыты по энкодерам, стратегиям подписей, смесям данных. Ключевая ablation: доля длинных подписей 0–100%; GenEval на оригинальных / повторённых / переписанных промптах.  
Результат (как вы зафиксировали): обучение на длинных даёт слабо на коротких GenEval-промптах (~0.17), лучше при повторе короткого ×12 (~0.49), ещё лучше при LLM-rewrite (~0.73).  
Учат на заранее сгенерированных подписях, меняя процент длинных и коротких; правый столбец про **инференс** на GenEval, не про смену обучения. Датасет в их постановке — ImageNet-22K-классный масштаб/рецепт.  
**Вывод для нас:** учиться на длинных и на inference удлинять/reprompt’ить до train-распределения, а не учить на коротких «под пользователя».

### FIBO — Generating an Image From 1,000 Words
https://arxiv.org/abs/2511.06876  

Ablation long structured vs short на одном backbone. Train captions порядка ~1160 токенов в среднем. Long structured быстрее сходятся, лучше FID и контролируемость. При тысячетокенном режиме нужна архитектура вроде DimFusion, иначе attention дорожает; TokenFusion ещё дороже.  
**Важно:** сравнение снова «богатый structured vs короткий», не matched semantics — тот же класс confounds, что у Seed.

### HunyuanImage 3.0
https://arxiv.org/abs/2509.23951  

Compositional Caption Synthesis: семплирование полей → длина примерно от 30 до 1000 слов, EN/ZH. Длина и паттерн намеренно варьируются на train. На infer опциональный CoT think_recaption.  
**Вывод:** широкополосная рандомизация длины может снизить нужду в обязательном rewriter.

### PixArt-α → PixArt-Σ
https://arxiv.org/abs/2310.00426 / https://arxiv.org/abs/2403.04692  

Линия denser / better captions и масштабирования DiT — исторический фон к «длинным подписям помогают».

### SD3 / scaling + rectified flow
https://arxiv.org/pdf/2403.03206  

Законы скалирования, rectified flow, SD3 — про backbone и training recipe, не про re-prompt как таковой; держим как контекст генератора.

### Старый курьёз: Faster R-CNN боксы
https://arxiv.org/pdf/2006.11807  

По сути: детектят боксы и описывают каждый — ранний вкус «структура + локальные описания», забавно рифмуется с современными SP с bbox.

### Fingerprints — отпечатки разных caption-моделей
https://arxiv.org/pdf/2602.22734  

Как разные модели подписей оставляют характерный след в T2I. Полезно помнить, когда выбираем captioner для train-данных: меняем не только «длину», но и стиль источника подписей.

---

## 2. Re-prompt / обучение переводчика user → conditioning

### Input-Side Inference-Time Scaling
https://arxiv.org/abs/2510.12041  

Замороженный генератор, DPO на re-prompter. Заметили: длина растёт, додумываются элементы и отношения. Можно смотреть устройство paraphraser’а и их citation tree. Aesthetic-награда легко ломает alignment (это важный негативный урок для RL-ветки).

### PromptEnhancer
https://arxiv.org/abs/2509.04545  

SFT → GRPO, AlignEvaluator по fine-grained ошибкам. Классика RL-лагеря external rewriter.

### APE — Agentic Prompt Enhancer
https://arxiv.org/pdf/2606.00204  

Небольшие SLM как trainable enhancers (SAPE / MAPE). MAPE: выбор семантических полей → rewrite полей → compose. Учат через GRPO, генератор не трогают. Мотивация из multi-agent литературы (CAMEL, AutoGen, …).  
По их словам, GRPO-enhancer лучше снимает расплывчатость, заземляет абстракции в визуально реализуемое и меньше уходит в overthinking / semantic drift.

### VisualPrompter
https://arxiv.org/pdf/2506.23138  

Training-free: атомы Entity / Attribute / Relation → LLM генерирует вопросы → VLM отвечает по картинке → правки промпта в цикле.

### TARA — Type-Aware Repair Allocation
https://arxiv.org/pdf/2607.18724  

Близко к VisualPrompter: улучшили схему типов вопросов/ремонта, выиграли по метрикам. Post-hoc repair после генерации, не predictive «нужен ли PE заранее».

### Think-Then-Generate
https://arxiv.org/pdf/2601.10332  

Thinking → перепись промпта; в DiT идут **эмбеддинги** модели, которая думала/переписывала (не обязательно текстовый продукт). VLM на SFT под Think-Then-Rewrite; совместно с генератором ещё и GRPO. Это мост между «re-prompt текстом» и «conditioning эмбеддингами».

### Seed — Scaling Properties of Text Conditioning
https://arxiv.org/pdf/2607.29679  

Ввели GPG и ED; loss связан с информативностью conditioning. Diffuser на SP, prompter лестницей SFT → cold-start → OPSD (+ agentic).  

**Ваша критика matched NL (её сохраняем как основу идеи 1):**  
Фиксировали длины для NL и SP «из одного описания», но рост NL — вода и переформулировки, рост SP — новые поля (bbox, layout, …). Информативность SP выше. Пример в духе Small NL «pineapple + beer bottles» против богатого SP это подсвечивает.  
**Вопрос, который вы ставите и который мы берём в работу:** что будет, если тот же JSON перевести в текст и так же явно писать bbox, color, position — даст ли структура прирост сама, или достаточно той же семантики в NL.

Подробный разбор их обучения: [`training_bytedance_context_scaling.md`](./training_bytedance_context_scaling.md).

---

## 3. Похоже на соседние темы, но не про классический re-prompt

### UniFusion / VLM вместо T5+CLIP+VAE
https://arxiv.org/pdf/2510.12789  

Большинство диффузоров: текст отдельно (T5/CLIP), картинка через VAE. Здесь — замороженная мультимодальная модель (InternVL / Gemma-класс) как единый conditioning path. Основное — архитектура и attention, не внешний re-prompter.  
Интересный контролируемый факт: модель на T5 ~100k steps, переключение на InternVL-2.5-8B LAP — порядка ~10k steps хватает, чтобы снова рисовать связно; при равном числе сэмплов «с нуля на VLM» и «переключили с T5» почти не отличаются.  
Отдельно любопытно: подача сгенерированного продолжения промпта, чтобы VLM «подумала» и, возможно, по сути сделала внутренний re-prompt — это уже стык с нашей темой, но не главный вклад статьи.

### Ускорение видео по сложности областей
https://arxiv.org/pdf/2603.00519  

Разный compute на разные области «сложности» — не про re-prompt; держим как соседний compute-allocation мотив (рифмуется с «куда класть бюджет», но в другом месте пайплайна).

### Модели становятся менее безопасными со временем
https://arxiv.org/pdf/2605.28137  

Safety drift — вне основного фокуса captions/re-prompt; в обзоре как пограничная заметка.

---

## 4. Исследовательские сюжеты, которые из этого обзора следует вести

### Сюжет A — Структурность vs NL при одной семантике

Текст, который вы уже сформулировали:

Сравнение форматов с одной семантикой NL и Structured. Ориентир Seed [`2607.29679`](https://arxiv.org/pdf/2607.29679): чиним их confound и отдельно проверяем необходимость структурности. Лестницы длин как у них, но NL наращивает сущности и детали, не только воду; плюс перевод SP в обычный текст с теми же bbox/color/position. Отдельно учим re-prompter (Qwen3.5-397B LoRA rank 128, SFT) и полностью diffuser под задачу; сравниваем loss и метрики.

**Тейк.** NL богаче внутренней структурой и подсмыслами; схема облегчает базовые концепты. Проверка — как раз matched-facts стенд и paraphrase SP→NL.

Рядом по литературе: FIBO (structured vs short без matched info), i1 (длинные + rewrite на infer), Hunyuan (вариативность длины вместо обязательного rewriter), RECAP (mix при CLIP-77), Brack (дизайн captions).

### Сюжет B — Насколько глубоко учить prompter (SFT / RL / агенты)

Ваш развёрнутый текст уже хороший; якоря из обзора:

| Лагерь | Что делает | Откуда в обзоре |
|--------|------------|-----------------|
| SFT | Учит формат и распределение IR | Seed SFT; DALL·E 3 / i1 логика «попасть в train style»; PromptEnhancer stage 1 |
| RL / preference | Подстраивает под картинку и судью | PromptEnhancer GRPO; APE GRPO; ISS DPO; Seed OPSD; Think-Then-Generate GRPO |
| Агенты / циклы | Rewrite → render → вопросы/критика → правка | VisualPrompter; TARA; APE MAPE; Seed agentic loop |

Смысл эксперимента: один diffuser, один IR, накопительно SFT → cold-start/RL → loop; качество относительно **исходного** запроса; отдельно стоимость обучения и стоимость задержки ответа; плюс вопрос, не закрывает ли большой frozen LLM со схемой в контексте весь post-training. Метрики врать умеют: у Seed DPG почти стоит, structure/GSB растут.

Полный bakeoff с ссылками: [`ideas_reprompter_training_bakeoff.md`](./ideas_reprompter_training_bakeoff.md).

### Сюжет C — Трейдоф бюджета: diffuser vs re-prompter

Из Seed-разложения Diffusability × Promptability + i1/DALL·E 3 (сначала распределение подписей и генератор, потом upsampler). Считать потолок «IR с картинки» и потолок «лучший IR без картинки», смотреть куда ещё есть запас и сколько качества покупает час GPU на каждом рычаге.

### Сюжет D — Где теряется сигнал / не только текст

Цепочка annotate → serialize → encode → DiT. UniFusion и Think-Then-Generate намекают: иногда ответ не «лучший JSON», а другой канал conditioning (VLM encoder, embeddings после thinking). SoftREPA-класс в соседних отчётах репо — тот же мотив.

### Сюжет E — Бюджет токенов и вариативность длины

RECAP mix, i1 truncation 256, Hunyuan 30–1000 слов, FIBO ~1000 + спецархитектура, Seed L5–L10. Вопрос «что класть в лимит» и «рандомизировать ли длину на train, чтобы не зависеть от rewriter».

---

## 5. Чего из обзора специально не путать

- **UniFusion (`2510.12789`)** — не статья про внешний re-prompter; ядро про VLM-encoder.  
- **DALL·E 3 PDF** — сильная постановка captioner + upsampler, мало деталей реализации caption-модели.  
- **Seed NL vs SP** — не честное сравнение одной семантики; ваш парафраз SP→NL как раз это чинит.  
- **i1 правый столбец GenEval** — режимы инференса на уже обученной модели, не отдельные train-раны.  
- **VisualPrompter / TARA** — post-hoc / iterative repair, не замена вопросу «надо ли учить prompter».  
- **Think-Then-Generate** — re-prompt может заканчиваться эмбеддингами, не строкой.

---

## 6. Куда это лежит в репо

| Файл | Роль |
|------|------|
| Этот файл | Ваш обзор + фильтрация «про то / не про то» |
| [`ideas_t2i_conditioning_narrative.md`](./ideas_t2i_conditioning_narrative.md) | Идеи по шаблону |
| [`ideas_t2i_conditioning_stage.md`](./ideas_t2i_conditioning_stage.md) | Связное эссе |
| [`ideas_reprompter_training_bakeoff.md`](./ideas_reprompter_training_bakeoff.md) | SFT / RL / agents |
| [`training_bytedance_context_scaling.md`](./training_bytedance_context_scaling.md) | Как учили в Seed |
| [`fundamental_papers_reprompt_reading_list.md`](./fundamental_papers_reprompt_reading_list.md) | Более широкое ядро PE |
