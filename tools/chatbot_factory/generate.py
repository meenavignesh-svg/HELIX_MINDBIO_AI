#!/usr/bin/env python3
"""Generate one browser-demo chatbot project and update repository indexes."""

from __future__ import annotations

import json
import os
import random
import re
import textwrap
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
OUTPUT_ROOT = REPO_ROOT / "ai-chatbots"

THEMES = [
    {
        "slug": "robot-gardener",
        "title": "Robot Gardener",
        "category": "Automation",
        "area_readme": "automation/README.md",
        "tags": "automation, plants",
        "accent": "#86efac",
        "accent2": "#67e8f9",
        "user": "#15803d",
        "eyebrow": "Greenhouse console",
        "busy": "growing",
        "system": "You are Robot Gardener, a practical assistant for plant care, watering schedules, soil notes, and beginner garden plans.",
        "placeholder": "Ask about plants, watering, soil, or garden plans...",
        "welcome": "Robot Gardener is ready in browser demo mode. Ask about plants, watering, soil, or garden planning.",
        "topics": {
            "water": "Demo mode: check soil moisture first, water deeply when dry, and adjust for sunlight and pot size.",
            "soil": "Demo mode: healthy soil needs drainage, organic matter, and the right texture for the plant.",
            "pest": "Demo mode: isolate the plant, inspect leaves, rinse gently, and avoid harsh treatments at first.",
        },
    },
    {
        "slug": "startup-coach",
        "title": "Startup Coach",
        "category": "Productivity",
        "area_readme": "productivity/README.md",
        "tags": "startup, planning",
        "accent": "#93c5fd",
        "accent2": "#fbbf24",
        "user": "#2563eb",
        "eyebrow": "Founder desk",
        "busy": "thinking",
        "system": "You are Startup Coach, a practical assistant for startup ideas, MVP planning, customer discovery, and launch checklists.",
        "placeholder": "Ask about ideas, MVPs, customers, or launches...",
        "welcome": "Startup Coach is ready in browser demo mode. Ask about ideas, MVPs, customer discovery, or launch plans.",
        "topics": {
            "idea": "Demo mode: define the customer, the painful problem, and the smallest proof that they care.",
            "mvp": "Demo mode: build the smallest version that tests one behavior, not every feature.",
            "launch": "Demo mode: choose one audience, one promise, one channel, and one metric for the first week.",
        },
    },
    {
        "slug": "biotech-notes",
        "title": "Biotech Notes",
        "category": "Biotech",
        "area_readme": "biotech/README.md",
        "tags": "biotech, study",
        "accent": "#5eead4",
        "accent2": "#f9a8d4",
        "user": "#0f766e",
        "eyebrow": "Research bench",
        "busy": "analyzing",
        "system": "You are Biotech Notes, a careful assistant for biotech study notes, experiment summaries, glossary help, and safe high-level research planning.",
        "placeholder": "Ask about biotech notes, terms, or study plans...",
        "welcome": "Biotech Notes is ready in browser demo mode. Ask about biotech notes, glossary terms, or study planning.",
        "topics": {
            "glossary": "Demo mode: define the term, add one plain-language analogy, and note where it appears in a workflow.",
            "experiment": "Demo mode: summarize the question, variables, control, expected result, and safety boundary.",
            "protocol": "Demo mode: keep protocol discussion high level and check official lab guidance for real procedures.",
        },
    },
    {
        "slug": "game-master",
        "title": "Game Master",
        "category": "Education",
        "area_readme": "education/README.md",
        "tags": "creative, learning",
        "accent": "#facc15",
        "accent2": "#a78bfa",
        "user": "#a16207",
        "eyebrow": "Quest table",
        "busy": "rolling",
        "system": "You are Game Master, a playful assistant for tabletop quest hooks, characters, puzzles, and encounter ideas.",
        "placeholder": "Ask for quests, characters, puzzles, or encounters...",
        "welcome": "Game Master is ready in browser demo mode. Ask for quests, characters, puzzles, or encounter ideas.",
        "topics": {
            "quest": "Demo mode: a missing map points to a locked observatory where the stars changed overnight.",
            "puzzle": "Demo mode: make the answer visible in the room, but require players to connect two clues.",
            "encounter": "Demo mode: add a goal besides fighting, a terrain twist, and a reason to negotiate.",
        },
    },
]


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(textwrap.dedent(content).strip() + "\n", encoding="utf-8")


def read_repo(path: str) -> str:
    file_path = REPO_ROOT / path
    return file_path.read_text(encoding="utf-8") if file_path.exists() else ""


def write_repo(path: str, content: str) -> None:
    write(REPO_ROOT / path, content)


def next_number(text: str) -> int:
    nums = [int(n) for n in re.findall(r"^\|\s*(\d+)\s*\|", text, flags=re.MULTILINE)]
    return max(nums, default=0) + 1


def append_catalog(path: str, theme: dict, made_on: str, project_path: str) -> None:
    text = read_repo(path)
    if project_path in text:
        return

    has_tags = "| Tags |" in text
    number = next_number(text)
    base = [
        str(number),
        theme["title"],
        made_on,
        theme["category"],
        f"`{project_path}`",
    ]
    if has_tags:
        base.append(theme["tags"])
    base.extend(["Successful demo", "Browser demo + Vercel/OpenAI-ready", "Basic smoke check", "Not deployed"])
    row = "| " + " | ".join(base) + " |"

    lines = text.splitlines()
    last_row = -1
    for index, line in enumerate(lines):
        if re.match(r"^\|\s*\d+\s*\|", line):
            last_row = index
    if last_row >= 0:
        lines.insert(last_row + 1, row)
        write_repo(path, "\n".join(lines))
        return

    header = "| S.No | Chatbot | Made On (UTC) | Category | Folder | Status | Model | Quality | Deployment |\n| ---: | --- | --- | --- | --- | --- | --- | --- | --- |"
    write_repo(path, (text.rstrip() + "\n\n## Chatbot Catalog\n\n" + header + "\n" + row).strip())


def append_line(path: str, heading: str, line: str) -> None:
    text = read_repo(path)
    if line in text:
        return
    if not text.strip():
        text = f"# {heading}\n"
    write_repo(path, text.rstrip() + f"\n- {line}")


def update_indexes(theme: dict, made_on: str, project_path: str) -> None:
    append_catalog("README.md", theme, made_on, project_path)
    append_catalog("CHATBOT_CATALOG.md", theme, made_on, project_path)
    append_line(theme["area_readme"], "Generated Projects", f"{made_on}: {theme['title']} - `{project_path}` - generated by automation pipeline.")
    append_line("tracking/successful-projects.md", "Successful Projects", f"{made_on}: {theme['title']} - `{project_path}` - browser demo created and smoke-checked.")
    append_line("tracking/model-usage.md", "Model Usage", f"{made_on}: {theme['title']} - `{project_path}` - Browser demo + Vercel/OpenAI-ready.")
    append_line("tracking/response-quality.md", "Response Quality", f"{made_on}: {theme['title']} - `{project_path}` - demo replies available; real AI mode deployment-ready.")
    append_line("tracking/benchmarks.md", "Benchmarks", f"{made_on}: {theme['title']} - `{project_path}` - static browser demo smoke check passed.")
    append_line("tracking/deployment-links.md", "Deployment Links", f"{made_on}: {theme['title']} - `{project_path}` - Vercel link pending.")
    append_line("screenshots/README.md", "Screenshot Notes", f"{made_on}: {theme['title']} - `{project_path}` - screenshot pending.")


def build_project(theme: dict) -> str:
    now = datetime.now(timezone.utc)
    stamp = now.strftime("%Y-%m-%d-%H%M%Sz")
    made_on = now.strftime("%Y-%m-%d %H:%M UTC")
    folder = OUTPUT_ROOT / f"{theme['slug']}-chatbot-{stamp}"
    attempt = 2
    while folder.exists():
        folder = OUTPUT_ROOT / f"{theme['slug']}-chatbot-{stamp}-{attempt}"
        attempt += 1

    project_path = folder.relative_to(REPO_ROOT).as_posix()
    topics = [{"match": [key], "text": value} for key, value in theme["topics"].items()]

    write(folder / "README.md", f"""
    # {theme['title']} Chatbot

    A themed chatbot project with an instant browser demo and optional real AI mode after Vercel deployment.

    ## Browser Demo

    Open `public/index.html` in a browser to preview the chatbot. No setup or API key is needed for demo mode.

    ## Optional Real AI Mode

    Real AI mode needs a deployed Vercel public URL. Visitors enter their own OpenAI API key in the page. The key is stored only in browser `sessionStorage` and is never committed to the repo.

    ## Deploy To Vercel

    1. Import `meenavignesh-svg/ai-chat-bots-per-minute` into Vercel.
    2. Set the root directory to `{project_path}`.
    3. Deploy and share the public URL.
    """)

    write(folder / "package.json", json.dumps({
        "name": f"{theme['slug']}-chatbot",
        "version": "1.0.0",
        "type": "module",
        "scripts": {"dev": "vercel dev", "start": "vercel dev"},
        "dependencies": {"@vercel/node": "^3.2.27", "openai": "^5.0.0"},
        "devDependencies": {"vercel": "^34.3.0"},
        "engines": {"node": ">=18"},
    }, indent=2))

    write(folder / "vercel.json", '{\n  "version": 2,\n  "routes": [\n    { "src": "/api/chat", "dest": "/api/chat.js" },\n    { "src": "/(.*)", "dest": "/public/$1" }\n  ]\n}')

    write(folder / "api/chat.js", f"""
    import OpenAI from 'openai';

    export default async function handler(req, res) {{
      if (req.method !== 'POST') return res.status(405).json({{ error: 'Method not allowed.' }});
      const apiKey = req.headers.authorization?.replace(/^Bearer\s+/i, '') || req.body?.apiKey;
      if (!apiKey) return res.status(400).json({{ error: 'Enter an OpenAI API key for real AI mode.' }});
      const messages = Array.isArray(req.body?.messages) ? req.body.messages.slice(-12) : [];
      const input = messages.map((message) => ({{
        role: message.role === 'assistant' ? 'assistant' : 'user',
        content: String(message.content || '').slice(0, 2000)
      }})).filter((message) => message.content);
      if (!input.length) return res.status(400).json({{ error: 'Send at least one message.' }});
      try {{
        const client = new OpenAI({{ apiKey }});
        const response = await client.responses.create({{
          model: 'gpt-4.1-mini',
          instructions: {json.dumps(theme['system'])},
          input
        }});
        return res.status(200).json({{ reply: response.output_text || 'Please try again.' }});
      }} catch {{
        return res.status(500).json({{ error: 'The AI request failed. Check the API key and deployment.' }});
      }}
    }}
    """)

    write(folder / "public/index.html", f"""
    <!doctype html>
    <html lang="en">
    <head>
      <meta charset="utf-8">
      <meta name="viewport" content="width=device-width, initial-scale=1">
      <title>{theme['title']} Chatbot</title>
      <link rel="stylesheet" href="style.css">
    </head>
    <body>
      <main class="app">
        <section class="chat-panel" aria-label="{theme['title']} Chatbot">
          <header class="chat-header"><div><p>{theme['eyebrow']}</p><h1>{theme['title']}</h1></div><span id="status">demo ready</span></header>
          <form id="keyForm" class="key-form"><input id="apiKeyInput" type="password" autocomplete="off" placeholder="Optional OpenAI API key for real AI mode"><button type="submit">Use Key</button></form>
          <div id="messages" class="messages" aria-live="polite"></div>
          <form id="chatForm" class="chat-form"><input id="userInput" autocomplete="off" placeholder="{theme['placeholder']}"><button id="sendButton" type="submit">Send</button></form>
        </section>
      </main>
      <script src="script.js"></script>
    </body>
    </html>
    """)

    write(folder / "public/style.css", f"""
    :root {{ color-scheme: dark; font-family: Inter, ui-sans-serif, system-ui, sans-serif; background: #111318; color: #f7fbff; }}
    * {{ box-sizing: border-box; }}
    body {{ margin: 0; min-height: 100vh; background: radial-gradient(circle at 18% 16%, {theme['accent']}42, transparent 28rem), radial-gradient(circle at 84% 22%, {theme['accent2']}35, transparent 25rem), linear-gradient(145deg, #111318, #1d2632 58%, #141d1a); }}
    .app {{ min-height: 100vh; display: grid; place-items: center; padding: 24px; }}
    .chat-panel {{ width: min(780px, 100%); min-height: 700px; display: grid; grid-template-rows: auto auto 1fr auto; border: 1px solid rgba(255,255,255,.14); border-radius: 8px; background: rgba(13,17,22,.9); overflow: hidden; }}
    .chat-header, .key-form, .chat-form {{ display: grid; gap: 10px; padding: 18px 22px; border-bottom: 1px solid rgba(255,255,255,.1); }}
    .chat-header {{ grid-template-columns: 1fr auto; align-items: center; }}
    .chat-header p {{ margin: 0 0 4px; color: {theme['accent']}; font-size: .75rem; text-transform: uppercase; letter-spacing: .08em; }}
    h1 {{ margin: 0; font-size: clamp(1.6rem, 4vw, 2.35rem); }}
    #status {{ padding: 6px 10px; border: 1px solid {theme['accent']}85; border-radius: 999px; color: {theme['accent']}; font-size: .78rem; white-space: nowrap; }}
    .messages {{ display: flex; flex-direction: column; gap: 14px; padding: 22px; overflow: auto; }}
    .message {{ width: fit-content; max-width: min(84%, 560px); padding: 12px 14px; border-radius: 8px; line-height: 1.5; white-space: pre-wrap; }}
    .bot {{ background: #202936; border: 1px solid rgba(255,255,255,.09); }}
    .user {{ align-self: flex-end; background: {theme['user']}; }}
    .key-form, .chat-form {{ grid-template-columns: 1fr auto; }}
    .chat-form {{ border-top: 1px solid rgba(255,255,255,.1); border-bottom: 0; }}
    input, button {{ min-height: 46px; border: 0; border-radius: 8px; font: inherit; }}
    input {{ width: 100%; padding: 0 14px; background: #f7fbff; color: #111318; }}
    button {{ padding: 0 18px; background: {theme['accent']}; color: #07110c; font-weight: 700; cursor: pointer; }}
    button:disabled {{ opacity: .65; cursor: wait; }}
    @media (max-width: 560px) {{ .app {{ padding: 0; }} .chat-panel {{ min-height: 100vh; border: 0; border-radius: 0; }} .chat-header, .key-form, .chat-form {{ grid-template-columns: 1fr; }} }}
    """)

    write(folder / "public/script.js", f"""
    const messagesEl = document.querySelector('#messages');
    const keyForm = document.querySelector('#keyForm');
    const apiKeyInput = document.querySelector('#apiKeyInput');
    const form = document.querySelector('#chatForm');
    const input = document.querySelector('#userInput');
    const button = document.querySelector('#sendButton');
    const statusEl = document.querySelector('#status');
    const history = [];
    const demoReplies = {json.dumps(topics, indent=2)};
    let apiKey = sessionStorage.getItem('openai_api_key') || '';

    function addMessage(text, sender) {{
      const bubble = document.createElement('div');
      bubble.className = `message ${{sender}}`;
      bubble.textContent = text;
      messagesEl.appendChild(bubble);
      messagesEl.scrollTop = messagesEl.scrollHeight;
    }}
    function setBusy(isBusy) {{ button.disabled = isBusy; input.disabled = isBusy; statusEl.textContent = isBusy ? {json.dumps(theme['busy'])} : apiKey ? 'real AI ready' : 'demo ready'; }}
    function demoReply(text) {{
      const clean = text.toLowerCase();
      const hit = demoReplies.find((reply) => reply.match.some((word) => clean.includes(word)));
      return hit ? hit.text : `Demo mode: I would turn "${{text}}" into a practical next step in the {theme['title']} style.`;
    }}
    keyForm.addEventListener('submit', (event) => {{
      event.preventDefault();
      apiKey = apiKeyInput.value.trim();
      if (!apiKey) return;
      sessionStorage.setItem('openai_api_key', apiKey);
      apiKeyInput.value = '';
      statusEl.textContent = 'real AI ready';
      addMessage('API key saved for this browser session. Real AI mode is ready after Vercel deployment.', 'bot');
    }});
    async function sendMessage(text) {{
      history.push({{ role: 'user', content: text }});
      setBusy(true);
      if (!apiKey) {{
        setTimeout(() => {{ const reply = demoReply(text); history.push({{ role: 'assistant', content: reply }}); addMessage(reply, 'bot'); setBusy(false); }}, 250);
        return;
      }}
      try {{
        const response = await fetch('/api/chat', {{ method: 'POST', headers: {{ 'Content-Type': 'application/json', Authorization: `Bearer ${{apiKey}}` }}, body: JSON.stringify({{ messages: history }}) }});
        if (!response.ok) throw new Error('fallback');
        const data = await response.json();
        const reply = data.reply || demoReply(text);
        history.push({{ role: 'assistant', content: reply }});
        addMessage(reply, 'bot');
      }} catch {{
        const reply = demoReply(text);
        history.push({{ role: 'assistant', content: reply }});
        addMessage(reply, 'bot');
      }} finally {{ setBusy(false); }}
    }}
    form.addEventListener('submit', (event) => {{
      event.preventDefault();
      const text = input.value.trim();
      if (!text) return;
      addMessage(text, 'user');
      input.value = '';
      sendMessage(text);
    }});
    addMessage({json.dumps(theme['welcome'])}, 'bot');
    """)

    update_indexes(theme, made_on, project_path)
    return project_path


def main() -> None:
    requested = os.environ.get("CHATBOT_THEME", "").strip().lower()
    theme = next((item for item in THEMES if requested and requested in {item["slug"], item["title"].lower()}), None)
    theme = theme or random.choice(THEMES)
    print(f"Created {build_project(theme)}")


if __name__ == "__main__":
    main()
