"""Local read-only laboratory dashboard. python -m programmo_evolvens.lab --open"""
import argparse
from collections import deque
import json
import os
from pathlib import Path
import subprocess
import sys
import threading
import time
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlsplit
import webbrowser

STATIC = Path(__file__).resolve().parent / 'lab_ui'
ROOT = Path(__file__).resolve().parent.parent


def configured_distro():
    if os.environ.get('PE_WSL_DISTRO'):
        return os.environ['PE_WSL_DISTRO']
    config = ROOT / '.local/lab.json'
    return json.loads(config.read_text(encoding='utf-8-sig')).get('distro') if config.exists() else None


def observe_command(distro):
    if sys.platform == 'win32':
        return ['wsl.exe', *(['-d', distro] if distro else []), '--user', 'root', '--exec',
                '/usr/bin/python3', '-I', '/opt/pe-world/observe.py']
    return [*(['sudo', '-n'] if os.geteuid() else []), '/usr/bin/python3', '-I', '/opt/pe-world/observe.py']


class Telemetry:
    def __init__(self, command):
        self.command = command
        self.lock = threading.Lock()
        self.stopped = threading.Event()
        self.state = {'available': False, 'error': 'Waiting for WSL telemetry', 'history': []}
        self.history = deque(maxlen=90)
        self.previous = None

    def sample(self):
        try:
            result = subprocess.run(self.command, capture_output=True, timeout=4,
                                    creationflags=getattr(subprocess, 'CREATE_NO_WINDOW', 0))
            if result.returncode or len(result.stdout) > 524288:
                raise RuntimeError('WSL exporter unavailable. Run scripts/setup-lab.ps1.')
            data = json.loads(result.stdout)
            if not data.get('available'):
                raise RuntimeError(data.get('error', 'Telemetry unavailable'))
            cpu = None if data['active'] else 0.0
            if self.previous and data['active_run_id'] and data['active_run_id'] == self.previous['active_run_id']:
                elapsed = data['sample_unix'] - self.previous['sample_unix']
                if elapsed > 0:
                    cpu = max(0, (data['cpu_usec'] - self.previous['cpu_usec']) / elapsed / 10000)
            data['cpu_percent'] = cpu
            self.previous = data.copy()
            self.history.append({'time': data['sample_unix'], 'cpu': cpu, 'memory': data['memory_bytes']})
            data['history'] = list(self.history)
        except (OSError, ValueError, RuntimeError, subprocess.SubprocessError) as exc:
            self.previous = None
            data = {'available': False, 'error': str(exc), 'sample_unix': time.time(), 'history': list(self.history)}
        with self.lock:
            self.state = data

    def run(self):
        while not self.stopped.is_set():
            self.sample()
            self.stopped.wait(2)

    def payload(self):
        with self.lock:
            return json.dumps(self.state, ensure_ascii=False).encode('utf-8')


def make_handler(telemetry):
    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            host = self.headers.get('Host', '')
            allowed = {f'127.0.0.1:{self.server.server_port}', f'localhost:{self.server.server_port}'}
            if host not in allowed or self.headers.get('Origin', 'http://' + host) != 'http://' + host:
                self.send_error(403)
                return
            path = urlsplit(self.path).path
            assets = {'/': ('index.html', 'text/html; charset=utf-8'),
                      '/app.js': ('app.js', 'application/javascript; charset=utf-8'),
                      '/app.css': ('app.css', 'text/css; charset=utf-8')}
            if path == '/api/state':
                body, mime = telemetry.payload(), 'application/json; charset=utf-8'
            elif path in assets:
                filename, mime = assets[path]
                body = (STATIC / filename).read_bytes()
            else:
                self.send_error(404)
                return
            self.send_response(200)
            self.send_header('Content-Type', mime)
            self.send_header('Content-Length', str(len(body)))
            self.send_header('Cache-Control', 'no-store')
            self.send_header('X-Content-Type-Options', 'nosniff')
            self.send_header('Content-Security-Policy', "default-src 'self'; style-src 'self'; script-src 'self'; connect-src 'self'; frame-ancestors 'none'")
            self.end_headers()
            try:
                self.wfile.write(body)
            except (BrokenPipeError, ConnectionResetError):
                pass

        def log_message(self, *args):
            pass
    return Handler


class LocalServer(HTTPServer):
    def get_request(self):
        connection, address = super().get_request()
        connection.settimeout(2)
        return connection, address


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--distro', default=configured_distro())
    parser.add_argument('--port', type=int, default=8765)
    parser.add_argument('--open', action='store_true')
    args = parser.parse_args()
    telemetry = Telemetry(observe_command(args.distro))
    server = LocalServer(('127.0.0.1', args.port), make_handler(telemetry))
    sampler = threading.Thread(target=telemetry.run, daemon=True)
    sampler.start()
    url = f'http://127.0.0.1:{server.server_port}'
    print(f'Programmo Evolvens laboratory: {url}', flush=True)
    if args.open:
        webbrowser.open(url)
    try:
        server.serve_forever(poll_interval=.5)
    except KeyboardInterrupt:
        pass
    finally:
        telemetry.stopped.set()
        server.server_close()
        sampler.join(timeout=5)


if __name__ == '__main__':
    main()
