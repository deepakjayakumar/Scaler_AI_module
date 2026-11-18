# scraper.py
# URL in, readable page text out. No AI anywhere in this file.

import requests
from bs4 import BeautifulSoup

HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; ClassSummarizer/1.0)"}

# Cap how much page text we keep. Stops a huge page from blowing up cost and latency.
MAX_CHARS = 12_000


def fetch_website_contents(url):
    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    try:
        response = requests.get(url, headers=HEADERS, timeout=15)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        return f"COULD_NOT_FETCH: {e}"

    soup = BeautifulSoup(response.text, "html.parser")
    title = soup.title.string if soup.title else "No title found"

    # Drop the furniture: scripts, styling, menus, footers, images, forms.
    for tag in soup(["script", "style", "nav", "footer", "header", "img", "input"]):
        tag.decompose()

    text = soup.get_text(separator="\n", strip=True)
    if len(text) > MAX_CHARS:
        text = text[:MAX_CHARS] + "\n\n[truncated]"

    return f"Title: {title}\n\nPage contents:\n{text}"


if __name__ == "__main__":
    page = fetch_website_contents("https://en.wikipedia.org/wiki/Pune_Metro")
    print(page)
    print("...")
    print(f"\nTotal characters kept: {len(page)}")
