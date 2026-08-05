# Bandit false-negative classification (n=31)

One grader. Every issue + label + reason, published for re-grading.

## The classification (so a reader can re-grade)

**GRADING (22)** — a check exists but fails to match this form:
| # | one-line |
|---|---|
| 1465 | B501/B113 match `httpx.request` but only 7 `requests` verb helpers, not `requests.request` |
| 1405 | B704 misses local `Markup` subclasses |
| 1399 | detection of `cmdclass` is evadable by reshaping the call |
| 1397 | B508/B509 argument-shape check too narrow |
| 1395 | B104 misses `bind(("", port))` (only matches `"0.0.0.0"`) |
| 1394 | B501 misses `verify=False` on session/client instances |
| 1392 | B202 checks `extractall`, misses `extract` |
| 1390 | B103 only handles integer-literal mode, misses `stat.*` BinOp |
| 1383 | B105/6/7 rigid regex misses identifier forms |
| 1336 | B608 regex requires a space after `VALUES` |
| 1267 | B105 misses password as a dict value |
| 1171 | B202 misses `extractall` when qualified name unresolved |
| 977  | B608 misses `connections[...].cursor().execute(f"...")` |
| 916  | B608 misses f-string `FormattedValue` between select/from |
| 886  | B105 misses password inside a connection-string literal |
| 656  | B104/B608 matching regression in 1.6.2 |
| 639  | B105 misses password on Py≥3.8 (AST `Constant` vs `Str`) † |
| 605  | dup of 639/551 (B105, Py3.8) † |
| 551  | B105 not fired under Py3 (AST) † |
| 462  | B506 misses `from yaml import load; load()` (name resolution) |
| 313  | password check too lenient (misses dict/kw forms) |
| 157  | shell check matches `True`/`"True"`, misses `shell=1` |

**PATTERN-LIST (7)** — no check for the class exists:
| # | one-line |
|---|---|
| 1404 | no check for dynamic Jinja2 template-source execution |
| 1403 | no check for Flask `send_file` misuse |
| 1401 | no SSRF check |
| 1339 | no decompression-bomb check |
| 1071 | no check for `PKCS1v15` encryption |
| 1067 | no check for `Markup` on non-literal content |
| 121  | no PyCrypto check (at the time) |

**EXCLUSION (2)** — code never analyzed:
| # | one-line |
|---|---|
| 119 | internal crash on a node → file not analyzed |
| 88  | no plugins loaded after install → nothing scanned (install-level) |

Screened out as not detection-FNs (not counted): false-positives (1227, 1216,
996, 995, 994, 711, 596), reporting/CLI/util/doc bugs (459, 708, 318, 138, 1009,
1005, 1082), a self-scan (1389), and duplicates (52, 16 dup 88).

† **Boundary flag (honesty).** The four Py3.8-AST issues (639/605/551, and
arguably others) sit on the grading/exclusion line: is a node whose *type* the
matcher no longer recognizes a mis-grade (check fires on the wrong node type) or
an exclusion (the new node type is not visited)? I graded them GRADING because the
check exists and is intended to fire; a reviewer could move up to ~4 to EXCLUSION.
Even then exclusion is ≤ 6/31 (19%) — still not the plurality. The verdict does
not depend on these calls.

