#!/usr/bin/env python3
"""Generate one fresh browser-demo chatbot and update repo indexes.

The idea engine creates new concepts from domain, role, and job parts, then
skips any slug already present in README.md. This keeps the automation moving
without needing paid model tokens for every idea.
"""

from __future__ import annotations

import hashlib
import json
import random
import re
import textwrap
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "ai-chatbots"

DOMAINS = [
    ("Healthcare", "care", "safe wellness, symptom notes, appointment preparation"),
    ("Biotech", "bio", "biotech terms, study notes, lab-summary thinking"),
    ("Education", "learn", "teaching, quiz practice, and step-by-step explanations"),
    ("Automation", "flow", "workflow planning, task breakdowns, and process checks"),
    ("Productivity", "focus", "prioritization, planning, and personal systems"),
    ("Medical Coding", "code", "coding terminology, claim review concepts, and practice prompts"),
    ("Local LLM", "local", "local model testing, prompt trials, and result notes"),
    ("RAG", "rag", "retrieval planning, source grounding, and answer checking"),
    ("Voice Agents", "voice", "call flows, repair prompts, and spoken interaction design"),
]

ROLES = [
    ("Navigator", "nav", "maps choices into a clear next step"),
    ("Coach", "coach", "gives practical encouragement and structured action"),
    ("Analyst", "analyst", "compares options and explains tradeoffs"),
    ("Tutor", "tutor", "teaches with hints before answers"),
    ("Planner", "planner", "turns messy goals into checklists"),
    ("Reviewer", "reviewer", "checks quality, risks, and missing details"),
    ("Builder", "builder", "creates simple drafts, templates, and plans"),
    ("Scribe", "scribe", "summarizes notes into clean records"),
]

JOBS = [
    ("Daily Brief", "brief", "create a compact daily briefing with risks, actions, and open questions"),
    ("Decision Helper", "decision", "help choose between options using simple criteria"),
    ("Practice Lab", "practice", "make practice prompts and give feedback"),
    ("Checklist Maker", "checklist", "build checklists that are easy to follow"),
    ("Explainer", "explain", "explain hard ideas in plain language"),
    ("Quality Check", "quality", "score an answer and suggest improvements"),
    ("Idea Sprint", "sprint", "generate several useful ideas and pick the strongest"),
    ("Troubleshooter", "fix", "diagnose a problem and propose safe fixes"),
]

PALETTES = [
    ("#38bdf8", "#14b8a6"), ("#2dd4bf", "#f472b6"), ("#facc15", "#60a5fa"),
    ("#a78bfa", "#34d399"), ("#fb7185", "#fbbf24"), ("#93c5fd", "#22c55e"),
    ("#c084fc", "#67e8f9"), ("#f97316", "#84cc16"), ("#e879f9", "#38bdf8"),
]


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(textwrap.dedent(content).strip() + "\n", encoding="utf-8")


def read(path: str) -> str:
    file = ROOT / path
    return file.read_text(encoding="utf-8") if file.exists() else ""


def slugify(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")


def used_slugs() -> set[str]:
    return set(re.findall(r"ai-chatbots/([a-z0-9-]+)-chatbot-", read("README.md")))


def next_number(text: str) -> int:
    nums = [int(n) for n in re.findall(r"^\|\s*(\d+)\s*\|", text, flags=re.MULTILINE)]
    return max(nums, default=0) + 1


def append_row(path: str, row: str) -> None:
    file = ROOT / path
    write(file, read(path).rstrip() + "\n" + row)


def all_ideas() -> list[dict[str, str]]:
    ideas = []
    for domain, domain_slug, domain_focus in DOMAINS:
        for role, role_slug, role_style in ROLES:
            for job, job_slug, job_focus in JOBS:
                slug = f"{domain_slug}-{role_slug}-{job_slug}"
                title = f"{domain} {role} {job}"
                focus = f"{domain_focus}; {job_focus}; {role_style}"
                digest = hashlib.sha1(slug.encode("utf-8")).hexdigest()
                accent, accent2 = PALETTES[int(digest[:2], 16) % len(PALETTES)]
                ideas.append({
                    "slug": slug,
                    "title": title,
                    "category": domain,
                    "focus": focus,
                    "accent": accent,
                    "accent2": accent2,
                })
    return ideas


def pick_theme() -> dict[str, str]:
    used = used_slugs()
    available = [idea for idea in all_ideas() if idea["slug"] not in used]
    if not available:
        raise SystemExit("No unused idea combinations left. Add more idea parts before running again.")
    random.seed(datetime.now(timezone.utc).isoformat())
    return random.choice(available)


def build() -> str:
    theme = pick_theme()
    slug = theme["slug"]
    title = theme["title"]
    category = theme["category"]
    focus = theme["focus"]
    accent = theme["accent"]
    accent2 = theme["accent2"]

    now = datetime.now(timezone.utc)
    stamp = now.strftime("%Y-%m-%d-%H%M%Sz")
    made = now.strftime("%Y-%m-%d %H:%M UTC")
    folder = OUT / f"{slug}-chatbot-{stamp}"
    project_path = folder.relative_to(ROOT).as_posix()

    system = f"You are {title}, a concise practical chatbot for {focus}. Keep replies safe, clear, specific, and useful."
    demo = f"Demo mode: I am {title}. I can help with {focus}. Ask one specific question and I will give a useful next step."

    write(folder / "README.md", f"""
    # {title}

    A browser-demo chatbot generated by automation pipeline.

    ## Browser Demo

    Open `public/index.html` in a browser. Demo mode works without setup.

    ## Optional Real AI Mode

    Deploy this folder to Vercel, then enter an OpenAI API key in the browser UI. The key stays in `sessionStorage`.

    ## Folder

    `{project_path}`
    """)

    write(folder / "package.json", json.dumps({
        "name": f"{slug}-chatbot",
        "version": "1.0.0",
        "type": "module",
        "scripts": {"dev": "vercel dev"},
        "dependencies": {"@vercel/node": "^3.2.27", "openai": "^5.0.0"},
        "devDependencies": {"vercel": "^34.3.0"},
        "engines": {"node": ">=18"}
    }, indent=2))

    write(folder / "vercel.json", '{\n  "version": 2,\n  "routes": [\n    { "src": "/api/chat", "dest": "/api/chat.js" },\n    { "src": "/(.*)", "dest": "/public/$1" }\n  ]\n}')

    write(folder / "api/chat.js", f"""
    import OpenAI from 'openai';

    export default async function handler(req, res) {{
      if (req.method !== 'POST') return res.status(405).json({{ error: 'Method not allowed.' }});
      const apiKey = req.headers.authorization?.replace(/^Bearer\s+/i, '') || req.body?.apiKey;
      if (!apiKey) return res.status(400).json({{ error: 'OpenAI API key required for real AI mode.' }});
      const messages = Array.isArray(req.body?.messages) ? req.body.messages.slice(-10) : [];
      const input = messages.map((m) => ({{ role: m.role === 'assistant' ? 'assistant' : 'user', content: String(m.content || '').slice(0, 2000) }}));
      const client = new OpenAI({{ apiKey }});
      const response = await client.responses.create({{ model: 'gpt-4.1-mini', instructions: {json.dumps(system)}, input }});
      return res.status(200).json({{ reply: response.output_text || 'Please try again.' }});
    }}
    """)

    write(folder / "public/index.html", f"""
    <!doctype html>
    <html lang="en">
    <head>
      <meta charset="utf-8">
      <meta name="viewport" content="width=device-width, initial-scale=1">
      <title>{title}</title>
      <link rel="stylesheet" href="style.css">
    </head>
    <body>
      <main class="shell">
        <section class="chat">
          <header><p>{category}</p><h1>{title}</h1><span id="status">demo ready</span></header>
          <form id="keyForm"><input id="apiKey" type="password" placeholder="Optional OpenAI API key"><button>Use Key</button></form>
          <div id="messages"></div>
          <form id="chatForm"><input id="text" placeholder="Ask this chatbot for help..."><button>Send</button></form>
        </section>
      </main>
      <script src="script.js"></script>
    </body>
    </html>
    """)

    write(folder / "public/style.css", f"""
    :root {{ color-scheme: dark; font-family: Inter, system-ui, sans-serif; background: #111318; color: #f8fafc; }}
    * {{ box-sizing: border-box; }}
    body {{ margin: 0; min-height: 100vh; background: radial-gradient(circle at 15% 15%, {accent}55, transparent 28rem), radial-gradient(circle at 85% 25%, {accent2}44, transparent 24rem), #111318; }}
    .shell {{ min-height: 100vh; display: grid; place-items: center; padding: 24px; }}
    .chat {{ width: min(760px, 100%); min-height: 680px; display: grid; grid-template-rows: auto auto 1fr auto; border: 1px solid #ffffff24; border-radius: 8px; overflow: hidden; background: #10151de6; }}
    header, form {{ display: grid; gap: 10px; padding: 18px 22px; border-bottom: 1px solid #ffffff1a; }}
    header {{ grid-template-columns: 1fr auto; align-items: center; }}
    header p {{ margin: 0 0 4px; color: {accent}; text-transform: uppercase; font-size: .75rem; letter-spacing: .08em; }}
    h1 {{ margin: 0; font-size: clamp(1.45rem, 4vw, 2.25rem); }}
    #status {{ border: 1px solid {accent}; color: {accent}; padding: 6px 10px; border-radius: 999px; font-size: .78rem; }}
    #messages {{ padding: 22px; display: flex; flex-direction: column; gap: 14px; overflow: auto; }}
    .msg {{ max-width: min(84%, 560px); padding: 12px 14px; border-radius: 8px; line-height: 1.5; white-space: pre-wrap; background: #202936; }}
    .user {{ align-self: flex-end; background: {accent}; color: #061014; }}
    form {{ grid-template-columns: 1fr auto; }}
    input, button {{ min-height: 46px; border: 0; border-radius: 8px; font: inherit; }}
    input {{ padding: 0 14px; }}
    button {{ padding: 0 18px; background: {accent2}; color: #07110c; font-weight: 700; }}
    @media (max-width: 560px) {{ .shell {{ padding: 0; }} .chat {{ min-height: 100vh; border: 0; border-radius: 0; }} form, header {{ grid-template-columns: 1fr; }} }}
    """)

    write(folder / "public/script.js", f"""
    const messages = document.querySelector('#messages');
    const text = document.querySelector('#text');
    const apiInput = document.querySelector('#apiKey');
    const statusEl = document.querySelector('#status');
    let apiKey = sessionStorage.getItem('openai_api_key') || '';
    const history = [];

    function add(content, role = 'bot') {{
      const node = document.createElement('div');
      node.className = `msg ${{role}}`;
      node.textContent = content;
      messages.appendChild(node);
      messages.scrollTop = messages.scrollHeight;
    }}

    document.querySelector('#keyForm').addEventListener('submit', (event) => {{
      event.preventDefault();
      apiKey = apiInput.value.trim();
      if (!apiKey) return;
      sessionStorage.setItem('openai_api_key', apiKey);
      apiInput.value = '';
      statusEl.textContent = 'real AI ready';
      add('API key saved for this browser session.');
    }});

    document.querySelector('#chatForm').addEventListener('submit', async (event) => {{
      event.preventDefault();
      const value = text.value.trim();
      if (!value) return;
      text.value = '';
      add(value, 'user');
      history.push({{ role: 'user', content: value }});
      if (!apiKey) {{
        const reply = {json.dumps(demo)};
        history.push({{ role: 'assistant', content: reply }});
        setTimeout(() => add(reply), 200);
        return;
      }}
      try {{
        const response = await fetch('/api/chat', {{ method: 'POST', headers: {{ 'Content-Type': 'application/json', Authorization: `Bearer ${{apiKey}}` }}, body: JSON.stringify({{ messages: history }}) }});
        const data = await response.json();
        const reply = data.reply || data.error || 'No reply received.';
        history.push({{ role: 'assistant', content: reply }});
        add(reply);
      }} catch {{
        add({json.dumps(demo)});
      }}
    }});

    add({json.dumps(demo)});
    """)

    number = next_number(read("README.md"))
    append_row("README.md", f"| {number} | {title} | {made} | {category} | `{project_path}` | Successful demo | Browser demo + Vercel/OpenAI-ready | Not deployed |")
    append_row("tracking/successful-projects.md", f"| {number} | {title} | {made} | `{project_path}` | Browser demo created. |")
    append_row("tracking/model-usage.md", f"| {number} | {title} | Browser rules | gpt-4.1-mini via visitor key | generated by automation pipeline idea engine |")
    append_row("tracking/deployment-links.md", f"| {number} | {title} | `{project_path}` | Pending | Not deployed |")
    return project_path


if __name__ == "__main__":
    print(f"Created {build()}")
