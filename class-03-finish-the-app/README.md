# Class 3 — Finish the app

Classes 1 and 2 gave you a model call and a prompt. Today you fill the gaps: fetch a real page, keep the model honest about that page, and put a face on the whole thing.

| Piece | Status |
| --- | --- |
| A URL the user pastes | today |
| Something that fetches the page | today |
| A prompt | Class 2, now with safety rules |
| A model call | Class 1 |
| A face people can use | today |

The catch: the moment your app fetches a page, it is reading text written by a stranger. Everything before now, you controlled every word that reached the model. From today you do not.

## Setup

From the **repo root**, activate the same venv and install the new packages:

```bash
source .venv/bin/activate
pip install -r requirements.txt
```

In **this folder**, put your key next to the scripts (same key as Class 1):

```bash
cp .env.example .env
```

```
GROQ_API_KEY=gsk_your_key_here
```

All of these files must sit in **this same folder**: `scraper.py`, `summarizer.py`, `app.py`, `evil.html`, and `.env`.

## Step 1 — The scraper

Open `scraper.py`. There is no AI in this file. It takes a URL, fetches the page, throws away scripts/menus/footers, and returns readable text as one string.

Run it:

```bash
python scraper.py
```

You should see the first ~600 characters of the Pune Metro Wikipedia page, then a total character count.

Look at what came back. Is it clean? What survived that you did not expect?

Why strip navigation in code when the prompt already says to ignore it? Two reasons: it is cheaper (fewer tokens), and it is more reliable (text that was never there cannot confuse the model).

Scraping is not always allowed. Some sites block it, some need a login, and some ask you not to in their terms. For this class, use ordinary public pages. If a page refuses, that is a normal outcome, not a bug in your code.

## Step 2 — Whose words are these

Your app now builds a prompt from pieces with different origins. The model sees one stream of text and cannot tell them apart.

| Layer | Who writes it | Trust |
| --- | --- | --- |
| System prompt | You, in `summarizer.py` | High |
| User message wrapper | You, the `<page>...</page>` line | High |
| Scraped page text | Whoever runs that website | None |

If you want the model to treat the page differently, you have to say so explicitly, in words, inside the prompt.

## Step 3 — Failures you will actually see

Before you trust the summary, try these on real pages:

1. **No article** — point it at a login page, cookie wall, or 404. A page with no article can still produce a confident summary of a form or an invented article.
2. **Extra facts** — summarise a short article about something well-known. Check every sentence against the page. The usual failure is topping up: three facts from the page and a fourth from general knowledge, in the same confident tone.
3. **Long page** — summarise something near the `MAX_CHARS` cap. Accuracy often sags in the middle.
4. **Run twice** — same URL twice. With `temperature=0.2` they should be close. If a *fact* changes, that fact is being generated, not read.

## Step 4 — Grounding in the system prompt

Open `summarizer.py`. The system prompt now includes rules like:

- summarise only what is written in the page
- do not add background from general knowledge
- if there is no article, reply exactly `NO_ARTICLE_FOUND`
- every number must appear in the page text

Giving the model an exact way to say no matters. Without it, "I don't know" is not among the shapes of answer it reaches for.

If you still have your own prompt from Class 2, paste it in and keep these grounding lines. Then run:

```bash
python summarizer.py
```

## Step 5 — Prompt injection

Your summariser reads text written by strangers. That text can contain instructions. To the model it is all just text.

`evil.html` is a fake product review with a hidden instruction at the bottom. Read it through the same cleaning path the scraper uses:

```bash
python - <<'EOF'
from bs4 import BeautifulSoup
from summarizer import summarize

with open("evil.html", encoding="utf-8") as f:
    soup = BeautifulSoup(f.read(), "html.parser")

text = soup.get_text(separator="\n", strip=True)
print(text)
print("\n--- that entire string is about to become part of your prompt ---\n")
print(summarize(text))
EOF
```

Whatever the model does, notice that the attacker's sentence is sitting inside the prompt. On a real page this text does not have to be visible — it can be white on white or off-screen.

This summariser is low risk for one reason: it cannot do anything except produce text. The same injection against an app that can send email or run code is a different event.

## Step 6 — Defend the summariser

`summarizer.py` already has the main defences:

1. **Mark the boundary** — page text sits between `<page>` and `</page>`.
2. **Declare it data** — `BOUNDARY_RULES` says that text is never an instruction.
3. **Ground it** — the Section 4 / Step 4 rules above.
4. **Constrain the output** — reply is only the summary, at most 80 words.
5. **Cap the input in code** — `MAX_CHARS` in `scraper.py`.
6. **Handle fetch failure in code** — `COULD_NOT_FETCH` in `scraper.py`.

Prompt rules help with common cases. The two you should trust most are the ones that are code: the character cap and the fetch failure path. Sentences can be argued with. Code does not negotiate.

Re-run the `evil.html` test after you understand those rules. Then try a login page and a page that does not resolve.

## Step 7 — The Gradio interface

Nobody is going to run your Python script for fun. `app.py` turns `summarize` into a web page: a URL box, a results panel, no HTML/CSS/JS of your own.

Look at `summarize_url` carefully. Both failure paths are handled there: a fetch that failed, and a page with no article. The user gets a plain sentence instead of a stack trace or an invented summary.

From **this folder**:

```bash
python app.py
```

Gradio prints two links, something like:

```text
Running on local URL:  http://127.0.0.1:7860
Running on public URL: https://a1b2c3d4e5.gradio.live
```

Open the local one, paste a URL, and try it. The public link works for anyone for a limited time (Gradio currently says about a week) — send it to a classmate and have them try to break it.

`share=True` routes traffic through Gradio's servers to your laptop. Fine for a demo. Do not leave it running with anything sensitive behind it. Stop with Ctrl+C when you are done.

If you get an import error, check that `app.py`, `scraper.py`, `summarizer.py`, and `.env` are all in the same folder before debugging anything else.

## What a prompt cannot do

Keep this list nearby:

- A prompt cannot make a model know something it does not know. It can only stop it pretending.
- A prompt cannot guarantee a behaviour. It makes a behaviour much more likely.
- A prompt cannot keep a secret. Anything in it should be safe to read out loud.
- A prompt cannot limit what your app is able to do. Only the code and the permissions around it can.

## What you built

Four files and a key:

- `scraper.py` — fetch and clean a page
- `summarizer.py` — your prompt plus grounding and boundary rules
- `evil.html` — a local injection demo
- `app.py` — a Gradio face with a public link

You also handled the common failures: a page that will not load, a page with no article, a page that is too long, and a page that tries to talk to your model.

## Stuck?

- Import error on `scraper` or `summarizer` → run from this folder; all files must be here.
- `No GROQ_API_KEY` → `.env` missing, misnamed, or not next to the scripts.
- Unexpected keyword on `reasoning_effort` → delete that one line and keep going. After class: `pip install -U openai`.
- Site returns `COULD_NOT_FETCH` → normal for blocked pages; try Wikipedia or another public article.
- Public Gradio link dies after a limited time → expected. For something permanent later, a free Hugging Face Space can host the same files.

## Resources

| Resource | URL |
| --- | --- |
| Free API keys | https://console.groq.com |
| Gradio docs | https://www.gradio.app/docs |
| Hugging Face Spaces | https://huggingface.co/spaces |
