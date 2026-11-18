# Noveve AI module

Hands-on Python demos for the AI module. One folder per class. Shared install at the repo root; each class keeps its own `.env` next to the script.

## Setup once

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Get a Groq key at [console.groq.com/keys](https://console.groq.com/keys). It starts with `gsk_`.

## Classes

| Class | Folder | What you build |
| --- | --- | --- |
| 1 | [`class-01-first-call`](class-01-first-call/) | Load a key, send one chat call, print the reply |
| 2 | [`class-02-prompt-engineering-basics`](class-02-prompt-engineering-basics/) | Move a tuned prompt into code as a page summarizer |
| 3 | [`class-03-finish-the-app`](class-03-finish-the-app/) | Scrape a real page, harden the prompt, ship a Gradio UI |

Open the class folder, copy `.env.example` to `.env`, put your key in, then run the Python file in that folder.
