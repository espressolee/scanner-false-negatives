#!/usr/bin/env python3
"""One-time lift: the prose classification tables -> data/labels.csv.

After this runs, the CSV is the source of truth for counts and the Markdown
keeps the human-readable reasons. Re-running is harmless but pointless; if the
two ever disagree, the CSV wins and the Markdown is the stale copy.

It fails loudly rather than silently producing a smaller corpus: each section
header declares its own count, and this asserts the parse matches it. A
regex that quietly matched 21 of 22 rows would otherwise publish a corpus
that is not the one the study describes.
"""
import csv
import pathlib
import re
import sys

SOURCES = {
    "bandit": "data/bandit-classification.md",
    "semgrep": "data/semgrep-classification.md",
}
# The two files do not share a layout, and assuming they did is what the
# section-count assertion below caught on the first run: the bandit file uses
# Markdown table rows, the semgrep file uses inline `id` reason entries
# separated by a middle dot and wrapped across lines. Both are parsed.
#
# **GRADING (22)** — ...
CATEGORY = re.compile(r"^\*\*([A-Z][A-Z0-9 _-]*?)\s*\((\d+)\)\*\*")
# | 1465 | reason |
TABLE_ROW = re.compile(r"^\|\s*(\d+)\s*\|\s*(.*?)\s*\|\s*$")
# `11830` Rust arg reuse
# Located by POSITION, not by splitting: an entry is not always at the start of
# a chunk ("**PATTERN-LIST (1)** — no rule: `11825` ..."), and reasons contain
# backticks of their own (`p/docker-compose`, `version`). Requiring the whole
# backtick span to be digits also excludes the screened-out list, which is one
# span holding several ids (`11823 11582 ...`).
# One span can carry several ids sharing a reason (`11466/11463` Rust
# diesel-taint via refs/reassignment). Matching only single-id spans dropped
# exactly those two, which is how GRADING parsed 24 of 26.
INLINE_ID = re.compile(r"`(\d+(?:/\d+)*)`")

rows: list[dict[str, str]] = []
declared: dict[tuple[str, str], int] = {}


def flush_inline(tool: str, category: str, buffer: list[str]) -> None:
    text = " ".join(part.strip() for part in buffer).strip()
    if not text:
        return
    found = list(INLINE_ID.finditer(text))
    for index, match in enumerate(found):
        end = found[index + 1].start() if index + 1 < len(found) else len(text)
        reason = " ".join(text[match.end():end].split()).strip(" ·.").strip()
        for issue in match.group(1).split("/"):
            rows.append(
                {
                    "tool": tool,
                    "issue": issue,
                    "category": category,
                    "reason": reason,
                }
            )


for tool, path in SOURCES.items():
    category = None
    inline: list[str] = []
    for line in pathlib.Path(path).read_text().splitlines():
        match = CATEGORY.match(line)
        if match:
            if category:
                flush_inline(tool, category, inline)
            category = match.group(1).strip()
            declared[(tool, category)] = int(match.group(2))
            # The first entry can begin on the header line itself
            # ("**PATTERN-LIST (1)** — no rule: `11825` ..."), so the tail of
            # this line is content, not decoration. Dropping it is what made
            # PATTERN-LIST parse 0 of 1 and EXCLUSION 2 of 3.
            inline = [line[match.end():]]
            continue
        # A section's entries are one paragraph. Stop at the blank line after
        # it: the prose that follows ("Screened out (not detection FNs):
        # false-positives `11823 ...`") holds ids that are NOT labels, and
        # letting it run on appends them to the last entry's reason.
        if category and (not line.strip() or line.startswith("#")):
            flush_inline(tool, category, inline)
            inline = []
            category = None
            continue
        match = TABLE_ROW.match(line)
        if match and category:
            rows.append(
                {
                    "tool": tool,
                    "issue": match.group(1),
                    "category": category,
                    "reason": match.group(2),
                }
            )
        elif category and line.strip():
            inline.append(line)
    if category:
        flush_inline(tool, category, inline)

problems = []
for (tool, category), count in sorted(declared.items()):
    parsed = sum(1 for r in rows if r["tool"] == tool and r["category"] == category)
    if parsed != count:
        problems.append(f"  {tool}/{category}: header says {count}, parsed {parsed}")
if problems:
    sys.exit("section counts do not match the headers:\n" + "\n".join(problems))
if len(rows) != 61:
    sys.exit(f"expected 61 labels in total, parsed {len(rows)}")

out = pathlib.Path("data/labels.csv")
with out.open("w", newline="") as handle:
    # lineterminator="\n": csv defaults to CRLF (RFC 4180), git commits LF,
    # so the file would read as modified every time it is regenerated and
    # the regenerate-then-diff check would be pure noise.
    writer = csv.DictWriter(
        handle, ["tool", "issue", "category", "reason"], lineterminator="\n"
    )
    writer.writeheader()
    writer.writerows(rows)
print(f"wrote {out}: {len(rows)} labels across {len(declared)} sections")
