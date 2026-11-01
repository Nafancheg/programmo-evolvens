import json
from pathlib import Path
import tempfile
import threading
import unittest
from types import SimpleNamespace
from urllib.error import HTTPError
from urllib.request import Request, urlopen
from unittest.mock import patch

from programmo_evolvens.lab import LocalServer, Telemetry, make_handler
from world.wsl2.observe import applies, development_events


class LabTelemetryTests(unittest.TestCase):
    def test_event_reader_excludes_result_snapshot_and_incomplete_line(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory)/'record.stdout'
            event = {'event': 'initial', 'seq': 0}
            path.write_text(json.dumps({'type': 'heartbeat', 'development': event})+'\n'+
                            json.dumps({'type': 'result', 'development': {'cells': []}})+'\n'+
                            '{"type":', encoding='utf-8')
            self.assertEqual(development_events(path), [event])

    def test_old_world_report_does_not_accept_different_components(self):
        current = {'controller_sha256': 'controller', 'policy_sha256': 'policy'}
        report = {'accepted': True, 'suite_sha256': 'suite', 'cases': {'memory': dict(current)}}
        self.assertTrue(applies(report, current, 'suite'))
        self.assertFalse(applies(None, current, 'suite'))
        self.assertFalse(applies(report, dict(current, policy_sha256='changed'), 'suite'))
        self.assertFalse(applies(report, current, 'different-suite'))
        self.assertFalse(applies(dict(report, cases={}), current, 'suite'))

    def test_cpu_uses_external_deltas_and_new_run_has_no_estimate(self):
        telemetry = Telemetry(['fixed-exporter'])
        value = {'available': True, 'active': True, 'active_run_id': 'one', 'sample_unix': 10,
                 'cpu_usec': 1000000, 'memory_bytes': 20}
        def sample():
            with patch('programmo_evolvens.lab.subprocess.run', return_value=SimpleNamespace(returncode=0, stdout=json.dumps(value).encode())):
                telemetry.sample()
            return json.loads(telemetry.payload())
        self.assertIsNone(sample()['cpu_percent'])
        value.update(sample_unix=12, cpu_usec=2000000)
        self.assertEqual(sample()['cpu_percent'], 50)
        value.update(active_run_id='two', sample_unix=14, cpu_usec=10)
        self.assertIsNone(sample()['cpu_percent'])

    def test_source_failure_is_explicit_without_fabricated_zero_metrics(self):
        telemetry = Telemetry(['fixed-exporter'])
        with patch('programmo_evolvens.lab.subprocess.run', side_effect=OSError('WSL unavailable')):
            telemetry.sample()
        result = json.loads(telemetry.payload())
        self.assertFalse(result['available'])
        self.assertNotIn('cpu_percent', result)
        self.assertNotIn('memory_bytes', result)


class LabHttpTests(unittest.TestCase):
    def setUp(self):
        self.telemetry = Telemetry([])
        self.server = LocalServer(('127.0.0.1', 0), make_handler(self.telemetry))
        self.thread = threading.Thread(target=lambda: self.server.serve_forever(poll_interval=.01), daemon=True)
        self.thread.start()
        self.url = f'http://127.0.0.1:{self.server.server_port}'

    def tearDown(self):
        self.server.shutdown()
        self.server.server_close()
        self.thread.join(timeout=2)

    def test_dashboard_and_json_serve_with_no_cache_and_csp(self):
        with urlopen(self.url + '/api/state', timeout=2) as response:
            self.assertFalse(json.load(response)['available'])
            self.assertEqual(response.headers['Cache-Control'], 'no-store')
            self.assertIn("frame-ancestors 'none'", response.headers['Content-Security-Policy'])
        with urlopen(self.url, timeout=2) as response:
            self.assertIn(b'PROGRAMMO EVOLVENS', response.read())

    def test_foreign_host_and_origin_are_rejected(self):
        for headers in ({'Host': 'attacker.invalid'}, {'Origin': 'http://attacker.invalid'}):
            with self.subTest(headers=headers), self.assertRaises(HTTPError) as error:
                urlopen(Request(self.url+'/api/state', headers=headers), timeout=2)
            self.assertEqual(error.exception.code, 403)
            error.exception.close()

    def test_no_execution_endpoint_or_filesystem_traversal(self):
        for request, code in ((Request(self.url+'/api/run', data=b'{}'), 501),
                              (Request(self.url+'/../world/wsl2/policy.json'), 404)):
            with self.subTest(url=request.full_url), self.assertRaises(HTTPError) as error:
                urlopen(request, timeout=2)
            self.assertEqual(error.exception.code, code)
            error.exception.close()

    def test_specimen_and_sources_come_from_saved_instance(self):
        self.telemetry.state = {'development': {'run_id': 'saved-run', 'completed': True,
            'bundle_sha256': 'bundle', 'source': 'journal.stdout',
            'genome': {'schema': 'development-v0'},
            'source_code': {'development.py': {'text': '# saved source', 'sha256': 'source'}},
            'result': {'development': {'cells': [], 'value': 'saved-result'}, 'cases': [], 'scope': 'prescribed'}}}
        with urlopen(self.url+'/api/organism?download=1', timeout=2) as response:
            result = json.load(response)
            self.assertEqual(result['organism']['value'], 'saved-result')
            self.assertIn('attachment;', response.headers['Content-Disposition'])
        with urlopen(self.url+'/source/development.py', timeout=2) as response:
            self.assertEqual(response.read(), b'# saved source')
        with urlopen(self.url+'/source/genome.json', timeout=2) as response:
            self.assertEqual(json.load(response), {'schema': 'development-v0'})
