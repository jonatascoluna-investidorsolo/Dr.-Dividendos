from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
from typing import Iterable


@dataclass(frozen=True)
class Endpoint:
    name: str
    url: str


def check_endpoint(endpoint: Endpoint, timeout: int = 10) -> tuple[bool, str]:
    try:
        req = Request(endpoint.url, method="HEAD", headers={"User-Agent": "DoutorDosDividendos/1.3"})
        with urlopen(req, timeout=timeout) as response:
            return True, f"HTTP {response.status}"
    except HTTPError as exc:
        # A 403/405 still proves DNS/TCP/HTTP reachability; caller can decide whether auth is required.
        if exc.code in {401, 403, 405}:
            return True, f"HTTP {exc.code} (endpoint reachable; access/method restricted)"
        return False, f"HTTP {exc.code}"
    except (URLError, TimeoutError) as exc:
        return False, f"{type(exc).__name__}: {exc}"


def check_sources(endpoints: Iterable[Endpoint], timeout: int = 10) -> dict[str, dict[str, str | bool]]:
    checked = datetime.now(timezone.utc).isoformat()
    out: dict[str, dict[str, str | bool]] = {}
    for endpoint in endpoints:
        ok, detail = check_endpoint(endpoint, timeout=timeout)
        out[endpoint.name] = {"reachable": ok, "detail": detail, "checked_at": checked, "url": endpoint.url}
    return out
