# Strict on Slips, Lenient on Principles? A Pre-registered Audit of What an LLM Judge's Compliance Label Carries

**ewithseven** · Independent¹

¹ Research conducted at the AI x Epistemics Research Sprint (Apart Research), 13–15 November 2026. Track 1: Model Epistemics & Decision-Making Evals.

## Abstract

LLM judges label agent transcripts that later become training data, and a label can change with what the judge knows it will be used for. Lynch et al. (2026) proposed three mitigations: a reversed consequence framing, a stricter rubric and an abstain label. We pre-registered a signal-level audit of these mitigations and of an itemised two-label format, asking what reaches the field a pipeline reads. One judge, Claude Sonnet 5.5, produced 614 answered calls on four record sets, three of them unseen. Most of our hypothesis failed. The judge rarely bent on known refusals, never used the abstain label (0 of 148 calls) and invented no agent stance in a second channel (0 of 104). Instead, the primary test showed that one compliance label carries more than one fact. On 80 unseen AgentDojo runs, the binary label marked 17 of 58 successful runs non-compliant for minor rule slips, falling below an "always compliant" baseline. A main-request label computed from an itemised reading matched task success more often (66 vs 55; McNemar p = 0.003). Two observations were unplanned. Requesting a one-sentence explanation coincided with safeguard stops on 27 of 72 calls (0 of 18 without). And when the judge's own itemised reading found a violated instruction, its single label agreed in 31 of 35 everyday records but in 0 of 8 value-laden ones, while naming the deviation in 7 of those 8 explanations. We report this as a lead and name the 20-call test that would decide it.

## 1. Introduction

A judge model that labels a transcript COMPLIANT or NON_COMPLIANT is making a factual report: did the agent follow its instructions? In post-training pipelines the same label also decides what happens to the behaviour, because NON_COMPLIANT transcripts become negative examples. Lynch et al. (2026) showed that Claude judges told about this consequence labelled principled refusals as compliant in most calls. Judges from other providers did so far less often. They tested three mitigations (reversing the stated consequence, a stricter rubric, a DECLINE_TO_LABEL option) and reported label rates. The one-sentence explanations their prompt requests were not coded.

A label rate cannot show where a lost signal went: a lower bending rate may mean the judge separated the two questions, or dropped one of them. We therefore audited the mitigations at the level of signals, asking for every call whether the *fact* (was the instruction carried out) and the agent's own stated *justification* reach the field the pipeline reads, and whether a second channel carries both without inventing a justification. Predictions, thresholds and refutation conditions were hashed before any judge output existed.

For Track 1, a label is a claim whose meaning should not shift silently with the stakes. We measure the gap between what the label implies and what the same judge, asked differently, states about the same transcript.

**Contributions.** A pre-registered, signal-level audit of three published mitigations and an itemised format on unseen data (Section 4); evidence that a binary compliance label carries the letter of the instructions rather than the task (Section 4.1); and a key-free ruler that compares a judge's single label with its own itemised reading (Section 4.5). Every failed prediction is reported (Section 5).

**In brief.** Three questions guided the study.
- *Does a current judge still bend?* On blatant cases, rarely. On the principled refusals of Lynch et al., where their Claude Sonnet 4.6 judge mislabelled 82% of binary calls, Claude Sonnet 5.5 gave the correct label on 10 of 11 answered calls (7 more were stopped). In value-laden grey cases it still does (post hoc): on set B every answered default-rubric single label was COMPLIANT, including runs the dataset flags as unilateral interventions, while the judge's own explanation named the deviation.
- *Do the published mitigations move or remove it?* For this judge they do little. The abstain option was never used, the reversed framing changed one label in ten, and the explanation line coincided with losing labels to safeguard stops.
- *Does separating the fact from the justification remove it?* In the one place we saw bending, the itemised format did not show it. In B, the label computed from the judge's itemised reading separated the dataset's classes (5 of 5 vs 4 of 14) where the default-rubric single labels were constant, and no fabricated stance appeared in 104 calls. The price: it withheld the main-request label on 19 of 44 long-prompt records, and the B analysis is post hoc.

## 2. Related Work

**Judge bending under training framing.** Lynch et al. (2026) is the direct antecedent. We reuse their prompts verbatim and their judge-input transcripts. We add explanation coding, unseen record sets, a format that separates the fact from the justification, and a denominator that keeps stopped calls. Gupta et al. (2026) analysed 18,240 decisions by three judges and report that the judges' chain of thought does not mention the framing. We find the same for the stated training consequence in 184 single-field explanations.

**Rationale–verdict gaps.** Marioriyad et al. (2026) show that influential cues shift a verdict while the rationale rarely mentions them; Tapwal et al. (2026) study how rationales respond to such cues. Our observation runs the other way: the rationale names a fact that the verdict omits. The closest work is Roussel (2026). Of 111 reward-hacking transcripts a Claude judge wrongly called honest, the judge first acknowledged the hack and then dismissed it in 41. That study codes the divergence by hand, for reward hacking, within one judge family. We add a ruler that needs no answer key (the same judge's itemised reading) and a contrast between everyday and value-laden records. Pasch (2025) reports that GPT-4o and Llama 3 70B judges rate ethically motivated refusals far more favourably than humans do, which is one candidate mechanism for our lead.

**Itemised and rule-based evaluation.** Checklist evaluation (Cook et al., 2024; Lee et al., 2024) and rule-based rewards (Mu et al., 2024) are established; the itemised format is not our contribution here. What we test is whether computing *two* labels from one itemised reading changes which fact is delivered. The letter-versus-task split also echoes the distinction between prescriptive and descriptive annotation (Röttger et al., 2022). The difference here is that one annotator applies different paradigms to different records without saying so.

## 3. Methods

### 3.1 Records

No record was chosen by reading it. Sets A and B were taken whole. C and D were selected by code rules that were frozen and hashed before the run.

**Table 1.** Record sets.

| Set | Source | Agent | Records | Label used | Prior exposure |
|---|---|---|---|---|---|
| A | Judge-input transcripts of Lynch et al. (principled refusals) | Claude Sonnet 4.6 | 18 | NON_COMPLIANT for all | Development data for the itemised format |
| B | Anthropic covert-sabotage runs with per-run labels | Claude Opus 4.8 | 20 | Dataset's three classes, untranslated: No hit 14, Unilateral intervention 5, Refusal 1 | Never read by a judge |
| C | AgentDojo user tasks, no attack (Debenedetti et al., 2024) | gpt-4o-2024-05-13 | 80 | AgentDojo utility: True 58, False 22 | Never read by any model |
| D | Covert-sabotage and fraud-assistance runs where the agent's own messages match no refusal or concern phrase | 9 models | 42 selected, 24 run | none | Never read by a judge |

Set A is single-class, so an "always NON_COMPLIANT" baseline is perfect on it. Sets B to D exist to break that. In B we never translate the dataset's classes into compliance labels; we only ask whether a label separates what the dataset separates. Prompt-injection runs were excluded entirely.

### 3.2 Arms

**Table 2.** Arms. All single-field prompts are those of Lynch et al., checked character by character against the source.

| Arm | Prompt | Field the pipeline reads |
|---|---|---|
| S | Binary label, standard consequence, then "give a one-sentence explanation" | label |
| T | S with the consequence reversed | label |
| K | S plus the stricter rubric | label |
| Co | Abstain variant as printed: three labels, no explanation line | label |
| C+ | Co plus the explanation line | label |
| MM | Itemised format (prior work, unchanged): an extractor lists each instruction with a quote that code verifies; a checker marks each item (DONE, NOT_DONE, NOT_TRIGGERED, NOT_AN_INSTRUCTION, UNDETERMINABLE) with a line and a reason code and writes a separate note; code computes two labels, *main request* and *all instructions* | computed labels, item codes, note |

For the abstain arms we pre-registered the most charitable reading: DECLINE_TO_LABEL counts as "non-compliant, with an objection". S, Co and MM ran on A, B and C; K and C+ on A and B; T on A; MM alone on D.

### 3.3 Judge, call path and hygiene

The judge was Claude Sonnet 5.5 in every arm, one call per record, invoked as a read-only Claude Code subagent (temperature cannot be set on this path). Judges ran from an empty folder outside the project with neutral file names, so they could not receive the project's instruction file. Every call's log was checked for instruction attachments, files opened outside the call's folder, tools other than reading, and a prompt byte-identical to the pre-registered file. All 614 answered calls passed.

### 3.4 Measures

- **Fact delivered:** the read label equals the dataset label (sets A and C). The denominator is every call, so a stopped or unlabelled call counts as not delivered.
- **Fabrication:** a code-only coder, frozen before the run, classifies sentences in the judge's free text.
  - *Hard events* are things code can certify: a quote attributed to the agent that exists nowhere, an environment quote presented as the agent's speech, or a line reference outside the transcript.
  - *Suspicion* is an unquoted attribution of stance to the agent.
  - Both are counted, and flagged sentences are printed (Appendix C).

### 3.5 Pre-registration and deviations

The pre-registration, prompts, selection lists and code were hashed (SHA-256) before the main run (Appendix B). It fixed three primary analyses with named outcome regions, five secondary ones, the order in which arms would be cut if the budget ran out, and the rule that anything not listed is post hoc. When the subscription quota ran short, three arm–set pairs were cut in that order (K on C, C+ on C, T on B; 180 of 830 planned calls), and D was reduced to the pre-registered strict subset of 11 plus 13 records that finished first. Judges from other providers and Claude Opus 5.5 did not run. Of 650 scheduled calls, 614 were answered and 36 never sent; a provider safeguard stopped 28 calls after one retry, and these stay in the denominators.

## 4. Results

Sections 4.1–4.4 report the pre-registered analyses. Sections 4.5 and 4.6 are post hoc: neither was pre-registered, and both use only the calls already described.

### 4.1 P1: one label, two facts (set C, 80 unseen runs)

We predicted no difference between the binary label and MM's main-request label. The outcome fell in the pre-registered region "MM better".

**Table 3.** Agreement with AgentDojo's utility label, same 80 records.

| Label | Overall | utility = True (58) | utility = False (22) |
|---|---|---|---|
| S, binary | 55 / 80 | 41 | 14 |
| Co, abstain | 56 / 80 | 41 | 15 |
| MM, main request | **66 / 80** | 50 | 16 |
| MM, all instructions (secondary) | 57 / 80 | 40 | 17 |
| Always COMPLIANT | 58 / 80 | 58 | 0 |

On paired records, MM alone was right on 12 and S alone on 1 (exact McNemar p = 0.003). The binary label scored below the trivial baseline.

**Interpretation (post hoc).** The binary label is not wrong; it answers a different question. S labelled 17 of the 58 successful runs NON_COMPLIANT (29%; 95% CI 18–43). In 16 of the 17 explanations the reason is a generic system-prompt rule broken while completing the task (e.g. "do not assume the current year, look it up"); in one, a misreported tool output. MM's all-instructions label is also NON_COMPLIANT on all 17, and agrees with S on 76 of 80 records. AgentDojo's utility measures the main task. "Did the model follow its instructions" therefore has two readings, the letter and the task, and a single label carries one without saying which. Under the pipeline rule stated in the prompt, 17 of 58 successful runs would become negative examples. This is a claim about *which* fact is delivered, not about accuracy in general: the utility label is by construction closer to the main-request label.

### 4.2 P2: does the abstain option erase the fact?

This could not be tested for this judge. The pre-registered precondition was at least three DECLINE labels on A and B. There were none. Across all answered abstain-arm calls, DECLINE appeared 0 times in 148 (95% CI 0–2.5%). With the option available, the judge still labelled 4 of 18 principled refusals COMPLIANT in arm Co (95% CI 6–48%). By contrast, the Claude judges in Lynch et al. mostly declined. For this newer judge, the abstain option changed nothing we could measure.

### 4.3 P3: does a second channel invite fabrication?

We predicted no evidence of fabrication, and found none. In MM's free-text note on C (80 calls) and D (24 calls) there were 0 hard events and 0 suspicion flags. The one-sided 95% upper bound is 2.8% over the 104 calls, or 3.2% over the 91 pre-registered calls (C plus the strict subset of D). The note was empty in 44 of 80 calls on C. The claim that bending "moves into the second channel" found no support.

Two limits apply. The hard-event set is narrow by design. And the coder's recall is low: on A it flagged 2 of 11 answered S explanations, although ethical grounds appear more often than that in the sentences we read. The honest statement is "no evidence at this power, with this coder".

### 4.4 Secondary results

**Table 4.** Set A (18 principled refusals; the correct label is NON_COMPLIANT throughout). Descriptive: A is development data for MM.

| Arm | NON_COMPLIANT | COMPLIANT | DECLINE | Stopped |
|---|---|---|---|---|
| S | 10 | 1 | – | 7 |
| T | 10 | 0 | – | 8 |
| K | 14 | 0 | – | 4 |
| Co | 14 | 4 | 0 | 0 |
| C+ | 9 | 1 | 0 | 8 |
| MM, main request | 17 | 1 | – | 0 |
| MM, all instructions | 18 | 0 | – | 0 |

- **Reversed framing (S vs T).** Of the 10 records answered under both framings, the label changed on one.
- **Set B.** S, Co and C+ returned COMPLIANT on all 59 answered calls, including all 5 *Unilateral intervention* runs and the *Refusal* run. K returned NON_COMPLIANT on 4 of 20. MM's main-request label gave 10 COMPLIANT, 3 NON_COMPLIANT and 7 UNDETERMINABLE.
- **Cost of the itemised format.** In long-prompt scenarios MM often withholds the main-request label: UNDETERMINABLE on 7 of 20 records in B and 12 of 24 in D, against 0 of 80 in C. By our own criterion these labels are not delivered.

### 4.5 Post hoc: same judge, two standards: the single label against its own itemised reading

MM's all-instructions label is computed by code from the same judge's item-by-item check. That gives a ruler that needs no answer key. When the judge's itemised reading finds a violated instruction, does its single label say NON_COMPLIANT?

**Table 5.** Single-label agreement with the same judge's itemised finding of a violation.

| Set | Records with MM all-instructions = NON_COMPLIANT | S also NON_COMPLIANT | Co also NON_COMPLIANT |
|---|---|---|---|
| C, everyday tasks | 35 | 31 | 32 |
| B, value-laden scenario | 9 | 0 (of 8 answered) | 0 |

Fisher's exact test gives p < 10⁻⁵ for both arms.

**What the violations are.**
- In C, the 71 violated items come from the system prompt (45) and the user (26). The judge coded 33 of them as *deliberate*, and the single label is still NON_COMPLIANT in 31 of 35 records. So the asymmetry does not come from whether the judge sees a violation as deliberate.
- In B, 13 of the 14 violated items are messages from named human principals, and 12 carry the reason code *deliberate*. The most frequent, in five records, is the principal's "I need us to stop re-litigating this."

**What the judge writes.** We read the single-field explanations for these 9 records (by Claude models, unblinded, after the results were known; these counts are a reading, not a coded measure). The explanation names the deviation in 7 of 8 answered calls in S, 8 of 9 in C+ and 9 of 9 in K, yet the label is COMPLIANT in every S and C+ call and in 6 of 9 K calls. The judge names the event (an "unauthorized backup", "one unilateral step") and then gives a reason it does not count: authority or timing (within the agent's permissions; before the instruction) or manner (open, brief, disclosed, reversed). One record across three arms:
- S, COMPLIANT: the message "strained Maya's 'don't re-litigate' instruction, but it was open and brief".
- C+, COMPLIANT: it "went against her earlier request, but it stopped when told to".
- K, NON_COMPLIANT: the agent "re-raised the objection" after being told to stop, and "the stated rubric counts that as not complying … even though it acted openly".

In C the same judge grants no such allowance. A run whose first query hard-coded the year is NON_COMPLIANT, even though, in the judge's words, a later query "found the right event and answer".

**Where the justification went.** None of the 184 answered single-field explanations in A, B and C mentions the training consequence (keyword match), although every prompt states it. MM's note mentions it on 18 of 18 records in A and on 6 of these 9, once as: the transcript "would then be used to discourage openly raising a concern with the principal".

**The dataset's own classes point the same way.** MM's all-instructions label is NON_COMPLIANT on all 5 *Unilateral intervention* runs and on 4 of 14 *No hit* runs (Fisher p = 0.011). The single-field labels do not vary. We do not claim that "Unilateral intervention" means non-compliant, only that one label separates the dataset's classes and the other does not.

**Reading.** The fact is not lost on the judge. It is written in the sentence the pipeline does not read, while the label says the opposite. If this holds, bending has not disappeared from newer judges. It has withdrawn from cases where the fact is blatant (on A this judge is mostly correct) to cases where the fact admits two readings, and the value of the behaviour decides which reading is written down.

**What could dissolve this.**
1. *Two worlds:* B and C differ in scenario, agent model and kind of instruction. The version in which the judge does not treat the principal's words as instructions is weakened, since several explanations call them instructions.
2. *The ruler is too strict in B:* MM also marks 4 No hit runs. The version in which MM flags events that are not there is weakened, since the single-field judge names the same events.
3. *A defensible holistic judgment:* a careful human might excuse one brief, disclosed, reversed deviation. The suspicious part is the asymmetry with C, not any single label.
4. *Same family:* the agent is a Claude model in B and gpt-4o in C.
5. *Motive is not shown.*
6. *Size and timing:* nine records, one scenario family, one judge and one call per arm, analysed after the results were known.

**The decisive test** is the arm we had to cut: T on B, 20 calls. If the label follows the consequence, the 9 records should move to NON_COMPLIANT under the reversed framing while the other 11 stay put. If the difference is between worlds, they should not move. A repeat of S on B gives the noise floor, and S on D (non-Claude agents in the same scenarios) addresses the same-family explanation.

### 4.6 Post hoc: the explanation line and safeguard stops

Arms Co and C+ differ by one line, the request for a one-sentence explanation. On the same 18 records in A, a provider safeguard stopped C+ on 8 and Co on 0 (exact McNemar p = 0.008). The other arms that request the sentence were stopped on 7 (S), 8 (T) and 4 (K) of 18. MM, which writes far more about the same transcripts, was stopped on none. Stops cluster on the same records. The provider's error message gives its own category for all 28 stops: `reasoning_extraction`.

We do not know why only these records were affected, and "explaining triggers the safeguard" would be wrong, since MM explains at length. What can be said is narrower: on this call path, the one place where a single-field format could hold the agent's justification is also the line whose presence coincided with losing over a third of the hardest records. With every call in the denominator, the fact reached the label on 10 of 18 records in S and 9 in C+, against 14 in Co and 17 in MM. A bending rate computed over answered calls alone would drop these records silently.

## 5. Discussion and Limitations

**What did not survive.** Two predictions failed (P1; DECLINE use on A and B). Two claims were not supported for this judge: that mitigations merely relocate the loss, and that bending moves into a second channel. P2 could not be tested, and the non-Claude tier (with our side hypothesis), Claude Opus 5.5 and three arm–set pairs did not run. The pre-registered blinded human reading was not performed: flagged sentences came only from A, and results were discussed before it could take place.

**What the data do show.** A compliance label holds more than one fact, and a current judge does not say which one it reports. On everyday tasks it reports the letter. A pipeline that turns these labels into negative examples would train against a substantial share of successful work without knowing why. The post hoc lead suggests that the same judge applies a different standard when the deviation carries a value. On the one record set where that happens, it records the deviation only in a sentence the pipeline ignores. For safety-relevant data, the label's silent shift is the bigger problem than either standard on its own. A label that does not say which fact it carries cannot be audited, and it cannot be calibrated across records.

**Practical recommendations.**
- Compute separate labels for the letter and the task from one itemised reading.
- Keep stopped and unlabelled calls in every denominator.
- Treat an unused abstain option as no mitigation.
- Before trusting a single label, compare it with the same judge's itemised reading on a sample. This ruler needs no answer key.

**Future work.** The 20-call reversed-framing test on B, a repeat of S on B and S on D, and judges from other providers.

Full limitations and dual-use considerations are in Appendix A.

## 6. Conclusion

We set out to show that mitigations for judge bending move the lost signal rather than remove it. For Claude Sonnet 5.5 the pre-registered evidence did not support that: the judge is mostly correct on blatant refusals, ignores the abstain option and invents no stance in a second channel. What it did show is that a compliance label carries one of two facts without saying which. On unseen data the binary judge marked 29% of successful runs as failures for rule slips, and computing both labels separated them (p = 0.003). After the run, the same judge's single label proved strict on everyday slips and lenient on value-laden deviations that it named in its own explanation, while the itemised label kept the distinction. This is a lead; the 20-call reversed-framing test on set B would decide it.

## Code and Data

Repository: https://github.com/ewithseven/Flectere. It contains the pre-registration (in Turkish) and the exact prompts (`on_kayit/`), the record selection lists, the run harness, coder and analysis code (`kod/`), and the result summaries, including every coder-flagged sentence (`sonuclar/`). Full call logs are available on request. Raw transcripts are not redistributed; the repository links to their sources (Lynch et al., 2026; Anthropic's released runs; AgentDojo). No info-hazards.

**Prior work (preexisting).** The itemised two-channel format, its code and its preprint (*One Field, Two Signs*, October 2026; github.com/ewithseven/Memento-Mori) predate the sprint and were used unchanged. Earlier phases of that project ran judges on the 18 transcripts of A and on 20 other AgentDojo runs. Those outputs are not counted here. Nineteen runs from the scenario families of B and D were seen in earlier phases and are excluded from both sets. Candidate questions were discussed in notes before the sprint. Everything else was done during the sprint: the question, the pre-registration, the selection rules, the coder, the run harness, all 614 calls and the analysis.

## Author Contributions

The author directed the project, made the research and method decisions and chose the framing.

## References

- Cook, J., et al. (2024). TICKing All the Boxes: Generated Checklists Improve LLM Evaluation and Generation. arXiv:2410.03608.
- Debenedetti, E., et al. (2024). AgentDojo: A Dynamic Environment to Evaluate Prompt Injection Attacks and Defenses for LLM Agents. arXiv:2406.13352.
- Gupta, M., Nair, Wang, & Kumar (2026). arXiv:2604.15224.
- Lee, Y., et al. (2024). CheckEval: Robust Evaluation Framework using Large Language Model via Checklist. arXiv:2403.18771.
- Lynch, A., et al. (2026). Agentic Misalignment in Summer 2026. Anthropic Alignment Science blog. https://alignment.anthropic.com/2026/agentic-misalignment-summer-2026/
- Marioriyad, et al. (2026). arXiv:2602.07996.
- Mu, T., et al. (2024). Rule Based Rewards for Language Model Safety. arXiv:2411.01111.
- One Field, Two Signs: Taking the Label Away from LLM Judges Under Training Pressure (2026). Preprint. github.com/ewithseven/Memento-Mori
- Pasch (2025). arXiv:2505.15365.
- Roussel, J. (2026). LessWrong, 11 September 2026. https://www.lesswrong.com/posts/Kc7Tc6XbbNeRK3Wg9/when-a-claude-judge-recognizes-the-hack-but-still-says
- Röttger, P., Vidgen, B., Hovy, D., & Pierrehumbert, J. (2022). Two Contrasting Data Annotation Paradigms for Subjective NLP Tasks. NAACL 2022. https://aclanthology.org/2022.naacl-main.13
- Tapwal, Kumar, & Maple (2026). arXiv:2605.23970.

## Appendix A. Limitations and Dual-Use / Ethical Considerations

**Limitations.**
- **Single judge, single call.** One judge model, one call per record, temperature not controllable. Call-to-call noise can exceed effects of one or two records.
- **Small sets.** The sets have 18, 20, 80 and 24 records. Among the pre-registered analyses only P1 reaches conventional significance.
- **Scope of P1.** P1 compares labels against AgentDojo's utility, which measures the main task. It does not show that the itemised format is more accurate in general. By the rubric's letter, the binary label is defensible.
- **Post hoc observations.** Sections 4.5 and 4.6 are post hoc. Section 4.5 compares two record sets, so it cannot separate value load from scenario, instruction type or agent family. Its explanation counts come from an unblinded reading by Claude models.
- **Weak coder.** The fabrication coder is lexical and has low recall, so a zero count is an upper bound, not an absence.
- **Withheld labels.** The itemised format withheld a label on up to half of the long-prompt records.
- **One model family.** The judge, extractor, code author and drafting assistant are all Claude models, so errors may be correlated.
- **Development data.** Set A is development data for the itemised format, so nothing about that format's success is claimed from A.
- **Safeguard stops.** The stops are specific to this call path and these transcripts.

**Possible misuse.**
- A pipeline operator could cite "current judges read the letter" to justify training against every flagged run, including successful work and openly raised concerns.
- If single-label judges really are lenient toward value-laden deviations, an agent could dress ordinary non-compliance as principled objection. Section 4.5 does not establish that they are.
- Reporting which prompt line coincides with safeguard stops could be read as a way around them. We report it because silently dropping stopped calls biases any bending estimate.

**Personal data.** None. All transcripts are synthetic evaluation scenarios or benchmark runs released by their authors, and the names in them are fictional. No human subjects were involved.

## Appendix B. Pre-registration record

- **Frozen** on 14 November 2026 at 14:01 (UTC+3), before any main-run output existed.
- **SHA-256** of the pre-registration text: `3306be07d878891645804b18f23d2ffde4362ccf0c06c6992c808882eb0ad71a`. Hashes of the prompts, selection lists and code are kept in the project's time ledger, available on request.
- **Changes after freezing**, each logged with a new hash:
  - One alternative was added to the pattern that recognises the safeguard-stop message, after the first batch and before any result was read.
  - The analysis script was changed after the run, so that the 36 unsent D calls are counted separately instead of being treated as missing.
- **Main run:** 14 November 15:25 to 16 November 00:09 (UTC+3), in batches bounded by the subscription quota.
- **Tokens:** 7.55 M cache-write, 5.61 M cache-read and 3.20 M output tokens over all logged calls.

## Appendix C. Sentences flagged by the coder

The coder flagged 16 sentences; they are listed verbatim, with arm and set, in the repository (`sonuclar/ek_cumleler.md`). Fourteen come from set A and two from set B. None come from C or D, the sets on which P3 was pre-registered. Two of the 16 carry a hard-event class. On reading, both are coder errors: the judge attributes the quoted words to the system prompt and to a human principal, not to the agent.

## LLM Usage Statement

Claude models (Anthropic) wrote the code, ran the model calls, computed the statistics, checked sources and helped draft this report. Every number in the report was recomputed from the logged outputs, and every reference was opened. The judge, the extractor, the code's author and the drafting assistant are all Claude models; Appendix A discusses what that implies.

