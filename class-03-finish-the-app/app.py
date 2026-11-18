# app.py
# The face. A small Gradio page around the function you already wrote.

import gradio as gr
from scraper import fetch_website_contents
from summarizer import summarize


def summarize_url(url):
    if not url or not url.strip():
        return "Paste a URL first."

    page = fetch_website_contents(url)

    if page.startswith("COULD_NOT_FETCH"):
        return "Could not read that page. Check the URL, or try another site."

    result = summarize(page)

    if "NO_ARTICLE_FOUND" in result:
        return "That page does not seem to have an article on it."

    return result


demo = gr.Interface(
    fn=summarize_url,
    inputs=gr.Textbox(
        label="Website URL",
        placeholder="en.wikipedia.org/wiki/Pune_Metro",
    ),
    outputs=gr.Markdown(label="Summary"),
    title="AI Website Summarizer",
    description="Paste a link. Get the short version.",
)

if __name__ == "__main__":
    demo.launch(share=True)
