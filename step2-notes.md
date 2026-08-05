# Step-2 result — the pipeline runs, and the LLM-grader fallback does NOT yield a valid κ

disclosed LLM-grader fallback. The honest outcome is a **negative about the
method**, which is more useful than the number.

## What ran

- My pilot labels for Bandit's 31 FN issues, sealed as `grader_key_mine.json`.
- An independent LLM grader (fresh general-purpose agent, Sonnet) re-classified the
  **raw** issue bodies under the sealed rubric + boundary rule, blind to my labels.
- Cohen's κ computed: `grader_key_mine` vs the agent.

## The number, and why it is not what it looks like

```
n=31  agreement=31/31  po=1.000  pe=0.559  Cohen's κ = 1.000
```

**κ = 1.0 is real arithmetic and a near-worthless reliability estimate.** Three
reasons, each of which I would flag in someone else's paper:

1. **Same-brain graders.** The "independent" grader is an LLM of the *same model
   family* as the one doing my classification. Two raters that share weights and
   priors converge by construction; κ between them measures how deterministic the
   rubric is for one model, **not** whether the taxonomy carves reality. This is
   the design's fallback **option 2**, and step-2's real finding is that **option
   2 cannot produce a valid κ** — you cannot measure inter-rater reliability with
   raters that share a brain.
2. **Easy-dominated data.** Most of the 31 issues state their own root cause in the
   reporter's words ("only checks extractall, misses extract"; "no plugin exists
   for SSRF"). Perfect agreement on issues whose text hands you the label says
   little about the hard cases.
3. **The hard cases agreed by shared *rule*, not shared *truth*.** The boundary
   cases the pilot flagged with † (639/605/551 Python-3.8 AST; 119 crash; 88
   no-plugins) all agreed — but both raters applied the *same pre-registered
   boundary rule* ("AST mismatch → GRADING unless never dispatched"). Agreement
   there confirms the rule is deterministic, not that a human would call them the
   same way. A human grader is exactly where 639/551/119 could move to EXCLUSION.

## The near-miss (session discipline, recorded)

The **first** grader run returned κ=1.0 too — but that run was **contaminated**: I
had paraphrased each issue into interpretation-laden text ("a check exists but
misses X") in the prompt, so the grader graded *my summaries*, not the issues. I
caught it, threw it out, and re-ran with raw reporter bodies. Both the paraphrase
inflation and the same-model correlation are the same failure the parent project
is about — a measurement whose instrument cannot produce a counterexample. The raw
re-run removes the first; **nothing available to a solo run removes the second.**

## What step-2 actually establishes

- **Pipeline operable:** classify → independent re-grade → κ all ran end-to-end. ✓
- **The recruitment blocker is real, not a formality.** The design named a human
  (or cross-model) grader as load-bearing and offered an LLM fallback to de-risk;
  step-2 shows the LLM fallback **does not de-risk the reliability question** — it
  produces a confident number that means nothing. So the full study genuinely
  needs independent raters; it cannot be shortcut. That tightens the design.
- **Phase A⊥B concordance for Bandit is NOT cleanly testable.** I already know
  Bandit is grading-dominant (the pilot), so any discipline rating I produce now is
  contaminated. A clean Phase-A-before-Phase-B test requires a **fresh tool** whose
  defects I have not seen — that is the next real step, not Bandit.

## Revised design deltas (fold into STUDY_DESIGN.md)

- **Drop LLM-graders as a κ source.** They may pre-label to reduce human load, but
  the reliability κ must come from ≥2 *independent* raters — humans, or at minimum
  two *different model families* (and even then, treat cross-model κ as a weak
  proxy and say so).
- **The two-tool step-2 must use a tool not yet classified**, with Phase A sealed
  before Phase B, to test the concordance claim without the Bandit contamination.
- Cross-model grader option: a different-family model (e.g. via a peer bridge)
  would be less correlated — but the workspace's peer-bridge contract forbids
  treating peer output as evidence, so it is not used here; noted as an option that
  needs an explicit ruling before it could serve as a grader.

## One-line verdict

Step-2 did its job by **failing usefully**: it shows the study's independent-grader
requirement is load-bearing and un-shortcuttable, and it caught two ways I nearly
reported an inflated reliability. The pipeline is ready; the missing input is a
rater that does not share my brain.
