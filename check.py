import json
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone

SITES = [
    {"name": "GitHub", "url": "https://github.com"},
    {"name": "Wikipedia", "url": "https://www.wikipedia.org"},
    {"name": "Cloudflare", "url": "https://www.cloudflare.com"},
    {"name": "Python.org", "url": "https://www.python.org"},
]


def check_site(site):
    req = urllib.request.Request(
        site["url"],
        headers={"User-Agent": "Mozilla/5.0 (compatible; CloudUptimeMonitor/1.0)"},
    )
    start = time.perf_counter()
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            latency_ms = round((time.perf_counter() - start) * 1000)
            return {
                "name": site["name"],
                "url": site["url"],
                "online": True,
                "status_code": response.getcode(),
                "latency_ms": latency_ms,
            }
    except urllib.error.HTTPError as e:
        latency_ms = round((time.perf_counter() - start) * 1000)
        return {
            "name": site["name"],
            "url": site["url"],
            "online": False,
            "status_code": e.code,
            "latency_ms": latency_ms,
        }
    except Exception:
        latency_ms = round((time.perf_counter() - start) * 1000)
        return {
            "name": site["name"],
            "url": site["url"],
            "online": False,
            "status_code": 0,
            "latency_ms": latency_ms,
        }


def main():
    results = [check_site(site) for site in SITES]
    payload = {
        "last_updated": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC"),
        "runner": "GitHub Actions (ubuntu-latest)",
        "sites": results,
    }
    with open("status.json", "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)


if __name__ == "__main__":
    main()