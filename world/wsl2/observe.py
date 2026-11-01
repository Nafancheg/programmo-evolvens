"""Read-only, bounded laboratory telemetry export. No commands or paths accepted."""
import hashlib
import json
import platform
from pathlib import Path
import time
import zipfile

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


def development_events(path):
    events = []
    if path.is_file() and not path.is_symlink():
        with path.open('rb') as source:
            lines = source.read(131072).splitlines()
        for line in lines:
            try:
                event = json.loads(line)
            except ValueError:
                continue
            if (isinstance(event, dict) and event.get('type') == 'heartbeat'
                    and isinstance(event.get('development'), dict)):
                events.append(event['development'])
    return events[:96]


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
    development = None
    candidate = next((run for run in runs if run.get('probe') == 'development'), None)
    if candidate:
        stream = Path(candidate['source']).with_suffix('.stdout')
        development = {'run_id': candidate['id'], 'source': str(stream),
                       'bundle_sha256': candidate.get('probe_sha256'), 'completed': candidate['completed'],
                       'result': candidate.get('result'), 'events': development_events(stream)}
        bundle = ASSETS / 'development.pyz'
        if bundle.is_file() and not bundle.is_symlink() and bundle.stat().st_size <= 262144:
            if hashlib.sha256(bundle.read_bytes()).hexdigest() == development['bundle_sha256']:
                with zipfile.ZipFile(bundle) as archive:
                    development['genome'] = json.loads(archive.read('programmo_evolvens/development_genome.json'))
                    development['source_code'] = {}
                    for name in ('development.py', 'runtime.py'):
                        data = archive.read('programmo_evolvens/' + name)
                        development['source_code'][name] = {'text': data.decode('utf-8'),
                                                            'sha256': hashlib.sha256(data).hexdigest()}
    return {'sample_unix': time.time(), 'available': True, 'policy': policy,
            'active': active, 'active_run_id': active_run,
            'memory_bytes': number('memory.current'), 'tasks': number('pids.current'),
            'cpu_usec': int(stats.get('usage_usec', 0)), 'runs': runs,
            'development': development,
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
