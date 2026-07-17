from pathlib import Path

import httpx
from django.conf import settings
from pypdf import PdfReader

# Extensions the file_read tool is allowed to open.
ALLOWED_FILE_EXTENSIONS = {".txt", ".pdf"}


def web_search(query: str) -> list[dict]:
    """Search the web with Google (via SerpAPI) and return the top results.

    Use this whenever you need up-to-date facts, current events, documentation,
    prices, or anything you are not certain about from memory.

    Args:
        query: The search query, e.g. "latest Django LTS release".

    Returns:
        A list of result dicts, each with "title", "link" and "snippet".
    """
    url = "https://serpapi.com/search"
    params = {
        "q": query,
        "engine": "google",
        "num": 5,
        "api_key": settings.SERPAPI_API_KEY,
    }

    try:
        response = httpx.get(url, params=params, timeout=20.0)
        response.raise_for_status()
    except httpx.HTTPError as exc:
        return [{"title": "Search error", "link": "", "snippet": str(exc)}]

    data = response.json()

    if data.get("error"):
        return [{"title": "Search error", "link": "", "snippet": data["error"]}]

    results = []
    for item in data.get("organic_results", [])[:5]:
        results.append(
            {
                "title": item.get("title"),
                "link": item.get("link"),
                "snippet": item.get("snippet"),
            }
        )
    return results


def read_file(filename: str) -> str:
    """Read the text contents of a .txt or .pdf file from the shared file directory.

    Use this when the user refers to a document or report they have placed in
    the shared file directory and you need its contents to answer.

    Args:
        filename: The file's name, e.g. "notes.txt" or "report.pdf". Must be a
            plain file name relative to the shared file directory (no ".." or
            absolute paths).

    Returns:
        The extracted text content of the file, or an "Error: ..." message if
        the file cannot be read.
    """
    root = Path(settings.MEDIA_ROOT).resolve()
    requested = Path(filename)

    if requested.is_absolute() or ".." in requested.parts:
        return "Error: only file names within the shared file directory are allowed."

    candidate = (root / requested).resolve()
    try:
        candidate.relative_to(root)
    except ValueError:
        return "Error: access outside the shared file directory is not allowed."

    if candidate.suffix.lower() not in ALLOWED_FILE_EXTENSIONS:
        return f"Error: only {', '.join(sorted(ALLOWED_FILE_EXTENSIONS))} files can be read."

    if not candidate.is_file():
        return f"Error: file '{filename}' was not found."

    try:
        if candidate.suffix.lower() == ".pdf":
            reader = PdfReader(str(candidate))
            text = "\n".join(page.extract_text() or "" for page in reader.pages)
        else:
            text = candidate.read_text(encoding="utf-8", errors="replace")
    except Exception as exc:
        return f"Error reading '{filename}': {exc}"

    return text.strip()
