# Non-Textual Re-Prompter Channels for T2I

**Дата:** 2026-07-31  
**Scope:** только bridge **re-prompter / enrichment module → image generator**.  
**Вне scope:** latent communication между LLM-агентами (MAS).  
**Reading list:** [`reading_list_reprompter_latent_and_alt_channels.md`](./reading_list_reprompter_latent_and_alt_channels.md)

---

## 0. Вопрос

Классика:

```
user → LLM пишет новый текст → text encoder → vectors → G
```

Нужны способы, где enrichment **не** (или не главным образом) через текстовый rewrite:

1. **Латентный / векторный** re-prompter  
2. **Другие** каналы: schema, layout, endogenous, action space  

---

## 1. Латентный re-prompter (главная ветка)

### 1.1 Connector: LLM hidden → continuous conditioning

| Paper | ID | Wire to G | Freeze G? |
|-------|-----|-----------|-----------|
| ELLA | `2403.05135` | TSC outputs encoder_hidden_states | yes |
| SUR-adapter | `2305.05189` | adapter embeddings from short prompt | mostly |
| LaVi-Bridge | `2403.07860` | adapter between LM and vision | LoRA |
| LLM4GEN | `2407.00737` | fused CLIP+LLM features | plug-in |
| GlueGen | `2303.10056` | GlueNet-aligned encoder features | yes |
| Think-Then-Generate | `2601.10332` | **embeddings of reasoned prompt** | co-train |
| RISE-T2V | `2511.04317` | LLM next-token hiddens as implicit rephrase | adapter |
| DATE | `2510.23974` | per-step text-emb re-opt | training-free |
| UniFusion/VERIFI | `2510.12789` | in-model rewrite token embeddings | VLM+DiT |
| DimFusion (FIBO) | `2511.06876` | multi-layer LLM fused on emb-dim | co-train |
| Semantic Routing | `2602.03510` | gated LLM-layer fusion | yes/partial |

**Идея:** re-prompter = LLM(+connector), продукт = **векторы**, не revised_prompt string.

**Caution:** LI-DiT `2406.11831` — naive swap CLIP→LLM encoder degradирует following.

### 1.2 Soft / test-time embedding optimization

| Paper | ID | Idea |
|-------|-----|------|
| Manipulating Embeddings | `2308.12059` | Gradients on prompt embedding |
| PEO | `2510.02599` | Training-free emb enhancement vs rewrite |
| IPGO | `2503.21812` | Continuous injections + constraints |
| PEZ | `2302.03668` | Soft opt → hard tokens |
| DPO-Diff | `2407.01606` | Discrete opt via embedding relaxation |
| TextCraftor | `2403.18978` | Reward-tune text encoder |

**Идея:** «re-prompt» = сдвиг в continuous space, иногда без нового NL.

### 1.3 Когда это правильный ответ на bottleneck

Да, если bottleneck = **дискретизация в слова перед encode**.  
ELLA/SUR/Think-Then-Generate / PEO — прямые ответы.

Нет как единственный ответ, если нужны: точные bbox/RGB (schema), spatial plan (layout), audit string, чужой API без access к embeddings.

---

## 2. Другие каналы re-prompter → G

| Канал | Что передаётся | Якоря | vs latent |
|-------|----------------|-------|-----------|
| **Schema** | JSON / fields / numbers | FIBO, BBQ, Ideogram 4 | Дискретный, но parametric-точный |
| **Layout** | boxes / regions / draft | LMD, RPG, MetaCanvas, SCoT | Геометрия; SCoT: дополняет text, не заменяет |
| **Endogenous** | internal CoT / descriptors | T2I-R1, SEER, Hunyuan 3 | Нет внешнего re-prompter |
| **Action** | attn / weights / noise / latents | A&E, PAE, PromptLoop, RAISE | Не «сообщение», а рычаг sampler |
| **Text PE** | revised prose | PromptEnhancer, APE, TARA | Зрелый; portable; lossy mid-hop |

---

## 3. Рекомендуемый порядок чтения (только re-prompter)

1. ELLA → SUR-adapter → Think-Then-Generate  
2. LI-DiT (негатив) → DimFusion / Semantic Routing  
3. PEO + IPGO (emb opt)  
4. FIBO/BBQ (schema) · LMD/SCoT (layout) · T2I-R1/SEER (endogenous) · PromptLoop/RAISE (action)  
5. PromptEnhancer / GenEval 2 (текстовый контраст)

---

## 4. Design takeaway

Для «убрать текстовый middle hop» в **re-prompter→G**:

```
preferred prototype:
  user text → LLM/VLM (optional internal CoT)
           → connector / emb-opt  → continuous cond → G
  optional: short text log for UX only
```

Не смешивать с MAS latent messaging — там другой receiver (другой LLM), другие constraints (KV share, audit между агентами).

---

См. также широкую F1–F6 карту: [`report_bridge_methods_taxonomy.md`](./report_bridge_methods_taxonomy.md).
