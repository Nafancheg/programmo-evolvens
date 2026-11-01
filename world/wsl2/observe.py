"""Read-only, bounded laboratory telemetry export. No commands or paths accepted."""
import hashlib
import json
import platform
from pathlib import Path
import time

ASSETS = Path('/opt/pe-world')
RUNS = Path('/var/lib/pe-world/runs')
GROUP = Path('/sys/fs/cgroup/pe-world-current-v0/worker')


def read_json(path, limit=262144):
    if path.is_symlink() or not path.is_file() or path.stat().st_size > limit:
        raise ValueError('unsafe or oversized telemetry file')
    return json.loads(path.read_bytes())


def number(name):
    try:
        return int((GROUP / name).read_text().strip())
    except FileNotFoundError:
        return 0


def applies(acceptance, current, suite_hash):
    if not acceptance or not acceptance.get('accepted') or acceptance.get('suite_sha256') != suite_hash:
        return False
    cases = [case for case in acceptance.get('cases', {}).values() if 'controller_sha256' in case]
    return bool(cases) and all(all(case.get(key) == value for key, value in current.items()) for case in cases)


def snapshot():
    policy = read_json(ASSETS / 'policy.json')
    candidates = sorted(RUNS.parent.glob('acceptance-*.json'), reverse=True)[:16]
    acceptance = None
    accepted_ids = set()
    for path in candidates:
        value = read_json(path)
        if value.get('accepted'):
            if acceptance is None:
                acceptance = value
            accepted_ids.update(case['run_id'] for case in value['cases'].values() if 'run_id' in case)
            for case in value['cases'].values():
                accepted_ids.update(Path(name).stem for name in case.get('interrupted_journals', []))
    current = {key: hashlib.sha256((ASSETS / filename).read_bytes()).hexdigest() for key, filename in
               (('controller_sha256', 'direct.py'), ('shared_controller_sha256', 'controller.py'), ('policy_sha256', 'policy.json'),
                ('seccomp_sha256', 'seccomp.bpf'), ('rootfs_manifest_sha256', 'rootfs.manifest.json'))}
    current['kernel_release'] = platform.release()
    applicable = applies(acceptance, current, hashlib.sha256((ASSETS / 'acceptance.py').read_bytes()).hexdigest())
    files = list(RUNS.glob('*.jsonl'))
    for folder in sorted((RUNS / 'history').glob('*'), reverse=True)[:4]:
        if folder.is_dir() and not folder.is_symlink():
            files.extend(folder.glob('*.jsonl'))
    files = sorted(files, key=lambda p: p.stat().st_mtime, reverse=True)[:80]
    runs = []
    for path in files:
        if path.is_symlink() or path.stat().st_size > 65536:
            continue
        events = [json.loads(line) for line in path.read_bytes().splitlines() if line]
        if not events:
            continue
        merged = dict(events[0])
        for event in events[1:]:
            merged.update(event)
        merged['id'] = path.stem
        merged['source'] = str(path)
        merged['completed'] = any(event.get('event') == 'finish' for event in events)
        merged['expected_test_pass'] = path.stem in accepted_ids
        runs.append(merged)
    active = GROUP.exists() and 'populated 1' in (GROUP / 'cgroup.events').read_text()
    stats = {}
    if GROUP.exists():
        stats = dict(line.split() for line in (GROUP / 'cpu.stat').read_text().splitlines())
    active_run = next((r['id'] for r in runs if not r['completed']), None) if active else None
    if active_run:
        for run in runs:
            if run['id'] == active_run:
                run['outcome'] = 'running'
    return {'sample_unix': time.time(), 'available': True, 'policy': policy,
            'active': active, 'active_run_id': active_run,
            'memory_bytes': number('memory.current'), 'tasks': number('pids.current'),
            'cpu_usec': int(stats.get('usage_usec', 0)), 'runs': runs,
            'acceptance': {'accepted': applicable, 'previous_report_exists': bool(acceptance),
                           'profile': (acceptance or {}).get('profile'),
                           'finished_unix': (acceptance or {}).get('finished_unix'),
                           'cases': list((acceptance or {}).get('cases', {})),
                           'source': str(next((p for p in candidates if acceptance and read_json(p).get('accepted')), ''))},
            'kernel': Path('/proc/sys/kernel/osrelease').read_text().strip()}


if __name__ == '__main__':
    try:
        print(json.dumps(snapshot()))
    except (OSError, ValueError, KeyError) as exc:
        print(json.dumps({'available': False, 'error': str(exc), 'sample_unix': time.time()}))
