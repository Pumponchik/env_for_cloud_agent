# Latent Transfer for Agents & Re-Prompters

**Дата:** 2026-07-31  
**Вопрос пользователя:** убрать текстовый bottleneck по центру — latent reasoning / latent re-prompting; есть ли то же в agentic systems (передача между агентами векторами).  
**Reading list:** [`reading_list_latent_and_bridge_channels.md`](./reading_list_latent_and_bridge_channels.md)  
**Широкая таксономия bridge:** [`report_bridge_methods_taxonomy.md`](./report_bridge_methods_taxonomy.md)

---

## 0. Вердикт

Да: **latent communication** — оформившаяся линия (2024–2026). Есть survey на ~18 методов (`2606.05711`). Тезис авторов совпадает с твоим: decode→tokens→encode теряет информацию и стоит compute.

Для T2I «векторный репромптер» — тот же принцип, только receiver = diffusion conditioner (ELLA / Think-Then-Generate), а не второй чат-агент.

---

## 1. Проблема текстового канала (словами survey)

Natural-language MAS:

1. **Cost** — полная генерация сообщений.  
2. **Information loss** — дискретизация rich hidden state в tokens.  
3. **Ambiguity / redundancy** — язык несёт связность, не только смысл.

Latent protocol передаёт continuous state напрямую.

---

## 2. Таксономия latent communication (Beyond Tokens)

Три оси:

| Ось | Варианты |
|-----|----------|
| **WHAT** | Embeddings · Hidden states · KV-caches · other activations |
| **WHICH** | Какие слои/пространства sender↔receiver align (часто нужен projection) |
| **HOW** | Concat · prepend · math op · cross-attn · cache restore/inject |

### Представители

| Paper | arXiv | WHAT | Режим |
|-------|-------|------|-------|
| **Coconut** | `2412.06769` | last hidden as next input | Latent CoT *внутри* 1 модели |
| **LatentSeek** | `2505.13308` | latent policy gradient @ test time | Latent CoT / search |
| **Interlat** | ACL 2026 | last hidden (+ compress) | Agent↔agent |
| **LatentMAS** | `2511.20639` | KV working memory + latent thoughts | Training-free MAS |
| **DiffMAS** | `2604.21794` | KV trace as *learnable* channel | Trained latent MAS |
| **Cache-to-Cache** | `2510.03215` | KV semantic transfer | Direct LLM↔LLM |
| **KVComm / Q-KVComm** | `2510.03346` / `2512.17914` | Selective / compressed KV | Efficiency |
| **Thought Communication** | `2510.20733` | hidden «thoughts» | Multiagent |
| **State Delta Trajectory** | `2506.19209` | state deltas | Augment text MAS |
| **Mixture of Thoughts** | `2509.21164` | aggregate expert thoughts | Not just what they *say* |
| **Vision Wormhole** | `2602.15382` | latent across heterogeneous agents | Multimodal MAS |
| **LCGuard / When Latent Agents Lie** | `2606.28958` | security of KV channel | Threat model |

Awesome lists: [Awesome Latent Space](https://github.com/YU-deep/Awesome-Latent-Space), [Awesome Latent CoT](https://github.com/EIT-NLP/Awesome-Latent-CoT).

---

## 3. Связь с T2I bridge

| Agent latent idea | T2I analogue |
|-------------------|--------------|
| Agent A → vectors → Agent B | Rewriter LLM → vectors → Generator conditioner |
| Coconut continuous thought | Endogenous CoT / Think-Then-Generate embeddings |
| Shared KV working memory | Shared conditioning stream / DimFusion multi-layer states |
| Text side-channel for audit | Show short summary; rich path = latent |

### T2I papers to pair with latent-MAS reading

- ELLA `2403.05135`, SUR-adapter `2305.05189` — connector without emitting rewrite  
- Think-Then-Generate `2601.10332` — reason, pass **embeddings**  
- LI-DiT `2406.11831` — naive latent LLM encoder fails without refiners  
- MetaCanvas `2512.11464` — plan in spatial latents  
- FIBO DimFusion `2511.06876` — compress long LLM states into conditioning  

**Пока мало работ**, которые *явно* ставят latent-MAS protocol на путь rewriter→T2I. Это открытый стык двух линий: взять Interlat/LatentMAS как protocol между ролями APE-like pipeline, а в G отдать F2 connector.

---

## 4. Когда latent лучше текста (design rules)

Из survey + LatentMAS/Interlat + T2I empirics:

**Prefer latent when**
- оба модуля на одном (или aligned) backbone;  
- нужен throughput / меньше tokens;  
- хочешь сохранить uncertainty / alternatives (Coconut BFS-like);  
- human не должен читать mid-channel;  
- enrichment = semantic density, не parametric UI.

**Prefer text (or hybrid) when**
- audit / compliance / user edit of mid-artifact;  
- heterogeneous models without good projection;  
- security-sensitive (latent channels attackable — LCGuard line);  
- нужен portable API без доступа к hidden/KV;  
- spatial/numeric control → layout/schema всё равно лучше, чем «ещё latent prose».

**Hybrid (часто лучший продукт):**  
короткий text для человека + основной latent канал для модели.

---

## 5. Плюсы / минусы (кратко)

| | Latent | Text messages |
|-|--------|---------------|
| Semantic capacity | выше (меньше quantization loss) | ниже |
| Speed | выше | ниже |
| Audit / debug | плохо | хорошо |
| Cross-model | трудно | легко |
| Security | новый surface | зрелее |
| T2I fit | отлично как conditioner input | стандарт PE |

---

## 6. Практический next step для «латентного репромптера»

1. Прочитать survey `2606.05711` §4–5 + LatentMAS + Coconut.  
2. Для T2I прототипа: **ELLA-style connector** или Think-Then-Generate (embeddings out), не Multi-agent text debate.  
3. Если роли diagnose/repair/compose (как APE MAPE) — протокол между ролями = Interlat/DiffMAS; финальный emit в G = vectors.  
4. Не забывать LI-DiT: alignment слоя обязателен.  
5. Оставить optional text summary для UX.

---

## Артефакты

- Reading list (latent first, then others): [`reading_list_latent_and_bridge_channels.md`](./reading_list_latent_and_bridge_channels.md)  
- Full bridge taxonomy F1–F6: [`report_bridge_methods_taxonomy.md`](./report_bridge_methods_taxonomy.md)
