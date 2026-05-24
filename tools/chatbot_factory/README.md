# Chatbot Factory Tool

`generate.py` creates one new chatbot project with browser demo mode.

## Scheduled Workflow

The scheduled workflow runs the generator and commits the new chatbot project. New projects should also be reflected in the archive catalog and tracking files.

## Archive Updates Expected

For every generated chatbot, update:

- root `README.md`
- `CHATBOT_CATALOG.md`
- relevant research-area README
- `tracking/successful-projects.md`
- `tracking/model-usage.md`
- `tracking/response-quality.md`
- `tracking/benchmarks.md`
- `tracking/deployment-links.md`
- `screenshots/README.md`

## Test Expected

Each chatbot should be checked for:

- valid `public/index.html`
- linked `public/style.css`
- linked `public/script.js`
- visible chat form
- built-in demo replies without setup

## Run Locally

From the repository root:

```bash
python tools/chatbot_factory/generate.py
```

Optional theme:

```bash
CHATBOT_THEME=biotech-notes python tools/chatbot_factory/generate.py
```
