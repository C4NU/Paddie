import http.client
import json
import ssl
import urllib.parse
import webbrowser
from dataclasses import dataclass

from packaging.version import InvalidVersion, Version


CURRENT_VERSION = "3.4.1"
LATEST_RELEASE_HOST = "api.github.com"
LATEST_RELEASE_PATH = "/repos/C4NU/Paddie/releases/latest"
MAX_RESPONSE_BYTES = 1024 * 1024


@dataclass
class ReleaseInfo:
    version: str
    html_url: str


def fetch_latest_release(timeout=5):
    context = ssl.create_default_context()
    connection = http.client.HTTPSConnection(
        LATEST_RELEASE_HOST,
        timeout=timeout,
        context=context,
    )
    try:
        connection.request(
            "GET",
            LATEST_RELEASE_PATH,
            headers={
                "Accept": "application/vnd.github+json",
                "User-Agent": "Paddie",
            },
        )
        response = connection.getresponse()
        if response.status >= 400:
            raise RuntimeError(f"GitHub API returned HTTP {response.status}")

        payload = json.loads(response.read(MAX_RESPONSE_BYTES).decode("utf-8"))
    finally:
        connection.close()

    return ReleaseInfo(
        version=normalize_version(payload.get("tag_name", "")),
        html_url=payload.get("html_url", ""),
    )


def has_newer_release(latest_version, current_version=CURRENT_VERSION):
    try:
        latest = Version(normalize_version(latest_version))
        current = Version(normalize_version(current_version))
        return latest > current
    except InvalidVersion:
        return False


def normalize_version(version):
    return version.strip().lstrip("vV")


def open_release_page(release_info):
    if is_trusted_release_url(release_info.html_url):
        webbrowser.open(release_info.html_url)


def is_trusted_release_url(url):
    parsed_url = urllib.parse.urlparse(url)
    return (
        parsed_url.scheme == "https"
        and parsed_url.netloc.lower() == "github.com"
        and parsed_url.path.startswith("/C4NU/Paddie/releases/")
    )
