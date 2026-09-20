import requests
from bs4 import BeautifulSoup
from typing import Dict, Any


def scrape_pitch_url(url: str, timeout: float = 4.0) -> Dict[str, Any]:
    """Scrapes clean text and meta information from a startup website."""
    try:
        resp = requests.get(
            url,
            headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"},
            timeout=timeout
        )
        if resp.status_code == 200:
            soup = BeautifulSoup(resp.text, "html.parser")
            title = soup.title.string if soup.title else ""
            paragraphs = [p.get_text(strip=True) for p in soup.find_all("p")]
            return {
                "url": url,
                "title": title,
                "text": " ".join(paragraphs[:10]),
                "status": "success"
            }
    except Exception as e:
        return {"url": url, "error": str(e), "status": "failed"}
    return {"url": url, "status": "failed"}
