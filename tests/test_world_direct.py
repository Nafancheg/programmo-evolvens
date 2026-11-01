import sys
import hashlib
import json
import tempfile
from pathlib import Path
from types import SimpleNamespace
import unittest
from unittest.mock import patch

if sys.platform == "linux":
    from world.wsl2 import direct


@unittest.skipUnless(sys.platform == "linux", "direct cgroup backend is Linux-only")
class DirectWorldTests(unittest.TestCase):
    def test_custom_input_is_bounded_data_for_development_only(self):
        self.assertEqual(json.loads(direct.request_bytes(1, 'development', '  OTHER  '))['payload'], {'text':'  OTHER  '})
        self.assertEqual(json.loads(direct.request_bytes(1, 'development', ''))['payload'], {'text':''})
        for mode,text in (('smoke','data'),('development','x'*257)):
            with self.subTest(mode=mode), self.assertRaises(ValueError):
                direct.request_bytes(1,mode,text)

    def test_development_requires_matching_accepted_runtime(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            archive = root / 'runs'
            archive.mkdir()
            (root/'acceptance.py').write_text('trusted fixed suite')
            module = SimpleNamespace(trusted_tree=lambda _: True, digest=lambda data: hashlib.sha256(data).hexdigest())
            required = {'memory', 'output', 'line', 'protocol', 'hang', 'closed-pipes', 'permissions',
                        'inspect', 'cpu', 'deadline', 'pids', 'controller-death-and-concurrency', 'recovery'}
            identity = {'controller_sha256': 'one'}
            record = {'accepted': True, 'profile': 'existing-wsl-serial-single-thread-v0',
                      'suite_sha256': module.digest((root/'acceptance.py').read_bytes()),
                      'cases': {name: dict(identity) for name in required}}
            path = root/'acceptance-1.json'
            path.write_text(json.dumps(record))
            with patch.object(direct, 'ASSETS', root), patch.object(direct, 'ARCHIVE', archive), \
                 patch.object(direct, 'shared', return_value=module), \
                 patch.object(direct, 'runtime_identity', return_value=identity):
                self.assertEqual(direct.require_acceptance()['source'], str(path))
                record['cases']['memory']['controller_sha256'] = 'older'
                path.write_text(json.dumps(record))
                with self.assertRaisesRegex(RuntimeError, 'current W0 acceptance required'):
                    direct.require_acceptance()
                path.unlink()
                with self.assertRaisesRegex(RuntimeError, 'current W0 acceptance required'):
                    direct.require_acceptance()

    def test_rejected_admission_never_prepares_world_or_starts_candidate(self):
        with tempfile.TemporaryDirectory() as directory:
            module = direct.shared()
            original = module.trusted_tree
            module.trusted_tree = lambda _: True
            try:
                with patch.object(direct, 'ARCHIVE', Path(directory)), \
                     patch.object(direct, 'preflight', return_value=[]), \
                     patch.object(direct, 'shared', return_value=module), \
                     patch.object(direct.pwd, 'getpwnam', return_value=None), \
                     patch.object(direct, 'require_acceptance', side_effect=RuntimeError('not accepted')), \
                     patch.object(direct, 'prepare_groups') as prepare, \
                     patch.object(direct.subprocess, 'Popen') as launch:
                    with self.assertRaisesRegex(RuntimeError, 'not accepted'):
                        direct.run(1, 'development')
                    prepare.assert_not_called()
                    launch.assert_not_called()
            finally:
                module.trusted_tree = original

    def test_private_path_guard_rejects_root_and_foreign_group(self):
        for path in (direct.CGROOT, direct.CGROOT / "docker", direct.BASE / "other"):
            with self.subTest(path=path), self.assertRaises(RuntimeError):
                direct.assert_private_path(path)
        direct.assert_private_path(direct.BASE / "worker")

    def test_limits_are_checked_against_kernel_style_files(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory)
            expected = {"memory.max": "268435456", "cpu.max": "100000 100000"}
            for name, value in expected.items():
                (path / name).write_text(value + "\n")
            direct.check_limits(path, expected)
            (path / "memory.max").write_text("max\n")
            with self.assertRaisesRegex(RuntimeError, "kernel did not enforce"):
                direct.check_limits(path, expected)

    def test_existing_group_is_not_overwritten(self):
        with patch.object(Path, "exists", return_value=True):
            with self.assertRaisesRegex(RuntimeError, "already exists"):
                direct.prepare_groups()

    def test_cleanup_does_not_kill_an_active_controller(self):
        with patch.object(direct.os, "geteuid", return_value=0), \
             patch.object(Path, "exists", return_value=True), \
             patch.object(direct, "members", return_value=[123]), \
             patch.object(direct, "kill_worker") as kill:
            with self.assertRaisesRegex(RuntimeError, "still running"):
                direct.cleanup()
            kill.assert_not_called()

    def test_unknown_workload_is_rejected_before_launch(self):
        with patch.object(direct, "preflight", return_value=[]), \
             patch.object(direct.subprocess, "Popen") as launch:
            with self.assertRaisesRegex(RuntimeError, "fixed trusted probes"):
                direct.run(1, "/tmp/unknown.py")
            launch.assert_not_called()

    def test_full_archive_refuses_before_creating_cgroups(self):
        with tempfile.TemporaryDirectory() as directory:
            archive = Path(directory)
            for number in range(16):
                (archive / f"{number}.jsonl").touch()
            with patch.object(direct, "ARCHIVE", archive), \
                 patch.object(direct, "preflight", return_value=[]), \
                 patch.object(direct.pwd, "getpwnam", return_value=None), \
                 patch.object(direct, "prepare_groups") as prepare, \
                 patch.object(direct.subprocess, "Popen") as launch:
                with self.assertRaisesRegex(RuntimeError, "archive is full"):
                    direct.run(1, "smoke")
                prepare.assert_not_called()
                launch.assert_not_called()

    def test_controller_origin_accepts_systemd_scope_and_rejects_escape(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            (root / "init.scope").mkdir()
            for raw, valid in (("0::/init.scope", True), ("0::/../../outside", False)):
                with self.subTest(raw=raw), patch.object(direct, "CGROOT", root), \
                     patch.object(direct, "BASE", root / "pe-world-current-v0"), \
                     patch.object(Path, "read_text", return_value=raw):
                    if valid:
                        self.assertEqual(direct.origin_group(), root / "init.scope")
                    else:
                        with self.assertRaises((OSError, RuntimeError)):
                            direct.origin_group()
