"""
Web scraping utilities for DeepLens.

Fetches paper content from URLs (arXiv, Semantic Scholar, DOI links)
and researcher publications from Google Scholar profiles.
"""

import re
import time
import logging
from typing import Dict, Any, List, Optional
from urllib.parse import urlparse, parse_qs

import requests
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

# Common headers to mimic a browser request
_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/125.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9",
}

_REQUEST_TIMEOUT = 30  # seconds
_MAX_RETRIES = 5
_BASE_DELAY = 3  # seconds


def _request_with_retry(url: str, **kwargs) -> requests.Response:
    """HTTP GET with exponential-backoff retry on 429 / 5xx errors."""
    kwargs.setdefault("headers", _HEADERS)
    kwargs.setdefault("timeout", _REQUEST_TIMEOUT)

    last_exc: Optional[Exception] = None
    for attempt in range(_MAX_RETRIES):
        try:
            resp = requests.get(url, **kwargs)
            if resp.status_code == 429 or resp.status_code >= 500:
                delay = _BASE_DELAY * (2 ** attempt)
                retry_after = resp.headers.get("Retry-After")
                if retry_after and retry_after.isdigit():
                    delay = max(delay, int(retry_after))
                logger.warning(
                    "HTTP %s from %s — retrying in %ds (attempt %d/%d)",
                    resp.status_code, url, delay, attempt + 1, _MAX_RETRIES,
                )
                print(f"  ⏳ {resp.status_code} rate-limited by server, retrying in {delay}s …")
                time.sleep(delay)
                continue
            resp.raise_for_status()
            return resp
        except requests.exceptions.HTTPError:
            raise  # non-retryable HTTP errors (4xx other than 429)
        except requests.exceptions.RequestException as exc:
            last_exc = exc
            delay = _BASE_DELAY * (2 ** attempt)
            logger.warning(
                "Request error for %s — %s, retrying in %ds (attempt %d/%d)",
                url, exc, delay, attempt + 1, _MAX_RETRIES,
            )
            time.sleep(delay)

    raise last_exc or RuntimeError(f"Failed to fetch {url} after {_MAX_RETRIES} retries")


# ---------------------------------------------------------------------------
# Paper fetching
# ---------------------------------------------------------------------------

def fetch_paper(url: str) -> Dict[str, Any]:
    """
    Fetch a paper's metadata and content from a URL.

    Supports:
      - arXiv (abs or pdf links)
      - Semantic Scholar (API)
      - DOI links (via Crossref / content negotiation)
      - Generic web pages (best-effort extraction)

    Returns:
        {
            "title": str,
            "authors": list[str],
            "abstract": str,
            "content": str,       # full text when available, else abstract
            "source": str,        # "arxiv" | "semantic_scholar" | "doi" | "web"
            "url": str,
        }
    """
    url = url.strip()
    parsed = urlparse(url)
    domain = parsed.netloc.lower()

    if "arxiv.org" in domain:
        return _fetch_arxiv(url)
    elif "semanticscholar.org" in domain:
        return _fetch_semantic_scholar(url)
    elif "doi.org" in domain or url.startswith("10."):
        return _fetch_doi(url)
    else:
        return _fetch_generic_page(url)


def _extract_arxiv_id(url: str) -> str:
    """Extract arXiv ID from various URL formats."""
    # e.g. https://arxiv.org/abs/2301.12345, /pdf/2301.12345, /html/2301.12345v1
    m = re.search(r"arxiv\.org/(?:abs|pdf|html)/([^\s?#]+)", url)
    if m:
        return m.group(1).rstrip(".pdf")
    # bare ID
    m = re.search(r"(\d{4}\.\d{4,5}(?:v\d+)?)", url)
    if m:
        return m.group(1)
    raise ValueError(f"Cannot extract arXiv ID from: {url}")


def _detect_arxiv_format(url: str) -> str:
    """Detect arXiv URL format: 'abs', 'pdf', or 'html'."""
    if "/html/" in url:
        return "html"
    elif "/pdf/" in url:
        return "pdf"
    return "abs"


def _fetch_arxiv_html_content(arxiv_id: str) -> Optional[str]:
    """
    Try to fetch the full paper text from the arXiv HTML version.

    Not all papers have an HTML rendering — returns None if unavailable.
    """
    html_url = f"https://arxiv.org/html/{arxiv_id}"
    try:
        resp = _request_with_retry(html_url)
        soup = BeautifulSoup(resp.text, "html.parser")

        # Remove non-content elements
        for tag in soup(["script", "style", "nav", "footer", "header"]):
            tag.decompose()

        # arXiv HTML papers use <article> or class "ltx_document"
        article = (
            soup.find("article")
            or soup.find("div", class_="ltx_document")
            or soup.find("main")
            or soup.find("body")
        )
        if not article:
            return None

        content = article.get_text(separator="\n", strip=True)
        if len(content) < 500:
            # Too short — likely an error page, not a real paper
            return None
        if len(content) > 30000:
            content = content[:30000] + "\n\n[... content truncated ...]"
        return content
    except Exception as exc:
        logger.info("HTML version not available for %s: %s", arxiv_id, exc)
        return None


def _fetch_arxiv(url: str) -> Dict[str, Any]:
    """
    Fetch paper from arXiv.  Handles three URL formats:

      - /abs/ID  — metadata via API (abstract only)
      - /html/ID — scrapes full paper text from the HTML rendering
      - /pdf/ID  — tries HTML rendering for full text, falls back to abstract
    """
    arxiv_id = _extract_arxiv_id(url)
    url_format = _detect_arxiv_format(url)

    # --- Step 1: metadata from the arXiv Atom API (always) ----------------
    api_url = f"http://export.arxiv.org/api/query?id_list={arxiv_id}"
    resp = _request_with_retry(api_url)

    soup = BeautifulSoup(resp.text, "html.parser")
    entry = soup.find("entry")
    if not entry:
        raise ValueError(f"No arXiv entry found for ID {arxiv_id}")

    title = entry.find("title").get_text(strip=True) if entry.find("title") else ""
    abstract = entry.find("summary").get_text(strip=True) if entry.find("summary") else ""
    authors = [
        a.find("name").get_text(strip=True)
        for a in entry.find_all("author") if a.find("name")
    ]

    # --- Step 2: full text (for html / pdf links) -------------------------
    content = abstract  # default: abstract only

    if url_format in ("html", "pdf"):
        # User gave an html or pdf link → they likely want the full text.
        html_content = _fetch_arxiv_html_content(arxiv_id)
        if html_content:
            content = html_content
            logger.info(
                "Fetched full HTML content for %s (%d chars)",
                arxiv_id, len(content),
            )
        else:
            logger.info(
                "HTML version unavailable for %s; falling back to abstract",
                arxiv_id,
            )

    return {
        "title": title,
        "authors": authors,
        "abstract": abstract,
        "content": content,
        "source": "arxiv",
        "url": f"https://arxiv.org/abs/{arxiv_id}",
    }


def _fetch_semantic_scholar(url: str) -> Dict[str, Any]:
    """Fetch paper from Semantic Scholar API."""
    # Extract paper ID from URL
    m = re.search(r"semanticscholar\.org/paper/[^/]*/([a-f0-9]+)", url)
    if not m:
        m = re.search(r"semanticscholar\.org/paper/([a-f0-9]+)", url)
    if not m:
        raise ValueError(f"Cannot extract Semantic Scholar paper ID from: {url}")

    paper_id = m.group(1)
    api_url = f"https://api.semanticscholar.org/graph/v1/paper/{paper_id}?fields=title,abstract,authors"

    resp = _request_with_retry(api_url)
    data = resp.json()

    return {
        "title": data.get("title", ""),
        "authors": [a.get("name", "") for a in data.get("authors", [])],
        "abstract": data.get("abstract", ""),
        "content": data.get("abstract", ""),
        "source": "semantic_scholar",
        "url": url,
    }


def _fetch_doi(url: str) -> Dict[str, Any]:
    """Fetch paper metadata using DOI content negotiation (Crossref)."""
    doi = url
    if "doi.org/" in url:
        doi = url.split("doi.org/", 1)[1]

    api_url = f"https://api.crossref.org/works/{doi}"
    resp = _request_with_retry(api_url)
    data = resp.json().get("message", {})

    title_parts = data.get("title", [""])
    title = title_parts[0] if title_parts else ""
    authors = []
    for a in data.get("author", []):
        name = f"{a.get('given', '')} {a.get('family', '')}".strip()
        if name:
            authors.append(name)
    abstract = data.get("abstract", "")
    # Strip HTML tags from abstract
    if abstract:
        abstract = BeautifulSoup(abstract, "html.parser").get_text()

    return {
        "title": title,
        "authors": authors,
        "abstract": abstract,
        "content": abstract,
        "source": "doi",
        "url": f"https://doi.org/{doi}",
    }


def _fetch_generic_page(url: str) -> Dict[str, Any]:
    """Best-effort extraction from a generic web page."""
    resp = _request_with_retry(url)

    soup = BeautifulSoup(resp.text, "html.parser")

    # Remove scripts/styles
    for tag in soup(["script", "style", "nav", "footer", "header"]):
        tag.decompose()

    title = ""
    if soup.title:
        title = soup.title.get_text(strip=True)

    # Try to find the main article body
    article = soup.find("article") or soup.find("main") or soup.find("body")
    content = article.get_text(separator="\n", strip=True) if article else ""

    # Truncate very long pages
    if len(content) > 15000:
        content = content[:15000] + "\n\n[... content truncated ...]"

    return {
        "title": title,
        "authors": [],
        "abstract": "",
        "content": content,
        "source": "web",
        "url": url,
    }


# ---------------------------------------------------------------------------
# Google Scholar scraping
# ---------------------------------------------------------------------------

def fetch_google_scholar_profile(url: str) -> Dict[str, Any]:
    """
    Fetch a researcher's publications from a Google Scholar profile URL.

    Args:
        url: Google Scholar profile URL, e.g.
             https://scholar.google.com/citations?user=XXXXXXXX

    Returns:
        {
            "name": str,
            "affiliation": str,
            "publications": [
                {"title": str, "year": int|None, "cited_by": int, "abstract": str}
            ],
            "url": str,
        }

    Raises:
        ValueError: If the URL is not a Google Scholar profile
        RuntimeError: If the page cannot be fetched (CAPTCHA, private, etc.)
    """
    url = url.strip()
    if "scholar.google" not in url:
        raise ValueError(
            f"Not a Google Scholar URL: {url}\n"
            "Expected format: https://scholar.google.com/citations?user=XXXXXXXX"
        )

    # Make sure we request enough results
    if "cstart" not in url and "pagesize" not in url:
        separator = "&" if "?" in url else "?"
        url = url + f"{separator}cstart=0&pagesize=100"

    resp = _request_with_retry(url)

    soup = BeautifulSoup(resp.text, "html.parser")

    # Detect CAPTCHA / block
    if "Please show you" in resp.text or soup.find("form", id="gs_captcha_f"):
        raise RuntimeError(
            "Google Scholar returned a CAPTCHA. "
            "Please try again later or provide publications manually."
        )

    # Extract researcher name
    name_tag = soup.find("div", id="gsc_prf_in")
    name = name_tag.get_text(strip=True) if name_tag else "Unknown"

    # Affiliation
    aff_tag = soup.find("div", class_="gsc_prf_il")
    affiliation = aff_tag.get_text(strip=True) if aff_tag else ""

    # Extract publications
    publications = []
    rows = soup.select("tr.gsc_a_tr")
    for row in rows:
        title_tag = row.select_one("a.gsc_a_at")
        title = title_tag.get_text(strip=True) if title_tag else ""

        year_tag = row.select_one("span.gsc_a_h.gsc_a_hc")
        if not year_tag:
            year_tag = row.select_one("td.gsc_a_y span")
        year_text = year_tag.get_text(strip=True) if year_tag else ""
        year = int(year_text) if year_text.isdigit() else None

        cite_tag = row.select_one("a.gsc_a_ac")
        cite_text = cite_tag.get_text(strip=True) if cite_tag else "0"
        cited_by = int(cite_text) if cite_text.isdigit() else 0

        # Google Scholar doesn't show abstracts on profile pages,
        # so we leave this empty (the LLM can still evaluate from titles+years)
        publications.append({
            "title": title,
            "year": year,
            "cited_by": cited_by,
            "abstract": "",
        })

    if not publications:
        logger.warning("No publications found — the profile may be empty or restricted.")

    return {
        "name": name,
        "affiliation": affiliation,
        "publications": publications,
        "url": url,
    }


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def is_url(text: str) -> bool:
    """Check if a string looks like a URL."""
    text = text.strip()
    return text.startswith(("http://", "https://", "www."))


def is_google_scholar_url(text: str) -> bool:
    """Check if a string is a Google Scholar profile URL."""
    return "scholar.google" in text.lower() and "citations" in text.lower()
