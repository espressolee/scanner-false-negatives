#!/usr/bin/env python3
"""Regenerate the distribution tables from data/labels.csv.

The numbers in README.md are this script's output. If a label changes, re-run
this and paste the result -- do not hand-edit the tables. They were
hand-transcribed until 2026-08-07, which meant the repository invited strangers
to re-grade 61 labels while publishing figures nothing could recompute.

Standard library only, no arguments:  python3 analyze.py
"""
import collections
import csv
import pathlib

rows = list(csv.DictReader(pathlib.Path("data/labels.csv").open()))
by_tool = collections.defaultdict(collections.Counter)
for row in rows:
    by_tool[row["tool"]][row["category"]] += 1

for tool in sorted(by_tool):
    counts = by_tool[tool]
    total = sum(counts.values())
    print(f"\n{tool} false-negatives (n={total}):")
    for category, n in counts.most_common():
        print(f"  {category.lower():<14} {n:>3}  ({round(100 * n / total)}%)")

print(f"\ntotal labels: {len(rows)}")
seen = collections.Counter((r["tool"], r["issue"]) for r in rows)
duplicates = [key for key, n in seen.items() if n > 1]
if duplicates:
    print(f"WARNING duplicate (tool, issue) keys: {duplicates}")
