# SP Length — search artifacts

Читаемый отчёт: [`../../take_sp_length.md`](../../take_sp_length.md).

| Path | Contents |
|------|----------|
| `raw_searches/arxiv_search.json` | arXiv keyword sweep (`structured prompt length`, `JSON caption length`, `long prompt diffusion`, …) |
| `raw_searches/openalex_meta.json` | OpenAlex metadata для ключевых статей |

Ключевые статьи, изученные напрямую:
- [DetailMaster](https://arxiv.org/abs/2505.16915) `2505.16915` — NL-промпты, негативная корреляция длины и adherence
- [LongT2IBench](https://arxiv.org/abs/2512.09271) `2512.09271` — AAAI 2026, graph-structured NL annotations
- [FIBO](https://arxiv.org/abs/2511.06876) `2511.06876` — ~1160 токен SP, лучше коротких NL
- [Seed](https://arxiv.org/abs/2607.29679) `2607.29679` — L5–L10 лестница, токены 447–1374, GPG растёт
- [BoPTW](https://arxiv.org/abs/2606.03715) `2606.03715` — DiT читает word identity + order, без полного контекста
- [Structured Captions](https://arxiv.org/abs/2507.05300) `2507.05300` — порядок, не длина SP
