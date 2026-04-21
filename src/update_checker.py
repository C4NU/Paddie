import json
import urllib.parse
import webbrowser
from dataclasses import dataclass

import requests
from packaging.version import InvalidVersion, Version


CURRENT_VERSION = "3.4.1"
LATEST_RELEASE_API_URL = (
    "https://api.github.com/repos/C4NU/Paddie/releases/latest"
)


@dataclass
class ReleaseInfo:
    version: str
    html_url: str


def fetch_latest_release(timeout=5):
    response = requests.get(
        LATEST_RELEASE_API_URL,
        headers={
            "Accept": "application/vnd.github+json",
            "User-Agent": "Paddie",
        },
        timeout=timeout,
        allow_redirects=False,
    )
    response.raise_for_status()
    payload = json.loads(response.text)

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
