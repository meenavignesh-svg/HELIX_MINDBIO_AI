#!/usr/bin/env python3
"""Rewrite generated demos into a simple desktop-first dashboard layout."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DOCS = ROOT / "docs"


def generated_path(log_file: Path) -> str:
    for line in reversed(log_file.read_text(encoding="utf-8").splitlines()):
        if line.startswith("Created "):
            value = line.removeprefix("Created ").strip()
            if value.startswith("ai-chatbots/"):
                return value
    raise SystemExit("No generated product path found.")


def esc(value: str) -> str:
    return value.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def slug_short(title: str) -> str:
    words = re.findall(r"[A-Za-z0-9]+", title)
    return " ".join(words[:2]) or title


def html(meta: dict, sample: str) -> str:
    title = esc(meta["title"])
    category = esc(meta.get("category", "AI"))
    price = esc(meta.get("price_anchor", "$1000+ product"))
    short = esc(slug_short(meta["title"]))
    sample_json = json.dumps(sample)
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  <link rel="stylesheet" href="style.css">
</head>
<body data-product="premium-ai-chatbot">
  <main class="workspace">
    <nav class="topbar"><div><strong>{short}</strong><span>{category} product workspace</span></div><button id="sample" type="button">Load sample</button></nav>
    <section class="hero"><p>Premium workflow</p><h1>{title}</h1><span>{price}</span></section>
    <section class="metrics" aria-label="Product metrics"><article><strong id="score">94</strong><span>quality score</span></article><article><strong>5</strong><span>workflow modules</span></article><article><strong>$1k+</strong><span>price anchor</span></article></section>
    <section class="panel insights">
      <header class="brief"><p>Decision studio</p><h2>Paste real user input, score the situation, review risks, and produce a clear action plan.</h2></header>
      <div class="chips" aria-label="Workflow shortcuts"><button class="chip" type="button">structured intake</button><button class="chip" type="button">quality scoring</button><button class="chip" type="button">risk review</button><button class="chip" type="button">executive summary</button><button class="chip" type="button">export-ready action plan</button></div>
      <section class="workbench"><label class="input-card"><span>Input</span><textarea id="input" rows="10"></textarea></label><article class="output-card"><span>Decision report</span><div id="output"></div></article></section>
      <footer class="control-row"><input id="apiKey" type="password" placeholder="Optional OpenAI API key"><button id="analyze" type="button">Analyze</button></footer>
    </section>
  </main>
  <script>window.sampleData = {sample_json};</script>
  <script src="script.js"></script>
</body>
</html>"""


def css() -> str:
    return """:root{color-scheme:light;font-family:Inter,ui-sans-serif,system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;--accent:#4f46e5;--accent-2:#65a30d;--ink:#111827;--muted:#64748b;--line:#d9e2ec;--paper:#fff;--soft:#f5f7fb}*{box-sizing:border-box}html{background:var(--soft)}body{margin:0;min-height:100vh;color:var(--ink);background:#f5f7fb}.workspace{width:min(1280px,calc(100% - 32px));margin:0 auto;padding:20px 0 28px;display:grid;gap:16px}.topbar{min-height:58px;display:flex;align-items:center;justify-content:space-between;gap:16px;padding:12px 14px;border:1px solid var(--line);border-radius:12px;background:var(--paper);box-shadow:0 8px 28px rgba(15,23,42,.06)}.topbar div{display:grid;gap:2px}.topbar span{color:var(--muted);font-weight:700;font-size:.9rem}.hero{display:grid;grid-template-columns:minmax(0,1fr) auto;align-items:end;gap:20px;padding:24px;border-radius:14px;background:linear-gradient(135deg,#111827,#1f2937);box-shadow:0 14px 42px rgba(15,23,42,.14)}p{color:#a5b4fc;margin:0 0 8px;text-transform:uppercase;font-weight:900;font-size:.72rem;letter-spacing:.08em}h1{margin:0;color:#fff;font-size:clamp(2rem,4vw,3.6rem);line-height:.98;letter-spacing:0}h2{margin:0;max-width:920px;font-size:clamp(1.15rem,1.8vw,1.65rem);line-height:1.18;color:var(--ink);letter-spacing:0}.hero span{align-self:center;white-space:nowrap;border:1px solid rgba(255,255,255,.26);border-radius:999px;padding:9px 13px;background:rgba(255,255,255,.08);color:#fff;font-weight:800}.metrics{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:14px}.metrics article{min-width:0;padding:16px;border:1px solid var(--line);border-radius:12px;background:var(--paper);display:grid;gap:6px;box-shadow:0 8px 24px rgba(15,23,42,.05)}.metrics strong{color:var(--accent);font-size:2rem;line-height:1}.metrics span,.input-card span,.output-card span{color:var(--muted);font-weight:900;text-transform:uppercase;font-size:.7rem;letter-spacing:.06em}.panel{min-width:0;display:grid;gap:14px;padding:18px;border:1px solid var(--line);border-radius:14px;background:var(--paper);box-shadow:0 12px 35px rgba(15,23,42,.08)}.brief{padding:16px;border:1px solid var(--line);border-radius:10px;background:#f8fafc}.chips{display:flex;flex-wrap:wrap;gap:8px;align-items:center}.chip{border:1px solid var(--line);border-radius:999px;padding:8px 11px;background:#fff;color:var(--ink);cursor:pointer;font:inherit;font-weight:800}.workbench{min-height:420px;display:grid;grid-template-columns:1fr 1fr;gap:14px;align-items:stretch}.input-card,.output-card{min-width:0;min-height:0;display:grid;grid-template-rows:auto 1fr;gap:8px}textarea,input{width:100%;border:1px solid var(--line);border-radius:10px;padding:13px;font:inherit;background:#fff;color:var(--ink);outline:none}textarea{min-height:360px;height:100%;resize:vertical;line-height:1.5}textarea:focus,input:focus{border-color:var(--accent);box-shadow:0 0 0 4px rgba(79,70,229,.14)}.control-row{display:grid;grid-template-columns:minmax(0,1fr) 180px;gap:10px;align-items:center}button{border:0;border-radius:10px;min-height:44px;padding:0 16px;font:inherit;font-weight:900;background:var(--accent);color:#fff;cursor:pointer}.topbar button{min-height:38px;background:#111827}#analyze{background:var(--accent-2);color:#182306}#output{min-height:360px;height:100%;overflow:auto;white-space:pre-wrap;line-height:1.55;padding:14px;border:1px solid #1f2937;border-radius:10px;background:#101828;color:#e5edf6}@media(max-width:900px){.workspace{width:min(100% - 24px,1280px)}.hero,.metrics,.workbench,.control-row{grid-template-columns:1fr}.hero span{justify-self:start;white-space:normal}}"""


def main() -> None:
    log = ROOT / (sys.argv[1] if len(sys.argv) > 1 else "generated-product.txt")
    project = ROOT / generated_path(log)
    meta = json.loads((project / "project.json").read_text(encoding="utf-8"))
    sample = json.loads((project / "sample-data.json").read_text(encoding="utf-8")).get("sample_input", "")
    page = html(meta, sample)
    style = css()
    for base in [project / "public", DOCS / project.name]:
        base.mkdir(parents=True, exist_ok=True)
        (base / "index.html").write_text(page + "\n", encoding="utf-8")
        (base / "style.css").write_text(style + "\n", encoding="utf-8")
    print(f"Polished desktop demo: {project.relative_to(ROOT).as_posix()}")


if __name__ == "__main__":
    main()
