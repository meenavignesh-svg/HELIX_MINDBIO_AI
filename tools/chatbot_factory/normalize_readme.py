#!/usr/bin/env python3
"""Keep generated chatbot rows inside the README catalog table."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
README = ROOT / "README.md"

text = README.read_text(encoding="utf-8")
lines = text.splitlines()
row_re = re.compile(r"^\|\s*\d+\s*\|")
rows = []
clean = []
for line in lines:
    if row_re.match(line):
        if line not in rows:
            rows.append(line)
        continue
    clean.append(line)

insert_at = None
for index, line in enumerate(clean):
    if line.startswith("| ---:") and "Deployment" in clean[index - 1 if index else 0]:
        insert_at = index + 1
        break

if insert_at is None:
    README.write_text("\n".join(clean).rstrip() + "\n", encoding="utf-8")
    raise SystemExit(0)

renumbered = []
for number, row in enumerate(rows, start=1):
    parts = row.split("|")
    if len(parts) > 2:
        parts[1] = f" {number} "
    renumbered.append("|".join(parts))

clean[insert_at:insert_at] = renumbered
README.write_text("\n".join(clean).rstrip() + "\n", encoding="utf-8")
