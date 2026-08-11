# Куда копать: открытые вопросы T2I captions, re-prompt и bridge

**Дата:** 2026-08-03 (обновлено после автономного аудита)  
**Полный аудит статусов + 24 новые проблемы:** [`report_open_problems_autonomous_audit.md`](./report_open_problems_autonomous_audit.md)  
**Вход:** база репо + параллельный arXiv/web search по length / PE gating / structure / latent bridges / emerging areas.  
**Цель:** короткая карта «за что ухватиться»; детали и ложные закрытия — в полном аудите.

Связанные: [`report_bridge_methods_taxonomy.md`](./report_bridge_methods_taxonomy.md) · [`reading_list_reprompter_latent_and_alt_channels.md`](./reading_list_reprompter_latent_and_alt_channels.md) · [`fundamental_papers_reprompt_reading_list.md`](./fundamental_papers_reprompt_reading_list.md)

---

## 0. Короткий вердикт (после аудита)

Поле **не** «всё сделали labs». Главный апдейт: Seed `2607.29679` сильно закрывает тезис «длина NL = информация» и даёт Matched NL evidence, что **structure ≠ просто length**. Но:

- head-to-head рецептов длины (**Brack / i1 / FIBO / Seed-SP**) — **нет**;  
- predictive PE gating *до* generate — **нет** (есть только post-hoc TARA/VisualPrompter);  
- latent/soft vs text PE @ matched FLOPs на frozen DiT — **нет**;  
- bias schema expanders — **нет** (FairPro только prose);  
- oracle-gap / compute allocation / open GPG-ED — **новые топовые дырки**.

---

## 1. Сквозные темы — статус одной строкой

| ID | Тема | Статус |
|----|------|--------|
| T1 | Recipe tournament random vs long+rewrite vs structured | **OPEN** |
| T2 | Realizability filter до generate | **PARTIAL** (FaithRewriter offline; нет cheap pre-filter) |
| T3 | Predictive PE gating + oracle gap | **OPEN** |
| T4 | Structure ⊥ length | **PARTIAL** (`2607.29679` Matched NL) |
| T5 | Schema interoperability | **OPEN** |
| T6 | Attribute leakage / TaBR-like open bench | **OPEN** |
| T7 | Faithfulness / provenance revised_prompt | **OPEN** |
| T8 | Latent/soft vs text PE @ matched FLOPs | **OPEN** |
| T9 | Per-stage credit assignment | **OPEN** |
| T10 | Judge drift continuous monitoring | **PARTIAL** (GenEval 2) |
| T11 | Prompt-addressable ceiling | **OPEN** |
| T12 | Bias/diversity schema + PE style collapse | **PARTIAL** (FairPro prose) |

Новые топовые (N01–N03 и др. — полный список в аудите): **diffusability×promptability meters**, **test-time compute allocation**, **oracle-gap benchmark**, **open GPG/ED**, **multilingual PE**, **T2I→T2V transfer**, **PE injection**, **WK vs composition conflict**, **text-render vs rewrite**.

---

## 2. Ранжированный backlog (топ)

1. ★★★★★ Oracle-gap PE gating (enhance|skip|cost)  
2. ★★★★★ Recipe tournament A/B/C/E на одном backbone  
3. ★★★★★ Compute: PE tokens vs diffusion steps vs agentic rounds  
4. ★★★★☆ Bridge bakeoff text/soft/latent/layout/schema @ matched FLOPs  
5. ★★★★☆ Open information metrics + Diffusability×Promptability split  
6. ★★★★☆ Schema IR round-trip + bias audit expanders  
7. ★★★★☆ Provenance ledger / faithfulness audit  
8. ★★★★☆ Prompt-addressable fraction of residual errors  

Детали экспериментов — §5 полного аудита.

---

## 3. Казалось открытым → нашёлся ответ

| Вопрос | Статус | Где |
|--------|--------|-----|
| NL length масштабирует conditioning? | **Нет** | `2607.29679`, DetailMaster |
| Structure только из длины? | **Скорее нет** | Matched NL `2607.29679` |
| PE can hurt? | **Да** | AtelierEval, GenEval 2 |
| Visual grounding для rewriter training? | **Частично** | FaithRewriter `2606.08492` |
| Soft tokens для alignment? | **Да** (≠ PE bakeoff) | SoftREPA / AGSM |
| Demographic bias prose PE? | **Да** | FairPro `2512.04981` |
| Endogenous PE? | **Да** | SEER |
| Predictive gating / recipe tournament / schema standard / DiT latent bakeoff | **Всё ещё нет** | см. аудит |

---

## 4. С чего начать

| Интерес | Пакет |
|---------|--------|
| Быстрый impact | Oracle-gap gating на GenEval 2 |
| «Закрыть спор области» | Brack vs i1 vs FIBO-style vs Seed-SP |
| Systems / latent | Matched-FLOPs bakeoff на frozen DiT |
| Metrics | Open GPG/ED + diffusability/promptability |
| Risk | Schema bias + PE injection + diversity collapse |

Не начинать: always-on aesthetic rewriter; agentic без cost/gate; MAS latent messaging.

---

## 5. Чеклист paper (2026)

Eval vs **original** · information-matched controls · skip/enhance/oracle · diversity+bias · назвать train caption law · schema: structure vs length vs matched-info prose · latent: vs strong text PE @ matched compute · open seeds/judges · provenance добавок PE.

---

## Источники (ядро)

Brack `2506.16679` · i1 `2606.11289` · GenEval 2 `2512.16853` · FIBO `2511.06876` · **context-scaling `2607.29679`** · **FaithRewriter `2606.08492`** · APE `2606.00204` · ISS `2510.12041` · TARA `2607.18724` · SEER `2601.20305` · FairPro `2512.04981` · SoftREPA `2503.08250` · PromptLoop `2510.00430` · AtelierEval `2605.22645` · Format Tax `2604.03616` · Detailness `2505.15172`

Полный список якорей аудита: [`report_open_problems_autonomous_audit.md`](./report_open_problems_autonomous_audit.md) §10.
