# semgrep — sealed Phase-A prediction, then Phase-B classification (n=30)

## Phase A (sealed before any semgrep issue was read)

# Phase A — semgrep discipline rating (SEALED before Phase B)

semgrep's three layers on the discipline rubric **before looking at a single one
of its false-negative issues**, seal the prediction, then classify (Phase B) and
check concordance. I have not opened semgrep's issue tracker as of writing this.

**Basis (defect-blind):** semgrep architecture + official docs only —
`docs.semgrep.dev/writing-rules/testing-rules` and `.../ignoring-files-folders-code`,
fetched 2026-08-05. No FN issue was read.

## The three layers, mapped to semgrep

- **PATTERN-LIST** = the rule registry (the set of rules that exist).
- **GRADING** = the matching engine (semgrep-core: pattern/taint/metavariable
  matching — how a rule matches a given form).
- **EXCLUSION** = what is never analyzed: `.semgrepignore`, `nosemgrep`,
  `--exclude` (user-facing) **plus** silent automatic skips — files that fail to
  parse, unknown extensions, unsupported languages, >1 MB (automatic, no config).

## Rubric scores (R1 named/reviewed · R2 test coverage · R3 change-review · R4 surface)

| layer | R1 | R2 | R3 | R4 | composite |
|---|---|---|---|---|---|
| PATTERN-LIST (registry) | HIGH — named, documented, versioned rules | MODERATE — testing is **opt-in**, `--validate` checks config not coverage | HIGH — community rule PRs reviewed | HIGH — user-writable, documented | **HIGH** |
| GRADING (engine) | HIGH — named core | HIGH — core is heavily tested (though matching-breadth across languages is inherently incomplete) | HIGH — the product's heart, constantly touched | LOW — internal, not user-facing | **HIGH–MODERATE** |
| EXCLUSION | **MIXED→LOW** — user config named; **silent auto-skips unnamed** | **LOW** — parse-fail / unknown-extension skips are untested "out of scope" behaviors | **LOW** — silent-skip logic rarely revisited | MIXED — config high, **auto-skips automatic/uncontrolled** | **LOW (dragged by the silent sub-part)** |

## SEALED PREDICTION

**Least-disciplined layer = EXCLUSION**, specifically its silent automatic-skip
sub-part (parse failures, unknown extensions, unsupported languages). PATTERN-LIST
is the most disciplined (visible reviewed registry); GRADING sits between.

**H1 therefore predicts:** semgrep's false-negative **plurality = EXCLUSION.**

**My honest empirical expectation is the opposite** (stated now so it is on the
record before Phase B): from the Bandit pilot and mature-tool reasoning, I expect
Phase B to come out **GRADING-dominant** (a mature engine's FNs cluster in
"the rule/engine didn't match this form"). If that happens, **H1 is REFUTED for
semgrep** and the rival — "mature tools are grading-dominant regardless of which
layer is least-disciplined" (H2) — is supported. This is the discriminating case
the Bandit pilot could not provide, because for Bandit the least-disciplined layer
(grading) and the plurality (grading) coincided.

## What this step can and cannot establish

- CAN: demonstrate the Phase-A⊥Phase-B **separation is operable** on a fresh tool,
  and produce one **discriminating** concordance datum (Phase A says EXCLUSION,
  so a GRADING plurality would falsify H1 here — unlike Bandit).
- CANNOT: give a reliable κ — that still needs an independent grader (step-2's
  confirmed load-bearing blocker). This is one solo grader, so Phase B is a point
  estimate to be re-graded, not a sealed reliability.

**Seal marker:** written before any semgrep issue was opened. Phase B lives in a
separate file (`PHASE_B_SEMGREP.md`); if that file's git/mtime precedes this one,
the separation was violated and the result is void.


---

## Phase B (classification, after the seal)

# Phase B — semgrep FN classification, and H1 is REFUTED by the clean test

committed "least-disciplined = EXCLUSION" and predicted, via H1, an EXCLUSION
plurality — before any semgrep issue was opened). n=30 classified FNs from
`semgrep/semgrep`, one grader (me), κ deferred.

## Result

```
GRADING       26 / 30   (87%)   the engine fails to match a valid pattern to a form
EXCLUSION      3 / 30   (10%)   file not analyzed (parse failure / silent skip)
PATTERN-LIST   1 / 30   ( 3%)   no rule for the class
```

**Phase A (sealed) said the least-disciplined layer is EXCLUSION → H1 predicts an
EXCLUSION plurality. The plurality is GRADING, 87%. H1 is REFUTED for semgrep.**
And it is refuted *cleanly*, unlike Bandit: for Bandit the least-disciplined layer
(grading) and the plurality (grading) coincided, so Bandit could not distinguish
H1 from its rival. Semgrep separates them — Phase A pointed at EXCLUSION, the data
pointed at GRADING — so this is the discriminating datum, and it goes against H1.

## The classification (re-gradable)

**GRADING (26)** — a rule/engine exists but fails to match this form:
`11830` Rust arg reuse · `11826` docker-compose rule needs obsolete `version` ·
`11689` `pattern-inside` `...` selection · `11662` Java crypto rule metavariable ·
`11620` C/C++ match across goto · `11618` Java expr before closure · `11586` taint
through Python `**kwargs` · `11493` PHP `\unserialize` FQN · `11492` PHP taint via
`&$ref` · `11467` Rust shadowing taint · `11466/11463` Rust diesel-taint via refs/
reassignment · `11464` Rust taint via `match` · `11435` indirect inheritance ·
`11410` symbolic prop in try/except · `11408` Java case-sensitive algo names ·
`11333` Python `match` scrutinee refine · `11315` Rust `metavariable-type` alias ·
`11314` Rust tuple syntax · `11274` C# catch exception type · `11271` Rust sqlx
hardcoded-password taint · `11253` Rust hardcoded-auth via var · `11252` Kotlin
`Klass::class.java` · `11209` `metavariable-comparison` chained ORs · `11161` Rust
namespace+template · `11102` C# auto getters/setters.

**EXCLUSION (3)** — never analyzed: `11740` PHP `readonly` param PartialParsing ·
`11443` Python parse errors silently ignored · `11287` Python empty-string-before-
`match` parse error.

**PATTERN-LIST (1)** — no rule: `11825` `p/docker-compose` has no rule for
`user: root`.

Screened out (not detection FNs): false-positives `11823 11582 11571 11605 11264`,
perf/build/meta `11404 11279 11204 11074 11560`.

## What this refutes, and what survives

- **Naive 7/4/2 (exclusion-dominant): dead** — two mature tools (Bandit, semgrep)
  are both grading-dominant.
- **H1 (defects follow the least-disciplined layer): refuted here.** Semgrep's
  least-disciplined layer by the rubric is EXCLUSION (silent parse/extension
  skips), but its defects sit overwhelmingly in GRADING.
- **The reason is the sharper finding: defects track the *inherently hardest*
  layer, not the least-*disciplined* one.** Semgrep's grading layer is
  well-reviewed and well-tested (high discipline) yet holds 87% of FNs — because
  multi-language pattern/taint matching (Rust, PHP, Kotlin, C#, C/C++…) is a
  bottomless long tail. Discipline and inherent difficulty are different axes, and
  the semgrep data says defects follow **difficulty**.
- **Unifying all three tools:** each tool's defects concentrate in *its* hardest
  layer — a hand-built scanner's is its ad-hoc exclusion set-literals; a mature
  multi-language matcher's is its matching breadth. "Least-disciplined" was a proxy
  that happened to coincide with "hardest" for my tool and Bandit, and comes apart
  on semgrep.

## Honesty bounds

- **One solo grader, no κ.** The κ blocker (independent grader) is unresolved;
  this Phase B is a point estimate. A different grader could move the 3
  EXCLUSION/1 PATTERN-LIST calls, but not enough to make EXCLUSION the plurality —
  the refutation is robust to a few re-grades.
- **The Phase A rating is debatable, and that is the point.** A rater who called
  GRADING the least-disciplined layer (given its vast matching gaps) would make H1
  "supported" — which is exactly the circularity the Phase-A-before-Phase-B seal
  exists to expose. My Phase A committed to EXCLUSION in writing before Phase B, so
  the refutation is clean *for my rating*; whether EXCLUSION-least-disciplined is
  the right rating is what an independent Phase-A rater must check.
- **Selection:** FN issues reachable by the text search, screened to 30 in recency
  order — the reported subset, symmetric with the Bandit pilot.

## Step-2 verdict (folds into STUDY_DESIGN.md)

The clean Phase-A⊥Phase-B separation **ran on a fresh tool and produced a
discriminating result that killed the study's own successor hypothesis (H1).**
That is the strongest thing a pilot can do. The design's next hypothesis should be
the difficulty-locus version — *defects concentrate in the layer bearing the
tool's inherent complexity* — and the study must still recruit independent
Phase-A raters and Phase-B graders, because both the discipline rating and the
classification are, on this evidence, the load-bearing subjective steps.
