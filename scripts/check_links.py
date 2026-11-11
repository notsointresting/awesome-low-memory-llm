#!/usr/bin/env python3
"""Check project URLs; intended for scheduled CI, not offline validation."""
import json
import time
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

root = Path(__file__).resolve().parents[1]
entries = json.loads((root / 'data/projects.json').read_text(encoding='utf-8'))
failures = []
for item in entries:
    url = item['url']
    status = None
    try:
        # GET is more portable than HEAD for repository redirects.
        req = Request(url, headers={'User-Agent': 'awesome-low-memory-llm-link-checker/1.0'})
        with urlopen(req, timeout=20) as response:
            status = response.status
    except HTTPError as exc:
        status = exc.code
    except (URLError, TimeoutError, OSError) as exc:
        print(f'WARN {url}: {exc} (network/transient; not failing build)')
        continue
    print(f'{status} {url}')
    if status in (404, 410):
        failures.append(url)
    # Respect GitHub's rate limiting on anonymous requests.
    time.sleep(0.5)
if failures:
    raise SystemExit('Missing repositories: ' + ', '.join(failures))
print('Link check completed.')
