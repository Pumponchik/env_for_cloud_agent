# Как работают диффузионные модели для текста

Связано с: [`research/text-diffusion/`](./research/text-diffusion/), [`take_text_diffusion_dofs.md`](./take_text_diffusion_dofs.md), [`report_text_diffusion_landscape.md`](./report_text_diffusion_landscape.md).

Этот документ — механика «с нуля». Степени свободы и SOTA — отдельно в DOF-разборе.

---

## 1. Зачем вообще диффузия для текста

Классическая LLM учится **авторегрессионно**: \(p(x_1)p(x_2\mid x_1)\cdots p(x_n\mid x_{<n})\). Генерация строго слева направо, один токен за шаг декодера.

Диффузионная языковая модель учится **разрушать и восстанавливать** всю последовательность (или блок):

- на обучении модель видит частично испорченный текст и учится его чинить;
- на инференсе стартует из «шума» (часто все `[MASK]`) и за несколько шагов параллельно восстанавливает токены.

Идея заимствует успешный рецепт из изображений (DDPM / score-based), но текст **дискретен**, поэтому «гауссовский шум в пикселях» нельзя перенести буквально. Вся область — про то, **как именно** определить шум и обратный шаг для токенов.

---

## 2. Общий каркас (непрерывный прототип)

В непрерывном случае (картинки, или эмбеддинги слов):

1. **Forward / corruption.**  
   \(q(x_t \mid x_0)\) — гладкое зашумление к простому приору \(x_T \sim \mathcal{N}(0,I)\).
2. **Reverse / denoising.**  
   Нейросеть \(p_\theta(x_{t-1}\mid x_t)\) (или score \(s_\theta(x_t,t)\)) учится обращать шум.
3. **Sampling.**  
   \(x_T \to x_{T-1} \to \cdots \to x_0\).

Для текста этот каркас сохраняется, меняются:

- пространство состояний \(x\) (токены / эмбеддинги / латенты);
- семейство \(q\);
- что именно предсказывает сеть;
- как семплировать при категориальных переменных.

---

## 3. Три больших семейства представлений

### A. Continuous embedding diffusion

Токены отображают в вещественные векторы, диффузия идёт в \(\mathbb{R}^d\), в конце — проекция обратно в словарь (rounding / argmax / learned rounding).

- Исторический якорь: **Diffusion-LM** (контроллируемая генерация градиентами по непрерывным латентам).
- Плюсы: доступны continuous guidance, classifier gradients, знакомый DDPM math.
- Минусы: rounding error, геометрия эмбеддингов, часто хуже pure discrete ELBO на language modeling.

### B. Discrete token diffusion

Состояние — категориальный токен из словаря \(V\). Forward — марковская цепь по категориям.

Типичные corruption:

| Тип | Что происходит с токеном | Интуиция |
|-----|--------------------------|----------|
| **Absorbing / mask** | с ростом \(t\) токен уходит в `[MASK]` и остаётся там | как BERT-маска, но с расписанием по \(t\) |
| **Uniform** | токен равномерно прыгает по \(V\) | «перемешивание» символов |
| **Absorbing+uniform mixtures** | комбинации | компромисс edit vs mask |

Обратный процесс предсказывает распределение чистого токена / rates / concrete score. На практике **absorbing (masked) diffusion** доминирует в современных diffusion LLM: обучение близко к masked LM loss, семплирование — iterative unmasking.

Якоря: **D3PM**, **MDLM**, **MD4**, **SEDD**, **RADD**.

### C. Latent / compressed continuous diffusion

Сначала encoder сжимает текст в непрерывный латент (часто seq2seq), диффузия в латенте, затем decode. Близко к DiffuSeq / latent diffusion for sequences. Чаще для conditional generation (translation, summarization), реже как drop-in LLM.

---

## 4. Время: дискретное vs continuous-time

- **Discrete-time.** Как DDPM: фиксированные \(T\) шагов, transition matrices \(Q_t\). Проще инженерить, шаг = гиперпараметр.
- **Continuous-time (CTMC).** Состояние — токен; эволюция — rates между категориями. Score / ratio matching (**SEDD**, работы Campbell et al.). Красивая теория, гибкие солверы, но сложнее реализация и численная устойчивость.

На практике large diffusion LMs часто используют **discrete absorbing schedules**, иногда с continuous-time обоснованием ELBO.

---

## 5. Что учит модель (parameterization + objective)

Модель обычно — **двунаправленный Transformer** (видит всю зашумлённую последовательность). Варианты того, *что* она выдаёт:

1. **\(x_0\)-prediction.** Логиты чистых токенов в каждой позиции; loss ≈ weighted cross-entropy по замаскированным / зашумлённым позициям (MDLM-style).
2. **Concrete score / rates.** Отношения вероятностей переходов (SEDD); ближе к score matching.
3. **Mean / posterior param.** Параметризация \(p(x_{t-1}\mid x_t)\) напрямую (D3PM).

Для absorbing diffusion при правильном взвешивании ELBO **схлопывается к простой CE на масках** — поэтому обучение выглядит обманчиво похоже на BERT / masked LM, а отличие проявляется в **многошаговом семплировании** и расписании.

---

## 6. Как выглядит генерация

Типичный masked diffusion decode:

1. Инициализировать последовательность длины \(n\) как `[MASK]…[MASK]` (или шум + известный prompt-prefix).
2. Для \(t = T,\ldots,1\):
   - сеть предсказывает распределение токенов на замаскированных местах;
   - по schedule / confidence выбрать, какие позиции **раскрыть** на этом шаге;
   - остальные оставить MASK (или **remask** низкоуверенные — важный рычаг качества).
3. Получить полностью раскрытый текст.

Отличия от AR:

- много позиций обновляются **параллельно**;
- можно **редактировать середину** без переписывания префикса;
- latency зависит от числа denoising steps, не от \(n\) один-в-один (хотя \(n\) всё ещё влияет на compute внимания);
- нет бесплатного KV-cache как у causal AR — отсюда **Block Diffusion** и гибриды.

---

## 7. Условие (conditioning) и guidance

- **Prompt as clean prefix / context:** часть токенов зафиксирована, диффундирует только continuation / span.
- **Classifier-free guidance (CFG):** одновременно train conditional + unconditional; на семпле сдвиг logits — работает и в discrete, но чувствителен к schedule.
- **Classifier / reward / energy guidance:** градиенты или accept-reject по внешней модели (сложнее в discrete).
- **Constrained / structured decoding:** маски допустимых токенов, grammar, FSA — естественно стыкуются с iterative fill.

---

## 8. Гибриды с авторегрессией

Чистая полная параллельная диффузия на длинном контексте дорогая и без KV-cache. Активная линия:

- **Block Diffusion (BD3-LM):** генерировать блок авторегрессионно по блокам, внутри блока — diffusion; появляется cache между блоками.
- **Semi-AR / any-order / AR-Diffusion:** порядок раскрытия не строго left-to-right, но и не fully parallel.
- **AR backbone → diffusion fine-tune (DiffuLLaMA-style):** взять pretrained causal LM и адаптировать под diffusion objective — путь к scale без training from scratch.

---

## 9. Где «качество» реально ломается

Даже до списка DOF полезно держать failure modes:

- **Too few steps** → недочищенный шум, локальная бессмыслица.
- **Too greedy unmasking** → ранние ошибки закрепляются (нет AR teacher-forcing safety).
- **Remasking policy** плохо настроена → либо застревание, либо разрушение уже хороших токенов.
- **Train/infer schedule mismatch** → как length mismatch в T2I.
- **Rounding / embedding geometry** в continuous path.
- **Global consistency vs local fluency** tradeoff при параллельном decode.
- **Long context** без block/hybrid → compute и quality деградируют иначе, чем у AR.

---

## 10. Карта «что читать дальше»

| Вопрос | Куда |
|--------|------|
| Обзор областей и что горячо в 2025–2026 | [`report_text_diffusion_landscape.md`](./report_text_diffusion_landscape.md) |
| Степени свободы → SOTA → эксперименты | [`take_text_diffusion_dofs.md`](./take_text_diffusion_dofs.md) |
| Структурированный corpus / fields | [`research/text-diffusion/`](./research/text-diffusion/) |

---

## 11. Одной формулой

**Text diffusion = выбрать (представление × процесс порчи × objective × sampler) и учить модель обращать порчу; качество = насколько этот выбор согласован на train и infer, плюс guidance и schedule.**

Именно эти множители — степени свободы следующего артефакта.
