import json
import threading
import time
from types import SimpleNamespace
import unittest
from unittest.mock import patch

from programmo_evolvens.experiment import ExperimentJobs, execute, validate_text


class ExperimentTests(unittest.TestCase):
    def test_text_limit_counts_utf8_bytes(self):
        self.assertEqual(validate_text(''), '')
        self.assertEqual(validate_text('x'*256), 'x'*256)
        for text in ('x'*257, '\u0430'*129, None):
            with self.subTest(text_type=type(text).__name__), self.assertRaises(ValueError):
                validate_text(text)

    def test_text_is_stdin_data_and_never_command_arguments(self):
        text = '  NEW; $(data)  '
        reply = SimpleNamespace(returncode=0, stdout=b'{"outcome":"passed"}')
        with patch('programmo_evolvens.experiment.host_free_bytes', return_value=3*1024**3), \
             patch('programmo_evolvens.experiment.command_prefix', return_value=['fixed-root']), \
             patch('programmo_evolvens.experiment.subprocess.run', return_value=reply) as run:
            self.assertEqual(execute(text)['outcome'], 'passed')
            arguments = run.call_args_list[0]
            self.assertNotIn(text, arguments.args[0])
            self.assertEqual(arguments.kwargs['input'], text.encode('utf-8'))
            self.assertFalse(arguments.kwargs.get('shell', False))

    def test_low_host_reserve_refuses_before_process_creation(self):
        with patch('programmo_evolvens.experiment.host_free_bytes', return_value=0), \
             patch('programmo_evolvens.experiment.subprocess.run') as run:
            with self.assertRaisesRegex(RuntimeError, 'free host RAM'):
                execute('text')
            run.assert_not_called()

    def test_only_one_job_can_run_without_a_queue(self):
        started, release = threading.Event(), threading.Event()
        def runner(text):
            started.set()
            release.wait(1)
            return {'text': text}
        jobs = ExperimentJobs(runner)
        jobs.start('one')
        self.assertTrue(started.wait(1))
        with self.assertRaisesRegex(RuntimeError, 'already running'):
            jobs.start('two')
        release.set()
        end = time.monotonic()+1
        while jobs.snapshot()['status']=='running' and time.monotonic()<end:
            time.sleep(.01)
        self.assertEqual(jobs.snapshot(), {'status':'completed','report':{'text':'one'}})
