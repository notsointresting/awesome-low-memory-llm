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

# Evidence guard: numeric hardware claims require source-attributed report records.
for item in entries:
    profile = item.get('profile', {})
    for report in profile.get('reports', []):
        assert report.get('evidence') == 'author-reported', (item['name'], 'unattributed report')
        source = report.get('source')
        assert isinstance(source, str) and source.startswith('https://'), (item['name'], 'report source required')
        for key in ('system_ram_gb', 'peak_ram_gb', 'peak_vram_gb', 'disk_gb', 'tokens_per_second'):
            val = report.get(key)
            assert val is None or (type(val) in (float, int) and val >= 0), (item['name'], key)
print('Hardware evidence records have source URLs and valid numeric units.')

# Only reviewed submissions may enter the accepted benchmark index.
community_path = root / 'data/community-benchmarks.json'
if community_path.exists():
    community = json.loads(community_path.read_text(encoding='utf-8'))
    assert isinstance(community, list), 'community benchmark index must be an array'
    for result in community:
        assert result.get('status') == 'reviewed', 'Unreviewed candidate cannot be published'
        assert result.get('source_url', '').startswith('https://'), 'Accepted result needs source'
        assert result.get('reviewed_on'), 'Accepted result needs a review date'
print('Accepted community benchmark index validated.')
