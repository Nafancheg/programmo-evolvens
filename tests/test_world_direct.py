import sys
import tempfile
from pathlib import Path
import unittest
from unittest.mock import patch

if sys.platform == "linux":
    from world.wsl2 import direct


@unittest.skipUnless(sys.platform == "linux", "direct cgroup backend is Linux-only")
class DirectWorldTests(unittest.TestCase):
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
