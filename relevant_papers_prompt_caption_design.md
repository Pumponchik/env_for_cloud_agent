# Релевантные статьи: дизайн промптов и подписей для T2I

*64 статьи. Каждая: Проблема, Метод, Результат — 1–2 предложения на пункт.*

---

## 1. Improving Image Generation with Better Captions (DALL·E 3)

**Link:** [https://cdn.openai.com/papers/dall-e-3.pdf](https://cdn.openai.com/papers/dall-e-3.pdf)

**Проблема:** T2I-модели, обученные на шумном веб-alt-text, плохо следуют сложным промптам, потому что подписи короткие, неточные и не содержат деталей.

**Метод:** Обучить специальную модель-кэпшенер, которая генерирует длинные детальные синтетические подписи ко всем тренировочным изображениям; на инференсе использовать LLM «prompt upsampler», который переписывает короткие пользовательские промпты в стиль тренировочных подписей.

**Результат:** Радикально улучшенное следование промптам по сравнению с обучением на alt-text. Установлена парадигма, которую переняли SD3, FLUX, Playground и большинство последующих frontier T2I-систем.

---

## 2. How to Train Your Text-to-Image Model: Evaluating Design Choices for Synthetic Training Captions

**Link:** [https://www.semanticscholar.org/paper/31728f531ec52215f87f5d55446a34e9ca5488e0](https://www.semanticscholar.org/paper/31728f531ec52215f87f5d55446a34e9ca5488e0)

**Проблема:** Доктрина DALL·E 3 «длинные плотные подписи лучше» широко принята, но никто не проводил контролируемого исследования, изолирующего влияние дизайна подписей.

**Метод:** Зафиксировать архитектуру (SD v1.1), изображения (1M) и вычисления; варьировать только подписи по гипотезам: сила VLM, длина/плотность, температура, обновление между эпохами, persona diversity и гендерный bias. Оценка: aesthetics, PickScore, LPIPS diversity, bias при четырёх уровнях сложности промптов.

**Результат:** Длинные плотные подписи улучшают alignment, но ухудшают эстетику и diversity при коротких промптах. Рандомизация длины/плотности убирает trade-off и даёт лучшую модель в целом. Распределение терминов в подписях напрямую сдвигает гендерный bias модели.

---

## 3. i1: A Simple and Fully Open Recipe for Strong Text-to-Image Models

**Link:** [https://arxiv.org/abs/2606.11289v1](https://arxiv.org/abs/2606.11289v1)
**Year:** 2026

**Проблема:** Ведущие T2I-модели не раскрывают данные и не проводят ablation, что делает невозможным понять, какие решения действительно важны.

**Метод:** Полностью открытый рецепт (i1): энкодер T5Gemma-2B с усечением до 256 токенов; контролируемые эксперименты по текстовым энкодерам, стратегиям подписей и смешиванию датасетов. Ключевая ablation: обучение на 0–100% длинных подписей, оценка GenEval с оригинальными/повторёнными/переписанными промптами.

**Результат:** Обучение на длинных подписях даёт 0.17 на коротких GenEval-промптах, 0.49 при повторении ×12, 0.73 при LLM-rewrite. Вывод: учить на длинных и удлинять инференс-промпты до тренировочного распределения, а не учить на коротких под пользователей.

---

## 4. Improving Text-to-Image Generation with Input-Side Inference-Time Scaling

**Link:** [https://www.semanticscholar.org/paper/e40cbb9cf96ca92d7ad4cf83ab937612a85e1cfb](https://www.semanticscholar.org/paper/e40cbb9cf96ca92d7ad4cf83ab937612a85e1cfb)

**Проблема:** T2I-модели работают хуже на коротких/неопределённых промптах, потому что пользовательский текст далёк по распределению от плотных тренировочных подписей.

**Метод:** Обучить LLM-rewriter через итеративный DPO (без SFT-данных); rewriter расширяет пользовательские промпты до распределения тренировочных подписей перед генерацией.

**Результат:** Rewriter переносится между T2I-бэкбонами без дообучения. Сокращение разрыва между train/user текстом улучшает alignment, эстетику и качество на нескольких моделях.

---

## 5. PromptEnhancer: A Simple Approach to Enhance Text-to-Image Models via Chain-of-Thought Prompt Rewriting

**Link:** [https://www.semanticscholar.org/paper/70a0f72b06327998b9274a5d7da6f89159b75d16](https://www.semanticscholar.org/paper/70a0f72b06327998b9274a5d7da6f89159b75d16)

**Проблема:** Существующие методы prompt enhancement либо добавляют общие стилистические детали, либо оптимизируют без понимания failure modes T2I (attribute leakage, spatial errors).

**Метод:** PromptEnhancer: CoT-политика переписывания промптов, обученная RL против AlignEvaluator — reward-модели, оценивающей 24 категории T2I-ошибок. Переписывание добавляет нужный контент, а не пустую многословность.

**Результат:** Стабильно улучшает метрики alignment на нескольких T2I-бэкбонах. Показывает, что контент-ориентированное переписывание (исправление ошибок) лучше, чем максимизация длины.

---

## 6. Seeing is Believing: Aligning Prompt Rewriting with Visual Anchors for Text-to-Image Generation

**Link:** [https://arxiv.org/abs/2606.08492v2](https://arxiv.org/abs/2606.08492v2)
**Year:** 2026

**Проблема:** Текстовые rewriter-ы галлюцинируют визуально или физически невозможные детали (например, «вода, зависшая в воздухе»), потому что у них нет визуальной привязки.

**Метод:** FaithRewriter: сначала генерирует промежуточное изображение по исходному промпту, затем использует его как визуальный якорь при переписывании — гарантируя, что расширения соответствуют тому, что реально может быть сгенерировано.

**Результат:** Снижает галлюцинированные детали в расширенных промптах и улучшает faithfulness промпт-изображение по сравнению с text-only rewriter-ами.

---

## 7. TIPO: Text to Image with Text Presampling for Prompt Optimization

**Link:** [https://arxiv.org/abs/2411.08127v6](https://arxiv.org/abs/2411.08127v6)
**Year:** 2024

**Проблема:** Пользовательские промпты отличаются от тренировочных подписей по длине, стилю и содержанию, что создаёт distributional gap, снижающий качество генерации.

**Метод:** TIPO: расширяет промпты в направлении распределения тренировочного текста (корпус 30M пар / 40B токенов), сознательно расширяя, а не полностью переписывая.

**Результат:** 62.8% human win rate над оригинальными промптами и до 29.4% ускорения инференса. Формулирует цель PE как matching μ_train, а не максимизацию многословности.

---

## 8. A Picture is Worth a Thousand Words: Principled Recaptioning Improves Image Generation

**Link:** [https://www.semanticscholar.org/paper/10fce9e1718e968846c8429366c597380cce213d](https://www.semanticscholar.org/paper/10fce9e1718e968846c8429366c597380cce213d)

**Проблема:** Веб-alt-text шумный и неточный, что ухудшает обучение T2I, но оптимальная длина и стиль рекэпшенинга неизвестны.

**Метод:** RECAP: дообучить PaLI-кэпшенер с short/long conditioning-префиксами; сравнить обучение SD на RECAP-Short, RECAP-Long, 50/50 Mix и оригинальном alt-text. Подписи >77 токенов отбрасываются.

**Результат:** Short лучше по FID; Long лучше по семантике; 50/50 Mix лучший в целом. Первое принципиальное свидетельство в пользу смешивания длин подписей при ограничении CLIP-77.

---

## 9. What If We Recaption Billions of Web Images with LLaMA-3?

**Link:** [https://www.semanticscholar.org/paper/82bc594ddf77fe8e69e9b41dc32960d7f16b4b1d](https://www.semanticscholar.org/paper/82bc594ddf77fe8e69e9b41dc32960d7f16b4b1d)

**Проблема:** Датасеты веб-масштаба используют шумный короткий alt-text (~10 токенов в среднем), что недостаточно описывает изображения для T2I и representation learning.

**Метод:** Рекэпшенинг DataComp-1B с помощью LLaVA-1.5-LLaMA3-8B при max_new_tokens=128 и greedy decoding. Средняя длина вырастает с 10.22 до 49.43 токенов.

**Результат:** Улучшение downstream T2I и классификации. Устанавливает рабочую точку для офлайн VLM-рекэпшенинга среднего масштаба (~128 decode budget → ~50 реализованных токенов).

---

## 10. Generating an Image From 1,000 Words: Enhancing Text-to-Image With Structured Captions

**Link:** [https://www.semanticscholar.org/paper/38fd53bac34ba902b8e7f1cf3f6552da5a3eaaaf](https://www.semanticscholar.org/paper/38fd53bac34ba902b8e7f1cf3f6552da5a3eaaaf)

**Проблема:** Короткие свободные подписи недостаточно описывают изображения и ограничивают контролируемость; существующие модели не могут эффективно использовать длинный структурированный текст.

**Метод:** FIBO: обучение T2I-модели на ~1000-токенных структурированных JSON-schema подписях. DimFusion сливает промежуточные слои LLM без увеличения числа токенов (в отличие от TokenFusion, которая удваивает).

**Результат:** Длинные структурированные подписи сходятся быстрее, улучшают FID и открывают per-attribute контроль. DimFusion сравнима по качеству с TokenFusion при ~1.6× меньшем времени шага.

---

## 11. HunyuanImage 3.0 Technical Report

**Link:** [https://arxiv.org/abs/2509.23951v3](https://arxiv.org/abs/2509.23951v3)
**Year:** 2025

**Проблема:** Существующие T2I-системы используют либо фиксированные короткие, либо фиксированные длинные подписи, ограничивая робастность к разным стилям пользовательских промптов.

**Метод:** Compositional Caption Synthesis: сэмплирование и комбинирование иерархических полей подписей для генерации билингвальных подписей от ~30 до 1000 слов. На инференсе — опциональные CoT think_recaption режимы.

**Результат:** Робастная работа на коротких и длинных промптах без обязательного rewriter-а — широкая тренировочная полоса естественно покрывает оба режима.

---

## 12. DetailMaster: Can Your Text-to-Image Model Handle Long Prompts?

**Link:** [https://www.semanticscholar.org/paper/7a94c25090610547ee3a9ba5ca6d1ce22e185acd](https://www.semanticscholar.org/paper/7a94c25090610547ee3a9ba5ca6d1ce22e185acd)

**Проблема:** Бенчмарки T2I преимущественно используют короткие промпты; нет строгой оценки того, как модели справляются с длинными, детализированными профессиональными промптами.

**Метод:** DetailMaster: 4116 промптов со средней длиной 284.89 токенов и fine-grained метриками по атрибутам персонажей, локациям, атрибутам сцены и отношениям сущностей.

**Результат:** Даже SOTA-модели достигают лишь ~50% на сложных attribute tasks. Плотное длинное обучение важнее, чем просто увеличение token capacity. Точность монотонно падает с ростом длины промпта.

---

## 13. RePrompt: Reasoning-Augmented Reprompting for Text-to-Image Generation via Reinforcement Learning

**Link:** [https://www.semanticscholar.org/paper/757a286592ffcc50735eb525edf32b9fbdd1309b](https://www.semanticscholar.org/paper/757a286592ffcc50735eb525edf32b9fbdd1309b)

**Проблема:** Prompt enhancement для T2I обычно делается статическими шаблонами или простым LLM-перефразированием, без рассуждений о том, что нужно генератору.

**Метод:** RePrompt: reasoning-augmented reprompting, обученный через RL, где rewriter учится рассуждать, почему текущий промпт может не сработать.

**Результат:** Улучшает alignment и качество изображений по сравнению со статическими и шаблонными подходами к rewriting.

---

## 14. Harnessing Caption Detailness for Data-Efficient Text-to-Image Generation

**Link:** [https://www.semanticscholar.org/paper/f00a1a44e2adb0d3dd735e5c35a8d382a1855ca7](https://www.semanticscholar.org/paper/f00a1a44e2adb0d3dd735e5c35a8d382a1855ca7)

**Проблема:** Обучение T2I на плотных подписях дорого, поскольку генерация качественных синтетических подписей для каждого изображения требует больших VLM в масштабе.

**Метод:** Изучение, какие изображения больше всего выигрывают от детальных подписей, и выделение ресурсов кэпшенинга соответственно (data-efficient подход).

**Результат:** Сопоставимое или лучшее качество T2I при меньшем количестве дорогих плотных подписей — за счёт целевого распределения детализации.

---

## 15. Playground v3: Improving Text-to-Image Alignment with Deep-Fusion Large Language Models

**Link:** [https://www.semanticscholar.org/paper/b2e62ce609f3388f9a2fb709cb8f993fa4a8174f](https://www.semanticscholar.org/paper/b2e62ce609f3388f9a2fb709cb8f993fa4a8174f)

**Проблема:** CLIP/T5 dual-tower conditioning ограничивает глубину языкового понимания в генераторе; плотность и разнообразие подписей тоже требуют внимания.

**Метод:** Deep-fusion каждого слоя Llama3-8B в DiT, полностью заменяя CLIP/T5. Обучение на синтетических подписях с варьированием плотности и inter-epoch diversity.

**Результат:** Сильный text-image alignment и эстетика; вводит CapsBench для оценки качества подписей. Мотивирует рецепт «варьировать плотность + обновлять подписи между эпохами».

---

## 16. PixArt-Σ: Weak-to-Strong Training of Diffusion Transformer for 4K Text-to-Image

**Link:** [https://arxiv.org/abs/2403.04692v2](https://arxiv.org/abs/2403.04692v2)
**Year:** 2024

**Проблема:** Стандартные 77 текстовых токенов из CLIP недостаточны для плотных подписей, необходимых для точной генерации изображений в высоком разрешении.

**Метод:** Расширение длины текстового энкодера с 120 (PixArt-α) до ~300, чтобы вместить более плотные подписи, и обучение 4K-resolution diffusion transformer.

**Результат:** Улучшение text-image alignment и качества генерации на высоких разрешениях. Демонстрирует, что бюджет токенов энкодера должен масштабироваться с плотностью подписей.

---

## 17. PixArt-$α$: Fast Training of Diffusion Transformer for Photorealistic Text-to-Image Synthesis

**Link:** [https://arxiv.org/abs/2310.00426](https://arxiv.org/abs/2310.00426)
**Year:** 2023

**Проблема:** Обучение T2I diffusion transformer чрезвычайно дорого; нужны эффективные стратегии обучения и лучшие данные подписей.

**Метод:** Быстрое обучение DiT с T5-XXL, используя плотные LLaVA-подписи. Явное увеличение длины токенов с 77 до 120, потому что LLaVA-подписи плотнее.

**Результат:** Конкурентное качество при значительно меньших вычислениях, чем SD/DALL·E. Показывает, что плотные подписи улучшают эффективность обучения на каждом шаге.

---

## 18. Altogether: Image Captioning via Re-aligning Alt-text

**Link:** [https://arxiv.org/abs/2406.18583](https://arxiv.org/abs/2406.18583)

**Проблема:** Синтетические подписи лучше alt-text для T2I, но оптимальное соотношение смешивания синтетических и оригинальных подписей неизвестно.

**Метод:** Систематическое варьирование доли синтетических LLaVA-подписей, смешанных с оригинальным alt-text, для обучения T2I и CLIP.

**Результат:** Для T2I ~100% синтетических — лучше всего (оспаривая 95/5 микс DALL·E 3). Для CLIP оптимально лишь ~15% синтетических. Соотношение нужно настраивать под задачу.

---

## 19. Lens: Rethinking Training Efficiency for Foundational Text-to-Image Models

**Link:** [https://www.semanticscholar.org/paper/f69e22f570f6a4584792ba1debabf3211cc6cbe7](https://www.semanticscholar.org/paper/f69e22f570f6a4584792ba1debabf3211cc6cbe7)

**Проблема:** Обучение фундаментальных T2I-моделей требует огромных вычислений; неясно, какие стратегии данных/подписей наиболее compute-efficient.

**Метод:** Анализ взаимодействия качества подписей, состава данных и расписания обучения для поиска эффективных конфигураций.

**Результат:** Выявлены конфигурации, снижающие стоимость обучения при сохранении или улучшении качества генерации.

---

## 20. PromptEcho: Annotation-Free Reward from Vision-Language Models for Text-to-Image Reinforcement Learning

**Link:** [https://arxiv.org/abs/2604.12652](https://arxiv.org/abs/2604.12652)
**Year:** 2026

**Проблема:** Обучение PE/reward-моделей для T2I обычно требует дорогих человеческих аннотаций.

**Метод:** Извлечение reward-сигнала из VLM без аннотаций для RL-обучения text-to-image, используя оценки VLM как функцию награды.

**Результат:** Позволяет обучать prompt rewriter-ы/генераторы через RL без данных человеческих предпочтений.

---

## 21. DreamLIP: Language-Image Pre-training with Long Captions

**Link:** [https://www.semanticscholar.org/paper/0f284b2fdf001ced671ef87bea3435849c1e8059](https://www.semanticscholar.org/paper/0f284b2fdf001ced671ef87bea3435849c1e8059)

**Проблема:** CLIP-модели обучаются на коротком alt-text, что ограничивает их понимание детализированных визуальных описаний.

**Метод:** Language-image pre-training с длинными детальными синтетическими подписями для улучшения как CLIP-style representations, так и downstream T2I conditioning.

**Результат:** Улучшение zero-shot и fine-tuned результатов, когда language-image модели видят длинные плотные подписи при pre-training.

---

## 22. Low-hallucination Synthetic Captions for Large-Scale Vision-Language Model Pre-training

**Link:** [https://www.semanticscholar.org/paper/018700af04b19af74cc3745fd75ba3c47be3a299](https://www.semanticscholar.org/paper/018700af04b19af74cc3745fd75ba3c47be3a299)

**Проблема:** Синтетические подписи от VLM могут галлюцинировать объекты или атрибуты, отсутствующие на изображении, отравляя тренировочные данные.

**Метод:** Применение пайплайнов обнаружения и фильтрации галлюцинаций к VLM-подписям перед использованием для VL pre-training.

**Результат:** Чистые подписи улучшают надёжность downstream-моделей; подчёркивает, что длина подписи без faithfulness вредна.

---

## 23. RICO: Improving Accuracy and Completeness in Image Recaptioning via Visual Reconstruction

**Link:** [https://www.semanticscholar.org/paper/7e10a5223adfd36121541ff64cb14addaef5475e](https://www.semanticscholar.org/paper/7e10a5223adfd36121541ff64cb14addaef5475e)

**Проблема:** Существующие подходы к рекэпшенингу приоритезируют либо accuracy, либо completeness, но редко оба одновременно.

**Метод:** RICO: цикл визуальной реконструкции — генерировать изображение из подписи и сравнить с оригиналом — для обеспечения accuracy и completeness подписей.

**Результат:** Улучшенное качество рекэпшенинга на нескольких бенчмарках; сигнал реконструкции ловит и пропуски, и галлюцинации.

---

## 24. Building a Precise Video Language with Human-AI Oversight

**Link:** [https://www.semanticscholar.org/paper/84e9bfb2900a257aed59b6503cca04d9b1c5202d](https://www.semanticscholar.org/paper/84e9bfb2900a257aed59b6503cca04d9b1c5202d)

**Проблема:** Video-language models (VLMs) learn to reason about the dynamic visual world through natural language.

**Метод:** We introduce a suite of open datasets, benchmarks, and recipes for scalable oversight that enable precise video captioning.

**Результат:** Data and code are available on our project page: https://linzhiqiu.github.io/papers/chai/

---

## 25. ShareGPT4Video: Improving Video Understanding and Generation with Better Captions

**Link:** [https://www.semanticscholar.org/paper/9583cadea300f67aaab0fdf7b6d1f774c3cd55e7](https://www.semanticscholar.org/paper/9583cadea300f67aaab0fdf7b6d1f774c3cd55e7)

**Проблема:** We present the ShareGPT4Video series, aiming to facilitate the video understanding of large video-language models (LVLMs) and the video generation of text-to-video models (T2VMs) via dense and precise captions.

**Метод:** The series comprises: 1) ShareGPT4Video, 40K GPT4V annotated dense captions of videos with various lengths and sources, developed through carefully designed data filtering and annotating strategy.

**Результат:** Based on ShareGPT4Video, we further develop ShareCaptioner-Video, a superior captioner capable of efficiently generating high-quality captions for arbitrary videos...

---

## 26. VideoPainter: Any-length Video Inpainting and Editing with Plug-and-Play Context Control

**Link:** [https://www.semanticscholar.org/paper/38c29254113bbc6a98048fac368cb1914e2429c9](https://www.semanticscholar.org/paper/38c29254113bbc6a98048fac368cb1914e2429c9)

**Проблема:** Video inpainting, crucial for the media industry, aims to restore corrupted content.

**Метод:** However, current methods relying on limited pixel propagation or single-branch image inpainting architectures face challenges with generating fully masked objects, balancing background preservation with foreground generation, and maintaining ID consistency over long video.

**Результат:** Extensive experiments demonstrate VideoPainter’s state-of-the-art performance in any-length video inpainting and editing across 8 key metrics, including video quality, mask region preservation, and textual coherence.

---

## 27. Efficient Scaling of Diffusion Transformers for Text-to-Image Generation

**Link:** [https://www.semanticscholar.org/paper/8d066b07fa15312338b6fba86149bc6e8526136d](https://www.semanticscholar.org/paper/8d066b07fa15312338b6fba86149bc6e8526136d)

**Проблема:** We empirically study the scaling properties of various Diffusion Transformers (DiTs) for text-to-image generation by performing extensive and rigorous ablations, including training scaled DiTs ranging from 0.3B upto 8B parameters on datasets up to 600M images.

**Метод:** We find that U-ViT, a pure self-attention based DiT model provides a simpler design and scales more effectively in comparison with cross-attention based DiT variants, which allows straightforward expansion for extra conditions and other modalities.

**Результат:** On the data scaling side, we investigate how increasing dataset size and enhanced long caption improve the text-image alignment performance and the learning efficiency.

---

## 28. Moving Alphabet: A Controlled Study of Training Data for Text-to-Video Generation

**Link:** [https://www.semanticscholar.org/paper/f9934e0a4c2d2e76a7033255431e9a145df8779c](https://www.semanticscholar.org/paper/f9934e0a4c2d2e76a7033255431e9a145df8779c)

**Проблема:** Text-to-video generation has advanced significantly over the past five years through scaling of model size, data, and compute.

**Метод:** Unlike model architecture, training data is often underexplored.

**Результат:** We believe these insights can inform the development of large-scale text-to-video models, and we advocate for greater attention to the science of pre-training data.

---

## 29. ETTA: Elucidating the Design Space of Text-to-Audio Models

**Link:** [https://www.semanticscholar.org/paper/2e1056e68951dedcfd492d5297840321b3b3daf0](https://www.semanticscholar.org/paper/2e1056e68951dedcfd492d5297840321b3b3daf0)

**Проблема:** Recent years have seen significant progress in Text-To-Audio (TTA) synthesis, enabling users to enrich their creative workflows with synthetic audio generated from natural language prompts.

**Метод:** Despite this progress, the effects of data, model architecture, training objective functions, and sampling strategies on target benchmarks are not well understood.

**Результат:** Finally, we show ETTA's improved ability to generate creative audio following complex and imaginative captions -- a task that is more challenging than current benchmarks.

---

## 30. BACON: Improving Clarity of Image Captions via Bag-of-Concept Graphs

**Link:** [https://www.semanticscholar.org/paper/8cc04354e5b308e30206103ba3ea5f8c2b59c0b0](https://www.semanticscholar.org/paper/8cc04354e5b308e30206103ba3ea5f8c2b59c0b0)

**Проблема:** Advancements in large Vision-Language Models have brought precise, accurate image captioning, vital for advancing multi-modal image understanding and processing.

**Метод:** Yet these captions often carry lengthy, intertwined contexts that are difficult to parse and frequently overlook essential cues, posing a great barrier for models like GroundingDINO and SDXL, which lack the strong text encoding and syntax analysis needed to fully leverage dense captions.

**Результат:** For example, BACON-style captions help GroundingDINO achieve 1.51× higher recall scores on open-vocabulary object detection tasks compared to leading methods.

---

## 31. Rethinking Music Captioning with Music Metadata LLMs

**Link:** [https://www.semanticscholar.org/paper/27bb0504e76395bf6ca8106929cc7b34f7c0ae06](https://www.semanticscholar.org/paper/27bb0504e76395bf6ca8106929cc7b34f7c0ae06)

**Проблема:** Music captioning, or the task of generating a natural language description of music, is useful for both music understanding and controllable music generation.

**Метод:** Training captioning models, however, typically requires high-quality music caption data which is scarce compared to metadata (e.g., genre, mood, etc.).

**Результат:** Compared to a strong end-to-end baseline trained on LLM-generated captions derived from metadata, our method: (1) achieves comparable performance in less training time over end-to-end captioners, (2) offers flexibility to easily change stylization post-training, enabling output captions to be tailored to specific stylistic and quality requirements, and (3) can be prompted with audio and partial metadata to enable powerful metadata imputation or in-filling--a common task for organizing music data.

---

## 32. RAPO++: Cross-Stage Prompt Optimization for Text-to-Video Generation via Data Alignment and Test-Time Scaling

**Link:** [https://www.semanticscholar.org/paper/5d4f3bef456e9d038a4d569a5b8f76cbb0328a41](https://www.semanticscholar.org/paper/5d4f3bef456e9d038a4d569a5b8f76cbb0328a41)

**Проблема:** Prompt design plays a crucial role in text-to-video (T2V) generation, yet user-provided prompts are often short, unstructured, and misaligned with training data, limiting the generative potential of diffusion-based T2V models.

**Метод:** We present \textbf{RAPO++}, a cross-stage prompt optimization framework that unifies training-data--aligned refinement, test-time iterative scaling, and large language model (LLM) fine-tuning to substantially improve T2V generation without modifying the underlying generative backbone.

**Результат:** The code is available at https://github.com/Vchitect/RAPO.

---

## 33. On the Scalability of Diffusion-based Text-to-Image Generation

**Link:** [https://www.semanticscholar.org/paper/a9489b4ad6f82db616f0b4a915dcfc0448e4c70e](https://www.semanticscholar.org/paper/a9489b4ad6f82db616f0b4a915dcfc0448e4c70e)

**Проблема:** Scaling up model and data size has been quite successful for the evolution of LLMs.

**Метод:** However, the scaling law for the diffusion based text-to-image (T2I) models is not fully explored.

**Результат:** Finally, we provide scaling functions to predict the text-image alignment performance as functions of the scale of model size, compute and dataset size.

---

## 34. Mastering Text-to-Image Diffusion: Recaptioning, Planning, and Generating with Multimodal LLMs

**Link:** [https://www.semanticscholar.org/paper/140cfda71bfff852c3e205b7ad61854b78c76982](https://www.semanticscholar.org/paper/140cfda71bfff852c3e205b7ad61854b78c76982)

**Проблема:** Diffusion models have exhibit exceptional performance in text-to-image generation and editing.

**Метод:** However, existing methods often face challenges when handling complex text prompts that involve multiple objects with multiple attributes and relationships.

**Результат:** Our code is available at: https://github.com/YangLing0818/RPG-DiffusionMaster

---

## 35. Semantic Browsing: Controllable Diversity for Image Generation

**Link:** [https://www.semanticscholar.org/paper/a370eda4515fb2ea120961196bd07e26205fd910](https://www.semanticscholar.org/paper/a370eda4515fb2ea120961196bd07e26205fd910)

**Проблема:** Modern text-to-image models excel in visual fidelity and prompt adherence.

**Метод:** However, this strict adherence comes at the cost of diversity: generated samples tend to collapse into a single visual interpretation.

**Результат:** We demonstrate that our method produces diverse and navigable design spaces where every variation corresponds to a specific, user-understandable semantic decision.

---

## 36. Generate Any Scene: Scene Graph Driven Data Synthesis for Visual Generation Training

**Link:** [https://arxiv.org/abs/2412.08221](https://arxiv.org/abs/2412.08221)
**Year:** 2024

**Проблема:** Recent advances in text-to-vision generation excel in visual fidelity but struggle with compositional generalization and semantic alignment.

**Метод:** Existing datasets are noisy and weakly compositional, limiting models' understanding of complex scenes, while scalable solutions for dense, high-quality annotations remain a challenge.

**Результат:** Finally, we apply these ideas to the downstream task of content moderation where we train models to identify challenging cases by learning from synthetic data.

---

## 37. View Selection for 3D Captioning via Diffusion Ranking

**Link:** [https://www.semanticscholar.org/paper/f4a3c29b3ed9442c848a6c6b226b142bcdef59b1](https://www.semanticscholar.org/paper/f4a3c29b3ed9442c848a6c6b226b142bcdef59b1)

**Проблема:** Scalable annotation approaches are crucial for constructing extensive 3D-text datasets, facilitating a broader range of applications.

**Метод:** However, existing methods sometimes lead to the generation of hallucinated captions, compromising caption quality.

**Результат:** Additionally, we showcase the adaptability of DiffuRank by applying it to pre-trained text-to-image models for a Visual Question Answering task, where it outperforms the CLIP model.

---

## 38. Improving Explicit Spatial Relationships in Text-to-Image Generation through an Automatically Derived Dataset

**Link:** [https://www.semanticscholar.org/paper/8408419e8263fa08c8515948f14b58e64bfef609](https://www.semanticscholar.org/paper/8408419e8263fa08c8515948f14b58e64bfef609)

**Проблема:** Existing work has observed that current text-to-image systems do not accurately reflect explicit spatial relations between objects such as 'left of' or 'below'.

**Метод:** We hypothesize that this is because explicit spatial relations rarely appear in the image captions used to train these models.

**Результат:** The dataset and the code will be publicly available.

---

## 39. APE: Agentic Prompt Enhancer for Image Generation and Editing

**Link:** [https://www.semanticscholar.org/paper/14333575850073eaa86bd09c2ffdd2d96c3536e4](https://www.semanticscholar.org/paper/14333575850073eaa86bd09c2ffdd2d96c3536e4)

**Проблема:** Natural language has become a powerful interface for image generation and editing, yet text-guided visual systems remain highly sensitive to prompt formulation.

**Метод:** Semantically similar requests can produce different outputs depending on wording, specificity, and how explicitly visual constraints are stated, motivating prompt enhancement as a trainable component rather than a peripheral user choice.

**Результат:** Experiments on challenging image generation and editing benchmarks demonstrate that post-trained small prompt enhancers reliably outperform their base counterparts, narrowing the gap to closed-source prompt enhancers; in addition, MAPE proves particularly strong on complex compositional tasks within these benchmarks.

---

## 40. Factorized-Dreamer: Training A High-Quality Video Generator with Limited and Low-Quality Data

**Link:** [https://www.semanticscholar.org/paper/df85f8ba638ac00c374908179426b9feb8db488b](https://www.semanticscholar.org/paper/df85f8ba638ac00c374908179426b9feb8db488b)

**Проблема:** Text-to-video (T2V) generation has gained significant attention due to its wide applications to video generation, editing, enhancement and translation, \etc.

**Метод:** However, high-quality (HQ) video synthesis is extremely challenging because of the diverse and complex motions existed in real world.

**Результат:** Our source codes are available at \url{https://github.com/yangxy/Factorized-Dreamer/}.

---

## 41. Precision or Recall? An Analysis of Image Captions for Training Text-to-Image Generation Model

**Link:** [https://www.semanticscholar.org/paper/ca1778e79ceaf1696181b49a19afd1834bd85914](https://www.semanticscholar.org/paper/ca1778e79ceaf1696181b49a19afd1834bd85914)

**Проблема:** Despite advancements in text-to-image models, generating images that precisely align with textual descriptions remains challenging due to misalignment in training data.

**Метод:** In this paper, we analyze the critical role of caption precision and recall in text-to-image model training.

**Результат:** Models trained with these synthetic captions show similar behavior to those trained on human-annotated captions, underscores the potential for synthetic data in text-to-image training.

---

## 42. Revisit Large-Scale Image-Caption Data in Pre-training Multimodal Foundation Models

**Link:** [https://www.semanticscholar.org/paper/7497c8c863d46320b77e865c7a24bef9b0e9749f](https://www.semanticscholar.org/paper/7497c8c863d46320b77e865c7a24bef9b0e9749f)

**Проблема:** Recent advancements in multimodal models highlight the value of rewritten captions for improving performance, yet key challenges remain.

**Метод:** For example, while synthetic captions often provide superior quality and image-text alignment, it is not clear whether they can fully replace AltTexts: the role of synthetic captions and their interaction with original web-crawled AltTexts in pre-training is still not well understood.

**Результат:** This comprehensive analysis provides valuable insights into optimizing captioning strategies, thereby advancing the pre-training of multimodal foundation models.

---

## 43. CommonCanvas: An Open Diffusion Model Trained with Creative-Commons Images

**Link:** [https://www.semanticscholar.org/paper/1b672e2ea961ef45a9f3322430ca5df9ff8ba165](https://www.semanticscholar.org/paper/1b672e2ea961ef45a9f3322430ca5df9ff8ba165)

**Проблема:** We assemble a dataset of Creative-Commons-licensed (CC) images, which we use to train a set of open diffusion models that are qualitatively competitive with Stable Diffusion 2 (SD2).

**Метод:** This task presents two challenges: (1) high-resolution CC images lack the captions necessary to train text-to-image generative models; (2) CC images are relatively scarce.

**Результат:** We release our models, data, and code at https://github.com/mosaicml/diffusion/blob/main/assets/common-canvas.md

---

## 44. CRAFT: Continuous Reasoning and Agentic Feedback Tuning for Multimodal Text-to-Image Generation

**Link:** [https://www.semanticscholar.org/paper/b369583dc62cf4e16fae0e4e5c359b820a9fa021](https://www.semanticscholar.org/paper/b369583dc62cf4e16fae0e4e5c359b820a9fa021)

**Проблема:** Recent work has shown that inference-time reasoning and reflection can improve text-to-image generation without retraining.

**Метод:** However, existing approaches often rely on implicit, holistic critiques or unconstrained prompt rewrites, making their behavior difficult to interpret, control, or stop reliably.

**Результат:** Our results suggest that explicitly structured, constraint-driven inference-time reasoning is a key ingredient for improving the reliability of multimodal generative models.

---

## 45. Improving Text Generation on Images with Synthetic Captions

**Link:** [https://www.semanticscholar.org/paper/bcf3a67b088aaea81323a496149abc4f39dd25a0](https://www.semanticscholar.org/paper/bcf3a67b088aaea81323a496149abc4f39dd25a0)

**Проблема:** The recent emergence of latent diffusion models such as SDXL [1] and SD 1.5 [2] has shown significant capability in generating highly detailed and realistic images.

**Метод:** Despite their remarkable ability to produce images, generating accurate text within images still remains a challenging task.

**Результат:** Our experiments show that with the addition of random letters to our raw dataset, our model's performance improves in producing well-formed visual text.

---

## 46. KOALA: Empirical Lessons Toward Memory-Efficient and Fast Diffusion Models for Text-to-Image Synthesis

**Link:** [https://www.semanticscholar.org/paper/8b8d8cbbfaef256bddce273f5e541ef6e9ba3130](https://www.semanticscholar.org/paper/8b8d8cbbfaef256bddce273f5e541ef6e9ba3130)

**Проблема:** As text-to-image (T2I) synthesis models increase in size, they demand higher inference costs due to the need for more expensive GPUs with larger memory, which makes it challenging to reproduce these models in addition to the restricted access to training datasets.

**Метод:** Our study aims to reduce these inference costs and explores how far the generative capabilities of T2I models can be extended using only publicly available datasets and open-source models.

**Результат:** We believe that our KOALA models will have a significant practical impact, serving as cost-effective alternatives to SDXL for academic researchers and general users in resource-constrained environments.

---

## 47. Segment and Caption Anything

**Link:** [https://www.semanticscholar.org/paper/339ec34efdccdf2bf43bb817ef7cab5058bfa2e7](https://www.semanticscholar.org/paper/339ec34efdccdf2bf43bb817ef7cab5058bfa2e7)

**Проблема:** We propose a method to efficiently equip the Segment Anything Model (SAM) with the ability to generate regional captions.

**Метод:** SAM presents strong generalizability to segment anything while is short for semantic understanding.

**Результат:** The project page, along with the associated code, can be accessed via the following link.

---

## 48. LoTLIP: Improving Language-Image Pre-training for Long Text Understanding

**Link:** [https://www.semanticscholar.org/paper/9023e89eb0c1d060b8f3d9fcd048ca698cbd7bad](https://www.semanticscholar.org/paper/9023e89eb0c1d060b8f3d9fcd048ca698cbd7bad)

**Проблема:** Understanding long text is of great demands in practice but beyond the reach of most language-image pre-training (LIP) models.

**Метод:** In this work, we empirically confirm that the key reason causing such an issue is that the training images are usually paired with short captions, leaving certain tokens easily overshadowed by salient tokens.

**Результат:** The project page is available at https://wuw2019.github.io/lot-lip.

---

## 49. Dual-Stage Value-Guided Inference with Margin-Based Reward Adjustment for Fast and Faithful VLM Captioning

**Link:** [https://www.semanticscholar.org/paper/d1666b3f89df3dfb906a0a1d276994580068ac70](https://www.semanticscholar.org/paper/d1666b3f89df3dfb906a0a1d276994580068ac70)

**Проблема:** Despite significant advances in inference-time search for vision-language models (VLMs), existing approaches remain both computationally expensive and prone to unpenalized, low-confidence generations which often lead to persistent hallucinations.

**Метод:** We introduce \textbf{Value-guided Inference with Margin-based Reward (ViMaR)}, a two-stage inference framework that improves both efficiency and output fidelity by combining a temporal-difference value model with a margin-aware reward adjustment.

**Результат:** Furthermore, when ViMaR-generated captions are used for self-training, the underlying models achieve substantial gains across a broad suite of visual comprehension benchmarks, underscoring the potential of fast, accurate, and self-improving VLM pipelines.

---

## 50. Altogether: Image Captioning via Re-aligning Alt-text

**Link:** [https://www.semanticscholar.org/paper/4254ed35e15a99f6c7fbb634e42301e15212b696](https://www.semanticscholar.org/paper/4254ed35e15a99f6c7fbb634e42301e15212b696)

**Проблема:** This paper focuses on creating synthetic data to improve the quality of image captions.

**Метод:** Existing works typically have two shortcomings.

**Результат:** Our results show our Altogether approach leads to richer image captions that also improve text-to-image generation and zero-shot image classification tasks.

---

## 51. DetCLIPv3: Towards Versatile Generative Open-Vocabulary Object Detection

**Link:** [https://www.semanticscholar.org/paper/9190dbc582c9871dc771fc87afd85ea4c2455fb9](https://www.semanticscholar.org/paper/9190dbc582c9871dc771fc87afd85ea4c2455fb9)

**Проблема:** Existing open-vocabulary object detectors typically require a predefined set of categories from users, signifi-cantly confining their application scenarios.

**Метод:** In this pa-per, we introduce DetCLIPv3, a high-performing detector that excels not only at both open-vocabulary object detection, but also generating hierarchical labels for detected objects.

**Результат:** DetCLIPv3 also achieves a state-of-the-art 19.7 AP in dense captioning task on VG dataset, showcasing its strong generative capability.

---

## 52. Mimir: Improving Video Diffusion Models for Precise Text Understanding

**Link:** [https://www.semanticscholar.org/paper/9978e1c198aa9052005d181e7b62aee19ab18a3d](https://www.semanticscholar.org/paper/9978e1c198aa9052005d181e7b62aee19ab18a3d)

**Проблема:** Text serves as the key control signal in video generation due to its narrative nature.

**Метод:** To render text descriptions into video clips, current video diffusion models borrow features from text encoders yet struggle with limited text comprehension.

**Результат:** Project page: https://lucaria-academy.github.io/Mimir/

---

## 53. MoTrans: Customized Motion Transfer with Text-driven Video Diffusion Models

**Link:** [https://www.semanticscholar.org/paper/cd851366e07d5dc5dc6920fc39835df46ab2cce0](https://www.semanticscholar.org/paper/cd851366e07d5dc5dc6920fc39835df46ab2cce0)

**Проблема:** Existing pretrained text-to-video (T2V) models have demonstrated impressive abilities in generating realistic videos with basic motion or camera movement.

**Метод:** However, these models exhibit significant limitations when generating intricate, human-centric motions.

**Результат:** Experimental results demonstrate that our method effectively learns specific motion pattern from singular or multiple reference videos, performing favorably against existing methods in customized video generation.

---

## 54. Diffusion Probe: Generated Image Result Prediction Using CNN Probes

**Link:** [https://www.semanticscholar.org/paper/b879e05782c0165ea5a03000022bcbad23f2ccb4](https://www.semanticscholar.org/paper/b879e05782c0165ea5a03000022bcbad23f2ccb4)

**Проблема:** Text-to-image (T2I) diffusion models lack an efficient mechanism for early quality assessment, leading to costly trial-and-error in multi-generation scenarios such as prompt iteration, agent-based generation, and flow-grpo.

**Метод:** We reveal a strong correlation between early diffusion cross-attention distributions and final image quality.

**Результат:** This reduces computational overhead while improving final output quality.Diffusion Probe is model-agnostic, efficient, and broadly applicable, offering a practical solution for improving T2I generation efficiency through early quality prediction.

---

## 55. Evolve to Inspire: Novelty Search for Diverse Image Generation

**Link:** [https://www.semanticscholar.org/paper/84c90e8d86bfcadb6d612d961d77f094b29a31b1](https://www.semanticscholar.org/paper/84c90e8d86bfcadb6d612d961d77f094b29a31b1)

**Проблема:** Text-to-image diffusion models, while proficient at generating high-fidelity im- ages, often suffer from limited output diversity, hindering their application in exploratory and ideation tasks.

**Метод:** Existing prompt optimization techniques typically target aesthetic fitness or are ill-suited to the creative visual domain.

**Результат:** Ablation studies confirm the efficacy of emitters.

---

## 56. Reverse Prompt: Cracking the Recipe Inside Text-to-Image Generation

**Link:** [https://www.semanticscholar.org/paper/43cba35a8933d5f33fd5d0b3c4b15b366b732939](https://www.semanticscholar.org/paper/43cba35a8933d5f33fd5d0b3c4b15b366b732939)

**Проблема:** Text-to-image generation has become increasingly popular, but achieving the desired images often requires extensive prompt engineering.

**Метод:** In this paper, we explore how to decode textual prompts from reference images, a process we refer to as image reverse prompt engineering.

**Результат:** More importantly, we can easily create novel images with diverse styles and content by directly editing these reverse prompts.

---

## 57. ReflectCAP: Detailed Image Captioning with Reflective Memory

**Link:** [https://www.semanticscholar.org/paper/68a13010d3915ff54dbdd86e7f5a423dfcceea42](https://www.semanticscholar.org/paper/68a13010d3915ff54dbdd86e7f5a423dfcceea42)

**Проблема:** Detailed image captioning demands both factual grounding and fine-grained coverage, yet existing methods have struggled to achieve them simultaneously.

**Метод:** We address this tension with Reflective Note-Guided Captioning (ReflectCAP), where a multi-agent pipeline analyzes what the target large vision-language model (LVLM) consistently hallucinates and what it systematically overlooks, distilling these patterns into reusable guidelines called Structured Reflection Notes.

**Результат:** This makes high-quality detailed captioning viable under real-world cost and latency constraints.

---

## 58. GMAIL: Generative Modality Alignment for generated Image Learning

**Link:** [https://www.semanticscholar.org/paper/1f925d2a62f6e3276b591a1368fc091a4074437c](https://www.semanticscholar.org/paper/1f925d2a62f6e3276b591a1368fc091a4074437c)

**Проблема:** Generative models have made it possible to synthesize highly realistic images, potentially providing an abundant data source for training machine learning models.

**Метод:** Despite the advantages of these synthesizable data sources, the indiscriminate use of generated images as real images for training can even cause mode collapse due to modality discrepancies between real and synthetic domains.

**Результат:** It also shows positive generated data scaling trends and notable enhancements in the captioning performance of the large multimodal model, LLaVA.

---

## 59. Value-Aligned Prompt Moderation via Zero-Shot Agentic Rewriting for Safe Image Generation

**Link:** [https://www.semanticscholar.org/paper/8256768881850042a773094d7977abd6f02c25f5](https://www.semanticscholar.org/paper/8256768881850042a773094d7977abd6f02c25f5)

**Проблема:** Generative vision-language models like Stable Diffusion demonstrate remarkable capabilities in creative media synthesis, but they also pose substantial risks of producing unsafe, offensive, or culturally inappropriate content when prompted adversarially.

**Метод:** Current defenses struggle to align outputs with human values without sacrificing generation quality or incurring high costs.

**Результат:** These results highlight VALOR as a scalable and effective approach for deploying safe, aligned, and helpful image generation systems in open-world settings.

---

## 60. Personalizing Text-to-Image Generation to Individual Taste

**Link:** [https://arxiv.org/abs/2604.07427v1](https://arxiv.org/abs/2604.07427v1)
**Year:** 2026

**Проблема:** Modern text-to-image (T2I) models generate high-fidelity visuals but remain indifferent to individual user preferences.

**Метод:** While existing reward models optimize for "average" human appeal, they fail to capture the inherent subjectivity of aesthetic judgment.

**Результат:** We release our dataset and model to facilitate standardized research in personalized T2I alignment and subjective visual quality assessment.

---

## 61. Endogenous Reprompting: Self-Evolving Cognitive Alignment for Unified Multimodal Models

**Link:** [https://www.semanticscholar.org/paper/8a5c529f9c45a61cef1f1883c0a9ff36a35eea04](https://www.semanticscholar.org/paper/8a5c529f9c45a61cef1f1883c0a9ff36a35eea04)

**Проблема:** Unified Multimodal Models (UMMs) exhibit strong understanding, yet this capability often fails to effectively guide generation.

**Метод:** We identify this as a Cognitive Gap: the model lacks the understanding of how to enhance its own generation process.

**Результат:** Experiments show that SEER consistently outperforms state-of-the-art baselines in evaluation accuracy, reprompting efficiency, and generation quality, without sacrificing general multimodal capabilities.

---

## 62. AutoPrompt: Automated Red-Teaming of Text-to-Image Models via LLM-Driven Adversarial Prompts

**Link:** [https://www.semanticscholar.org/paper/5ef58b926d69915934afd9fc8f1c67f0c6d1f519](https://www.semanticscholar.org/paper/5ef58b926d69915934afd9fc8f1c67f0c6d1f519)

**Проблема:** Despite rapid advancements in text-to-image (T2I) models, their safety mechanisms are vulnerable to adversarial prompts, which maliciously generate unsafe images.

**Метод:** Current red-teaming methods for proactively assessing such vulnerabilities usually require white-box access to T2I models, and rely on inefficient per-prompt optimization, as well as inevitably generate semantically meaningless prompts easily blocked by filters.

**Результат:** Warning: This paper contains model outputs that are offensive in nature.

---

## 63. The erasure of intensive livestock farming in text-to-image generative AI

**Link:** [https://www.semanticscholar.org/paper/dc6374f0563ed0c6d513d36ef3147d8206a173b2](https://www.semanticscholar.org/paper/dc6374f0563ed0c6d513d36ef3147d8206a173b2)

**Проблема:** Generative AI (e.g., ChatGPT) is increasingly integrated into people's daily lives.

**Метод:** While it is known that AI perpetuates biases against marginalized human groups, their impact on non-human animals remains understudied.

**Результат:** While OpenAI introduced prompt revision to mitigate bias, in the case of farmed animal production systems, it paradoxically introduces a strong bias towards unrealistic farming practices.

---

## 64. Wolf: Dense Video Captioning with a World Summarization Framework

**Link:** [https://www.semanticscholar.org/paper/a469471c93fc6e99a5e71d8aaffdd0619df91d2f](https://www.semanticscholar.org/paper/a469471c93fc6e99a5e71d8aaffdd0619df91d2f)

**Проблема:** We propose Wolf, a WOrLd summarization Framework for accurate video captioning.

**Метод:** Wolf is an automated captioning framework that adopts a mixture-of-experts approach, leveraging complementary strengths of Vision Language Models (VLMs).

**Результат:** Finally, we establish a benchmark for video captioning and introduce a leaderboard, aiming to accelerate advancements in video understanding, captioning, and data alignment.

---
