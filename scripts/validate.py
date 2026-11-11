#!/usr/bin/env python3
"""Validate basic consistency of the curated project catalog (stdlib only)."""
import json
from pathlib import Path
from urllib.parse import urlparse

root = Path(__file__).resolve().parents[1]
entries = json.loads((root / 'data/projects.json').read_text(encoding='utf-8'))
readme = (root / 'README.md').read_text(encoding='utf-8')
assert isinstance(entries, list) and entries, 'Catalog must contain entries'
seen_names, seen_urls = set(), set()
for item in entries:
    assert {'name', 'url', 'category', 'hardware', 'note', 'evidence'} <= item.keys(), item
    assert item['name'] not in seen_names, f"Duplicate name: {item['name']}"
    assert item['url'] not in seen_urls, f"Duplicate URL: {item['url']}"
    assert urlparse(item['url']).scheme == 'https', item['url']
    assert urlparse(item['url']).hostname == 'github.com', item['url']
    assert item['url'] in readme, f"Not linked in README: {item['name']}"
    assert isinstance(item['hardware'], list) and len(item['hardware']) > 0
    assert item['evidence'] in {'documentation', 'project-reported', 'community-reported', 'independently-reproduced'}
    seen_names.add(item['name'])
    seen_urls.add(item['url'])
print(f'Validated {len(entries)} catalog entries and their README links.')
