"""Validate fixed course structure; does not certify experiments."""
from pathlib import Path
import re

root = Path(__file__).resolve().parents[1]
weeks = sorted((root / 'curriculum/weeks').glob('week-*'))
assert len(weeks) == 24, len(weeks)
count = 0
for i, week in enumerate(weeks, 1):
    assert week.name == f'week-{i:02d}'
    assert (week / 'README.md').is_file()
    days = sorted(week.glob('day-*/README.md'))
    assert len(days) == 5, week
    for d, path in enumerate(days, 1):
        text = path.read_text(encoding='utf-8')
        assert text.startswith(f'# W{i:02d}D{d:02d}'), path
        assert len(re.findall(r'^\d\. \*\*問：', text, re.M)) == 2, path
        for heading in ['逐步實作', '驗收與除錯', '精簡中文複習', '官方參考']:
            assert heading in text, (path, heading)
        count += 1
for path in root.rglob('*.md'):
    for target in re.findall(r'\]\(([^)]+)\)', path.read_text(encoding='utf-8')):
        if '://' in target or target.startswith('#'):
            continue
        assert (path.parent / target.split('#')[0]).exists(), (path, target)
progress = (root / 'PROGRESS.md').read_text(encoding='utf-8')
assert len(re.findall(r'^\| \[W\d{2}D\d{2}\]', progress, re.M)) == 120
assert not list((root / 'curriculum').glob('stage-*.md'))
print(f'PASS: {len(weeks)} weeks, {count} days, 240 Q&A, local links, progress rows, no legacy stages')
