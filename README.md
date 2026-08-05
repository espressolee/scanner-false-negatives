# Where do a static analyzer's false negatives hide?

### A pre-registered study that refuted its own hypothesis, twice — with all data public for re-grading.

I built a small static analyzer, noticed its bugs seemed to cluster in one place,
and turned that into a falsifiable claim. Then I designed the test so that it
could kill the claim rather than confirm it — and it did, twice. This repository
is the honest record: the pre-registration, the classifications, the two
refutations, and the limits. Every label is published so a stranger can re-grade
it and disagree.

**This is an exploratory study, not a peer-reviewed result** (two tools, one
grader, no inter-rater κ yet). The topic is not novel — the prior work is cited
below. What it demonstrates is method: pre-registration, a circularity defense,
falsifying my own hypothesis, and catching two of my own inflated measurements.

---

## The claim I started with

I wrote a scanner for one bug class (borrow-then-use in Python C extensions). Over
a day of building it, it was wrong 14 times, and the errors seemed to concentrate
in its **exclusion layer** — the ad-hoc set-literals that decide what *not* to
scan — rather than in the named rule list a reviewer would actually read. The
split was `exclusion 7 / grading 4 / pattern-list 2`.

That suggested a general hypothesis:

> **H0 (naive):** a scanner's defects concentrate in its exclusion layer.

## Test 1 — Bandit: the naive claim dies

I mined 31 false-negative reports from [Bandit](https://github.com/PyCQA/bandit)
(a mature, plugin-based Python security linter) and classified each by root cause:
**pattern-list** (no check exists), **grading** (a check exists but fails to match
this form), or **exclusion** (the code was never analyzed).

```
Bandit false-negatives:   grading 22 (71%)   pattern-list 7 (23%)   exclusion 2 (6%)
My hand-built scanner:    exclusion 7 (54%)  grading 4              pattern-list 2
```

**Inverted.** Exclusion, which dominated my tool, is the *rarest* cause in Bandit.
So exclusion-dominance was a property of my hand-built tool, not of scanners. The
naive claim is dead. → [`data/bandit-classification.md`](data/bandit-classification.md)

## The successor, and the trap

The data suggested a better hypothesis:

> **H1:** a scanner's defects concentrate in its **least-disciplined layer** —
> ad-hoc set-literals for my tool, matching-breadth for a mature one.

But H1 has a fatal trap: if "least-disciplined layer" is judged *after* seeing
where the defects are, it is true by definition. So the design (below) **seals a
discipline rating of each layer before any defect is classified**, by a rubric
that never mentions defects. Phase A (rate discipline) ⊥ Phase B (classify
defects). If the separation slips, the study is void.

## Test 2 — semgrep: the clean test kills H1 too

For [semgrep](https://github.com/semgrep/semgrep) (a different architecture — a
rule engine, not per-language plugins), I wrote and **sealed** the discipline
rating first ([`preregistration`](preregistration.md) + the sealed Phase A):
its least-disciplined layer is **exclusion** (silent skips of files that fail to
parse). H1 therefore predicts an **exclusion** plurality.

Then I classified 30 semgrep false-negatives:

```
semgrep false-negatives:   grading 26 (87%)   exclusion 3 (10%)   pattern-list 1 (3%)
Sealed Phase-A prediction (H1):  exclusion plurality
```

**H1 refuted, cleanly.** Bandit couldn't discriminate — its least-disciplined
layer (grading) happened to coincide with its plurality (grading). semgrep
separates them: Phase A pointed at exclusion, the data pointed at grading. →
[`data/semgrep-classification.md`](data/semgrep-classification.md)

## What survived

The layer that holds the defects is not the least-*disciplined* one — semgrep's
grading layer is well-reviewed and well-tested, yet holds 87% of the false
negatives, because multi-language pattern/taint matching is a bottomless long
tail. **Defects track the layer bearing the tool's inherent difficulty, not the
one with the least review.** Discipline and difficulty are different axes, and the
data followed difficulty. That is the hypothesis the [full study](study-design.md)
would test next — and it, too, is stated so it can fail.

## The honest limits (read these)

- **One grader (me), no κ.** I re-graded the Bandit set with a second LLM grader
  and got κ = 1.0 — which is *worthless*, because same-model graders share a brain
  and converge. A real reliability number needs independent human (or cross-model)
  graders. Details, and the two times I nearly reported an inflated κ, are in
  [`step2-notes.md`](step2-notes.md).
- **Phase-A ratings are subjective.** A rater who called *grading* the
  least-disciplined layer would make H1 "supported" by the very circularity the
  seal exists to expose. My rating is committed in writing before Phase B; whether
  it is the *right* rating is what an independent rater must check.
- **The pre-registration is not git-verifiable from this repository.** This repo
  is a single-commit export made *after* both phases were done. The files record
  that each Phase-A rating was written before its Phase-B classification — and that
  is true; the working files' timestamps bear it out — but from this repository's
  history alone you cannot prove the order, and file timestamps are not proof to a
  determined skeptic. Treat the pre-registration as a **stated protocol, not a
  timestamp-proven one**. If "pre-registered" is the headline, the ordering is
  load-bearing, and I would rather say plainly where the public proof stops than
  let the word carry more than the bytes support. That admission is the same
  discipline the study is about.
- **Not novel.** This is a small, honest replication in the space already studied
  by Thung et al. (false negatives, ASE 2014), Liargkovas–Panourgia–Spinellis
  (suppression as an auditable surface, arXiv 2311.07482), Groce et al.
  (differential mutation analysis of analyzers, QRS 2021), and Taneja–Liu–Regehr
  (soundness/precision bugs inside analyzers, CGO 2020). The contribution here is
  the pre-registered self-refutation, not a discovery.
- **The scanner itself is not released.** It finds a real bug class in packages
  nobody has contacted; a run-it-yourself release would be disclosure at scale.

## Re-grade it

Every issue and its assigned label is in `data/`. Disagree with a call, and the
plurality either survives or it doesn't — that is the point of publishing the
labels instead of the conclusion.

## Contents

- [`preregistration.md`](preregistration.md) — the sealed rubric and decision rule.
- [`data/bandit-classification.md`](data/bandit-classification.md) — 31 labels + reasons.
- [`data/semgrep-classification.md`](data/semgrep-classification.md) — 30 labels + reasons, with the Phase-A seal that preceded them.
- [`study-design.md`](study-design.md) — the multi-tool, multi-grader design, and its circularity defense.
- [`step2-notes.md`](step2-notes.md) — why the LLM-grader κ is worthless, and the two inflations I caught.
