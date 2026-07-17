import httpx
from django.conf import settings


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
