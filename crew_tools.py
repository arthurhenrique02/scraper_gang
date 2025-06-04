import re

import requests
from bs4 import BeautifulSoup
from crewai.tools import tool
from duckduckgo_search import DDGS


@tool
def search_and_scrape(query: str, max_articles: int = 3) -> str:
    """
    Search the web for articles and scrape their content. Return a compiled text blob.
    """

    scraped_articles = []
    with DDGS() as ddgs:
        results = ddgs.text(query, max_results=max_articles)
        for result in results:
            try:
                url = result["href"]
                html = requests.get(url, timeout=5).text
                soup = BeautifulSoup(html, "html.parser")
                paragraphs = soup.find_all("p")
                text = " ".join(p.get_text() for p in paragraphs)
                clean_text = re.sub(r"\s+", " ", text)
                scraped_articles.append(f"URL: {url}\n{clean_text[:3000]}")
            except Exception as e:
                scraped_articles.append(f"Failed to scrape {url}: {str(e)}")
    return "\n\n---\n\n".join(scraped_articles)
