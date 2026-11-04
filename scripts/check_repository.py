"""Check repository evidence and layout without contacting any model."""
import ast
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    # Parse source without importing scripts or calling models.
    sources = [p for p in ROOT.rglob('*.py') if '.git' not in p.parts]
    for path in sources:
        ast.parse(path.read_text(encoding='utf-8'), filename=str(path))

    dataset = ROOT / 'data/baseline_dev.jsonl'
    cases = [json.loads(line) for line in dataset.read_text().splitlines() if line.strip()]
    assert cases, 'Active development dataset is empty'
    ids = set()
    for case in cases:
        assert isinstance(case.get('id'), str) and case['id'], 'Missing case ID'
        assert case['id'] not in ids, 'Duplicate active case ID: ' + case['id']
        ids.add(case['id'])
        assert case.get('label') in ('benign', 'attack'), 'Invalid active label'
        assert isinstance(case.get('prompt'), str) and case['prompt'].strip(), 'Empty prompt'

    snapshot = ROOT / 'logs/baseline_dev_2026-11-04.jsonl'
    expected = 'e18641021a86a4e669c0e425803a7f9507dc88e94d52cca20ee90e64ac27ad5f'
    assert digest(snapshot) == expected, 'Real baseline snapshot hash changed'
    records = [json.loads(line) for line in snapshot.read_text().splitlines() if line.strip()]
    assert len(records) == 4, 'Expected four preserved baseline records'
    assert len({r['case_id'] for r in records}) == 4
    assert all(r['config'] == 'target_only' for r in records)

    # Validate current navigation links; archives retain historical references.
    docs = [ROOT / 'README.md', ROOT / 'CONTRIBUTING.md']
    for folder in ('docs', 'defenses', 'experiments', 'contributions'):
        docs.extend((ROOT / folder).rglob('*.md'))
    for path in docs:
        for target in re.findall(r'\[[^\]]*\]\(([^)]+)\)', path.read_text(encoding='utf-8')):
            target = target.split('#', 1)[0]
            if not target or '://' in target or target.startswith('mailto:'):
                continue
            assert (path.parent / target).exists(), f'Broken link in {path.relative_to(ROOT)}: {target}'

    result = subprocess.run(
        [sys.executable, 'snapshots/initial/harness.py', 'verify', '--out', 'runs/fallback_sanity'],
        cwd=ROOT, text=True, capture_output=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    print(result.stdout.strip())
    print(f'PASS: {len(sources)} Python files, {len(cases)} active cases, navigation links, and real snapshot integrity.')
    print('No model requests or research-metric calculations were performed.')


if __name__ == '__main__':
    main()
