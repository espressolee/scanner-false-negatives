# Pilot pre-registration — does the exclusion-dominant defect split generalize?

Written 2026-08-05 **before looking at any specific Bandit issue.** Fixed here so
the classification cannot be fitted to a desired outcome.

## Question

My own borrow scanner's defects split `exclusion 7 / grading 4 / pattern-list 2`
(exclusion-dominant). Is that a property of scanners, or of *my hand-built* one?
Test on a mature, plugin-architecture scanner I did not build: **Bandit**
(`PyCQA/bandit`).

## Unit

A Bandit **false-negative** report: "Bandit did not flag insecure code X that it
should have." Excludes false-positives, feature requests, and usage questions.

## Classification (mutually exclusive, decided by root cause)

- **PATTERN-LIST** — Bandit has **no check/plugin** for vulnerability class X at
  all. The ruleset does not cover it. (≈ my BORROW_API missing a call.)
- **GRADING** — a check for X **exists but fails to match this form**: wrong AST
  shape, severity/confidence set so it is filtered, misclassification. (≈ my
  mis-grading a found site.)
- **EXCLUSION** — the code was **never analyzed**: path/file exclude, `# nosec`,
  an AST node type Bandit does not visit, a parse/encoding skip, vendored/generated
  skip. (≈ my SKIP_DIRS / suffixes.)
- **UNCLEAR** — not determinable from the issue, or misfiled (not actually a FN).

One label per issue. If two apply, pick the **root** cause (the earliest link in
the chain that, if fixed, would make Bandit flag it).

## Sampling

Neutral query on `PyCQA/bandit` issues for false-negative reports (title/body
"false negative", "not detected", "does not detect", "missed", "should flag"),
taken in the order returned, **no skipping**. Target: 30 classifiable (UNCLEAR
does not count toward 30; report how many were screened to reach 30).

## Decision rule (set before data)

- **Supports generality of 7/4/2**: EXCLUSION is the plurality (≥ ~45%).
- **Refutes it (my split is tool-specific)**: EXCLUSION is not the plurality —
  in particular if PATTERN-LIST dominates, that is the mature-tool signature and
  the honest conclusion is "the exclusion-dominance was an artifact of a hand-built
  tool."
- Either way the pilot decides go/no-go for a multi-tool study, and either way it
  is a real result.

## Anti-bias commitments

- Classify from the issue text, not from what would make 7/4/2 look right.
- Report the full 30 with one-line justifications so a reader can re-grade.
- n=30, one tool, one grader (me) — this is a **pilot**, not the study. It can
  only kill the hypothesis or license the larger, multi-grader study; it cannot
  confirm a general law.
