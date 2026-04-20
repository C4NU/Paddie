import json
import urllib.request
import webbrowser
from dataclasses import dataclass

from packaging.version import InvalidVersion, Version


CURRENT_VERSION = "3.4.1"
LATEST_RELEASE_API_URL = "https://api.github.com/repos/C4NU/Paddie/releases/latest"


@dataclass
class ReleaseInfo:
    version: str
    html_url: str


def fetch_latest_release(timeout=5):
    request = urllib.request.Request(
        LATEST_RELEASE_API_URL,
        headers={
            "Accept": "application/vnd.github+json",
            "User-Agent": "Paddie",
        },
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        payload = json.loads(response.read().decode("utf-8"))

    return ReleaseInfo(
        version=normalize_version(payload.get("tag_name", "")),
        html_url=payload.get("html_url", ""),
    )


def has_newer_release(latest_version, current_version=CURRENT_VERSION):
    try:
        return Version(normalize_version(latest_version)) > Version(normalize_version(current_version))
    except InvalidVersion:
        return False


def normalize_version(version):
    return version.strip().lstrip("vV")


def open_release_page(release_info):
    if release_info.html_url:
        webbrowser.open(release_info.html_url)
