import json
from pathlib import Path
import unittest
from unittest.mock import patch

from world.wsl2.controller import ASSETS, Monitor, bwrap_args, load_policy, preflight, worker_unit
from world.wsl2.seccomp import SYSCALLS


def event(**fields):
    return json.dumps(fields).encode() + b"\n"


class WorldControlTests(unittest.TestCase):
    def setUp(self):
        self.policy, self.policy_hash = load_policy()
        self.monitor = Monitor(self.policy, 10)

    def test_fixed_policy_and_real_hash(self):
        self.assertEqual(len(self.policy_hash), 64)
        self.assertEqual(self.policy["memory_bytes"], 256 * 1024 * 1024)
        self.assertEqual(self.policy["runtime_seconds"], 70)

    def test_heartbeat_uses_arrival_time_not_workload_clock(self):
        self.monitor.feed(event(type="heartbeat", seq=0, timestamp=1e30), 11)
        self.assertIsNone(self.monitor.tick(15.9))
        self.assertEqual(self.monitor.tick(16), "heartbeat_timeout")

    def test_replayed_heartbeat_is_not_liveness(self):
        line = event(type="heartbeat", seq=0, timestamp=1)
        self.monitor.feed(line, 11)
        self.monitor.feed(line, 12)
        self.assertEqual(self.monitor.reason, "protocol_error")

    def test_heartbeats_do_not_extend_runtime(self):
        for seq, now in enumerate(range(11, 80)):
            self.monitor.feed(event(type="heartbeat", seq=seq, timestamp=now), now)
        self.assertEqual(self.monitor.tick(80), "runtime_limit")

    def test_fragmented_json_and_result(self):
        line = event(type="heartbeat", seq=0, timestamp=12)
        self.monitor.feed(line[:5], 11)
        self.monitor.feed(line[5:], 12)
        self.monitor.feed(event(type="result", value="ok"), 13)
        self.assertEqual(self.monitor.result["value"], "ok")
        self.assertEqual(self.monitor.pending, b"")

    def test_non_json_and_nonfinite_heartbeats_are_rejected(self):
        for line in (b"hello\n", b"[]\n", event(type="heartbeat", seq=True, timestamp=2),
                     event(type="heartbeat", seq=0, timestamp=float("inf")),
                     b'{"type":"result","value":NaN}\n', b'{"type":"result","type":"heartbeat"}\n'):
            with self.subTest(line=line):
                monitor = Monitor(self.policy, 0)
                monitor.feed(line, 1)
                self.assertEqual(monitor.reason, "protocol_error")

    def test_line_flood_is_bounded_even_without_newline(self):
        self.monitor.feed(b"x" * (self.policy["max_line_bytes"] + 1), 11)
        self.assertEqual(self.monitor.reason, "line_limit")

    def test_stderr_counts_towards_output_budget(self):
        self.monitor.feed(b"x" * (self.policy["max_output_bytes"] + 1), 11, stdout=False)
        self.assertEqual(self.monitor.reason, "output_limit")

    def test_result_does_not_count_as_heartbeat(self):
        self.monitor.feed(event(type="result", value="ok"), 14)
        self.assertEqual(self.monitor.tick(15), "heartbeat_timeout")

    def test_duplicate_results_rejected(self):
        self.monitor.feed(event(type="result", value=1), 11)
        self.monitor.feed(event(type="result", value=2), 12)
        self.assertEqual(self.monitor.reason, "protocol_error")

    def test_service_limits_and_controller_lifetime_binding(self):
        controller = "pe-control-" + "b" * 32 + ".service"
        unit, command = worker_unit("a" * 32, controller)
        self.assertEqual(unit, "pe-run-" + "a" * 32 + ".service")
        for argument in ("--property=RuntimeMaxSec=70s", "--property=LimitNOFILE=256",
                         "--property=MemorySwapMax=0", "--property=KillMode=control-group",
                         f"--property=BindsTo={controller}", "--service-type=exec"):
            self.assertIn(argument, command)
        self.assertNotIn("--scope", command)

    def test_unit_names_cannot_inject_arguments(self):
        for run_id, controller in (("bad; echo", "x"), ("a" * 32, "ssh.service")):
            with self.assertRaises(ValueError):
                worker_unit(run_id, controller)

    def test_bwrap_exposes_only_fixed_read_only_inputs(self):
        args = bwrap_args(10)
        for flag in ("--clearenv", "--unshare-net", "--unshare-pid", "--new-session",
                     "--die-with-parent", "--disable-userns", "--assert-userns-disabled"):
            self.assertIn(flag, args)
        self.assertEqual(args[args.index("--seccomp") + 1], "10")
        self.assertEqual(args[args.index("--uid") + 1], "65534")
        sources = [args[i + 1] for i, value in enumerate(args) if value == "--ro-bind"]
        self.assertEqual(sources, [str(ASSETS / "rootfs"), str(ASSETS / "probes/smoke.py")])
        self.assertNotIn("--bind", args)
        self.assertNotIn("--share-net", args)

    def test_allowlist_does_not_include_sensitive_syscalls(self):
        for name in ("socket", "connect", "mount", "unshare", "setns", "ptrace", "bpf",
                     "clone", "clone3", "fork", "vfork", "reboot", "swapon"):
            self.assertNotIn(name, SYSCALLS)

    def test_non_linux_preflight_refuses_without_launching(self):
        with patch("world.wsl2.controller.platform.system", return_value="Windows"):
            self.assertTrue(preflight())


if __name__ == "__main__":
    unittest.main()
