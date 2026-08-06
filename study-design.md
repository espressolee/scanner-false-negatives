# Study design — where do a scanner's false-negative defects concentrate?

(`data/bandit-classification.md`), which killed the naive "exclusion-dominant (7/4/2)" claim and
replaced it with a testable successor. This is the protocol for the multi-tool,
multi-grader study. Nothing here is run yet.

---

## 1. Question and hypotheses

**RQ:** Across static analyzers of differing architecture, does the *plurality* of
their false-negative defects fall in the layer that was built with the **least
review discipline** — rather than in a fixed layer?

- **H1 (successor hypothesis):** the defect-plurality layer = the
  least-disciplined layer, as rated **independently and in advance**.
- **H0 (null):** defect-plurality is independent of the discipline rating — e.g.,
  it is always *grading* (matching breadth) regardless of architecture, or it is
  random with respect to the rating.
- **H2 (rival worth stating):** defect-plurality is determined by *architecture
  class alone* (hand-built→exclusion, plugin→grading, dataflow→?) and "discipline"
  adds nothing over architecture. H1 vs H2 is the interesting contest.

## 2. The circularity threat — the crux of the whole design

H1 is vacuous if "least-disciplined layer" is read off the defect distribution
(then it is true by definition). **The discipline rating must be produced before,
and independently of, any defect classification, by different people or at least
in a sealed prior phase.** Concretely:

- **Phase A (discipline rating), sealed before Phase B.** For each tool, rate each
  of its three layers (exclusion / grading / pattern-list) on a pre-specified
  discipline rubric that never mentions defects:
  - **R1 named-and-reviewed:** is the layer a named, documented API/ruleset (high)
    or ad-hoc literals/inline conditions (low)?
  - **R2 test coverage:** measured line/branch coverage of that layer's code.
  - **R3 change-review density:** PRs/reviews per KLoC touching that layer (from
    git history), a proxy for how much human attention it gets.
  - **R4 surface:** user-configurable + documented (high) vs internal-only (low).
  Composite discipline score per layer, frozen. **Whoever rates discipline does
  not classify defects, and vice versa.**
- **Phase B (defect classification):** classify each tool's FN issues into the
  three layers, blind to the Phase-A scores.
- H1 is confirmed only if the Phase-B plurality lands on the Phase-A
  lowest-discipline layer, tool by tool, with the two phases produced
  independently.

If this separation is not maintained, the study is not worth running — it would
reproduce the exact self-deception the pilot's parent project is about.

## 3. Constructs and definitions

**Layers (refined from the pilot):**
- **PATTERN-LIST** — no check for the vulnerability class exists.
- **GRADING** — a check exists but fails to match this form (AST shape, name
  resolution, value form, severity/confidence filtering).
- **EXCLUSION** — the code was never analyzed (path/file exclude, suppression
  comment, un-visited node type, parse/crash abort, unloaded plugin).

**Boundary rule (the pilot's † problem, now pre-specified):** an
AST-node-type/version mismatch is **GRADING** if the node is visited but the
check's type test fails; **EXCLUSION** only if the visitor never dispatches on
that node. Graders must cite the tool's dispatch code to choose EXCLUSION;
absent that evidence, default GRADING. This forces the harder-to-abuse call.

**Discipline** — Phase-A composite (R1–R4), not a defect-derived quantity.

## 4. Tool sample (the independent variable is architecture × discipline)

Selection criteria, pre-registered: public issue tracker; ≥ 25 classifiable FN
issues reachable by the sampling frame; open-source so Phase-A can read the code.
Target 5–6 tools spanning strata:

| stratum | candidates |
|---|---|
| hand-built / ad-hoc | `ftborrow` (mine — **included as one datum, flagged for author bias**, not as anchor) |
| plugin / AST linter | Bandit (pilot in hand), semgrep, pylint |
| dataflow / taint | CodeQL, Infer, Pysa |
| pattern / regex secrets | gitleaks, detect-secrets |

At least one tool per stratum; my own tool never more than one datum and never
the tie-breaker.

## 5. Sampling frame (reproducible FN enumeration)

- Enumerate candidate FNs by: issue labels matching `/false.?negative|missed/i`
  **plus** a fixed text-query set (the pilot's eight phrases), deduped, PRs
  excluded.
- Inclusion: a report that the tool failed to flag insecure/target code it should
  have. Exclusion: false-positives, pure feature requests with no existing check
  *unless* the class is in scope (those are PATTERN-LIST), usage/CLI/doc bugs,
  self-scans.
- **N per tool:** aim 30 classified (UNCLEAR excluded); report the screen ratio.
  Pre-specify a stopping rule (first 30 classifiable in recency order — no
  cherry-picking, the pilot's rule).

## 6. Multi-grader protocol

- **≥ 2 independent graders per tool, blind to H1, to the Phase-A scores, and to
  each other's labels.** **Superseded for the two tools already run:** the
  Bandit-31 and semgrep-30 label sets, and semgrep's sealed Phase-A rating, are
  published in `data/`, so no grader recruited after 2026-08-06 can be blind to them.
  Those two corpora are therefore spent for inter-rater work — retracting the files
  would not restore blinding, and would trade a real disclosure for a fake one. A
  blinded arm must use a corpus whose labels are unpublished at recruitment time and
  released only after the grader returns theirs, with that ordering pre-registered.
  Note also that the existing labels were LLM-produced under the sealed rubric (see
  the README), so an added human arm measures human-vs-LLM agreement, not
  human-vs-human. Third grader (or consensus meeting, pre-specified)
  adjudicates disagreements.
- **Inter-rater reliability:** report Cohen's κ (2 graders) or Fleiss' κ (≥3) per
  tool and pooled. **If κ is low, that is itself the finding** — the taxonomy does
  not carve reality and the "which layer" question is ill-posed. Pre-register a κ
  floor (e.g., 0.6) below which conclusions about plurality are withheld.
- **Grader instructions** = §3 verbatim + the boundary rule + worked examples from
  a tool *not* in the sample.

**Feasibility (honest, for a solo undergrad):** true independent graders are the
scarce resource. Staged fallbacks, in order of preference:
1. Recruit 1–2 external graders (same channel as prior external-reviewer work);
   pay a bounded, outcome-independent fee. Best.
2. If unavailable: one human grader (me) + one **LLM grader** under the same
   sealed rubric, disclosed as such, with κ reported and every disagreement
   hand-adjudicated and published. Weaker, but honest and increasingly accepted
   when disclosed.
3. Minimum: solo grader + full public data + a call for re-grading (crowd κ after
   the fact). Weakest; state it as a limitation, not a result.
The design does not pretend option 3 is option 1.

## 7. Analysis plan (pre-registered)

- **Primary:** per tool, is the Phase-B plurality layer == the Phase-A
  lowest-discipline layer? Report the 5–6 tool concordance as a fraction; with
  small N this is descriptive + an exact binomial against chance (1/3 per layer).
- **Secondary (H1 vs H2):** does discipline predict plurality *beyond* architecture
  stratum? With 5–6 tools this cannot be a regression; report it as a structured
  comparison and label it exploratory.
- **Decision rules, set now:**
  - H1 supported: concordance ≥ 5/6 and κ ≥ floor.
  - H1 refuted / H0: plurality is a fixed layer regardless of discipline rating.
  - Inconclusive: κ below floor, or concordance ~ chance — report as "taxonomy or
    power insufficient," not as either hypothesis.

## 8. Threats to validity

- **Construct:** the three-layer taxonomy may not partition cleanly (the † AST
  cases). Mitigated by the boundary rule + κ; if κ fails, that is the reported
  result.
- **Internal / author bias:** my own tool is one flagged datum, never the
  tie-breaker; discipline and defect phases are separated and independently graded.
- **Selection:** issue-tracker FNs are the *reported* subset, not all FNs — biased
  toward classes users notice. Stated as a ceiling, symmetric across tools so it
  does not favor a hypothesis.
- **External:** 5–6 tools is not "static analyzers in general." Claims scoped to
  the strata sampled.
- **Circularity:** §2 is the whole defense; if the phase separation slips, the
  study is void, not merely weak.

## 9. Replication package (this is also the portfolio artifact)

Publish: the sampling scripts, the raw candidate lists per tool, both phases'
rubrics, every grader's labels, the κ computation, and the adjudication log. A
reader must be able to re-grade from the same issues. Open data is the point —
the claim's credibility is that someone hostile can redo it.

## 10. Staging and effort

1. **Pilot — DONE** (Bandit, solo, n=31): killed 7/4/2, produced H1.
2. **Two-tool, two-phase, two-grader** (Bandit + one dataflow tool, e.g. CodeQL):
   proves the Phase-A/Phase-B separation is operable and yields a κ. ~1–2 weeks.
3. **Full 5–6 tools:** only after step 2 shows κ ≥ floor and the separation holds.
   Weeks, gated on grader recruitment.

Do not skip step 2. A design that has never been run end-to-end on two tools has
not earned the full sweep — the same rule the pilot enforced one level down.

## 11. The single sentence this study would earn (if H1 survives)

> Across static analyzers of differing architecture, a tool's false-negative
> defects concentrate in whichever internal layer received the least review
> discipline — not in a fixed layer — measured by separating an independent
> discipline rating from a blind defect classification, with inter-rater
> agreement reported.

If H1 does not survive, the earned sentence is the negative, and it is still
publishable because the design could have shown either.
