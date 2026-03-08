"""URL handling utilities."""


def normalize_target_url(base_url: str, directory: str) -> str:
    """Join base URL and directory into a clean single target URL."""
    base = base_url.strip().rstrip("/")
    path = directory.strip().strip("/")

    if not base:
        raise ValueError("Website URL cannot be empty.")

    if not path:
        return base

    return f"{base}/{path}"


def extract_hostname(url: str) -> str:
    """Extract hostname from URL."""
    # Remove protocol
    if "://" in url:
        url = url.split("://", 1)[1]
    # Remove path
    if "/" in url:
        url = url.split("/", 1)[0]
    # Remove port if present
    if ":" in url:
        url = url.split(":", 1)[0]
    return url
