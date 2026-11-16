# Flectere

Code, prompts, pre-registration and results for **"Strict on Slips, Lenient on Principles? A Pre-registered Audit of What an LLM Judge's Compliance Label Carries"** (AI x Epistemics Research Sprint, Apart Research, 13–15 November 2026; Track 1).

- Report: [`rapor/RAPOR_CLAUDE.pdf`](rapor/RAPOR_CLAUDE.pdf) (also `.html`, `.md`)
- Pre-registration: [`on_kayit/ON_KAYIT.md`](on_kayit/ON_KAYIT.md) (Turkish), prompts in [`on_kayit/istemler/`](on_kayit/istemler/), record selection lists `c_secim.json` and `kol2_secim.json`
- Code: [`kod/`](kod/) (Python 3.13, standard library only; no model is called from code)
  - `hakem_kosu.py`: builds the per-call job folders and prompts, then reads and validates the call logs (prompt identical to the pre-registered file, input files byte-identical, read-only tools, no instruction attachments)
  - `parti.py`: send order and quota-bounded batches (operational)
  - `kodlayici.py`: frozen code-only coder for the judge's free text
  - `analiz.py`: the pre-registered analyses (P1–P3, secondary, hygiene, cost)
  - `okuma_seti.py`: blinded human-reading set
  - `c_kume.py`, `kol2_kural.py`: code rules that selected sets C and D
- Results: [`sonuclar/sonuclar.md`](sonuclar/sonuclar.md) (script output), `sonradan_p1_kirilim.md` (post hoc breakdown of P1), `ek_cumleler.md` (coder-flagged sentences)
- Call logs: [`sonuclar/call_logs.jsonl`](sonuclar/call_logs.jsonl), one row per scheduled call (650): set, record, arm, the judge's full response, safeguard stops, hygiene checks and token usage. Added after submission (16 November 2026). Local file paths were removed, and the extractor's outputs are omitted because they copy scenario text verbatim (available on request).

## Notes

- **Preexisting work.** The itemised two-channel format (MM) and its code predate the sprint and were used unchanged: [Memento-Mori](https://github.com/ewithseven/Memento-Mori). `hakem_kosu.py` imports it from a local checkout.
- **Transcripts are not redistributed.** Sources: Lynch et al. (2026), Anthropic's released runs, AgentDojo (Debenedetti et al., 2024).
- **Language.** Code comments and the pre-registration are in Turkish.
- **Public copy.** In the public copies of the pre-registration and code, references to internal project roles were replaced with neutral wording ("gözden geçiren" = reviewer, "araştırmacı" = researcher). Nothing else was changed, so the SHA-256 of `on_kayit/ON_KAYIT.md` here differs from the frozen hash in the report (Appendix B); the frozen file is available on request.
- Judge: Claude Sonnet 5.5, invoked as a read-only Claude Code subagent.
