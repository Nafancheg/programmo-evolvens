"""Bounded custom-text experiments through the fixed, accepted W0 entry point."""
import argparse
import ctypes
import json
import os
from pathlib import Path
import secrets
import subprocess
import sys
import threading


def validate_text(text):
    if not isinstance(text, str) or len(text.encode('utf-8')) > 256:
        raise ValueError('Text must contain at most 256 UTF-8 bytes')
    return text


def host_free_bytes():
    if sys.platform == 'win32':
        class Memory(ctypes.Structure):
            _fields_ = [('length', ctypes.c_uint32), ('load', ctypes.c_uint32)] + [
                (name, ctypes.c_uint64) for name in ('total', 'available', 'page_total', 'page_available',
                                                   'virtual_total', 'virtual_available', 'extended')]
        memory = Memory()
        memory.length = ctypes.sizeof(memory)
        if not ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(memory)):
            raise OSError('Cannot verify host memory reserve')
        return memory.available
    lines = Path('/proc/meminfo').read_text().splitlines()
    return next(int(line.split()[1]) * 1024 for line in lines if line.startswith('MemAvailable:'))


def command_prefix(distro):
    if sys.platform == 'win32':
        return ['wsl.exe', *(['-d', distro] if distro else []), '--user', 'root', '--exec']
    return ['sudo', '-n'] if os.geteuid() else []


def execute(text, distro=None):
    data = validate_text(text).encode('utf-8')
    if host_free_bytes() < 2 * 1024**3:
        raise RuntimeError('Less than 2 GiB free host RAM; no experiment started')
    prefix = command_prefix(distro)
    options = {'capture_output': True, 'creationflags': getattr(subprocess, 'CREATE_NO_WINDOW', 0)}
    completed = False
    try:
        process = subprocess.run([*prefix, '/usr/bin/timeout', '--signal=KILL', '80s', '/usr/bin/python3',
                                  '-I', '/opt/pe-world/direct.py', 'development', '--text-stdin'],
                                 input=data, timeout=85, **options)
        if len(process.stdout) > 65536:
            raise RuntimeError('Oversized controller response')
        report = json.loads(process.stdout)
        if process.returncode or report.get('outcome') != 'passed':
            raise RuntimeError(report.get('error') or report.get('outcome') or 'Experiment failed')
        completed = True
        return report
    finally:
        if not completed:
            subprocess.run([*prefix, '/usr/bin/python3', '-I', '/opt/pe-world/direct.py', 'cleanup'],
                           timeout=5, **options)


class ExperimentJobs:
    """One bounded action, no queue; input is data, never part of command argv."""
    def __init__(self, runner):
        self.runner = runner
        self.token = secrets.token_urlsafe(24)
        self.lock = threading.Lock()
        self.state = {'status': 'idle'}

    def start(self, text):
        validate_text(text)
        with self.lock:
            if self.state['status'] == 'running':
                raise RuntimeError('An experiment is already running')
            self.state = {'status': 'running'}
        def work():
            try:
                state = {'status': 'completed', 'report': self.runner(text)}
            except Exception as exc:
                state = {'status': 'error', 'error': str(exc)}
            with self.lock:
                self.state = state
        threading.Thread(target=work, daemon=True).start()

    def snapshot(self):
        with self.lock:
            return dict(self.state)


def main():
    sys.stdout.reconfigure(encoding='utf-8')
    from .lab import configured_distro
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--text', required=True)
    parser.add_argument('--distro', default=configured_distro())
    options = parser.parse_args()
    try:
        print(json.dumps(execute(options.text, options.distro), ensure_ascii=False))
    except (OSError, ValueError, RuntimeError, subprocess.SubprocessError) as exc:
        print(json.dumps({'error': str(exc)}, ensure_ascii=False))
        return 1
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
