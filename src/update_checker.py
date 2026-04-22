import json
import urllib.parse
import webbrowser
from dataclasses import dataclass

from packaging.version import InvalidVersion, Version
from PySide6.QtCore import (
    QCoreApplication,
    QEventLoop,
    QTimer,
    QUrl,
)
from PySide6.QtNetwork import QNetworkAccessManager, QNetworkReply, QNetworkRequest


CURRENT_VERSION = "3.4.1"
LATEST_RELEASE_API_URL = (
    "https://api.github.com/repos/C4NU/Paddie/releases/latest"
)
_QT_APPLICATION = None


@dataclass
class ReleaseInfo:
    version: str
    html_url: str


def fetch_latest_release(timeout=5):
    ensure_qt_application()
    manager = QNetworkAccessManager()
    request = QNetworkRequest(QUrl(LATEST_RELEASE_API_URL))
    request.setRawHeader(b"Accept", b"application/vnd.github+json")
    request.setRawHeader(b"User-Agent", b"Paddie")
    request.setMaximumRedirectsAllowed(0)

    reply = manager.get(request)
    event_loop = QEventLoop()
    timeout_timer = QTimer()
    timeout_timer.setSingleShot(True)
    timeout_timer.timeout.connect(event_loop.quit)
    reply.finished.connect(event_loop.quit)

    timeout_timer.start(int(timeout * 1000))
    event_loop.exec()

    if timeout_timer.isActive():
        timeout_timer.stop()
    else:
        reply.abort()
        reply.deleteLater()
        raise TimeoutError("GitHub release request timed out.")

    if reply.error() != QNetworkReply.NetworkError.NoError:
        error_message = reply.errorString()
        reply.deleteLater()
        raise RuntimeError(error_message)

    payload = json.loads(bytes(reply.readAll()).decode("utf-8"))
    reply.deleteLater()

    return ReleaseInfo(
        version=normalize_version(payload.get("tag_name", "")),
        html_url=payload.get("html_url", ""),
    )


def ensure_qt_application():
    global _QT_APPLICATION
    if QCoreApplication.instance() is None:
        _QT_APPLICATION = QCoreApplication([])


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
