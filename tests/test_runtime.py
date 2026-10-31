from copy import deepcopy
import unittest

from programmo_evolvens import Adapter, GenomeError, RunError, Runtime
from programmo_evolvens.demo import ROOT, load_genome, smoke_checks


def node(identifier, pp, inputs, params):
    return {"id": identifier, "pp": pp, "version": 1, "inputs": inputs, "params": params}


def literal(value):
    return {"literal": value}


def ref(value):
    return {"ref": value}


def genome(*steps):
    return {"schema_version": 0, "id": "test", "steps": list(steps),
            "outputs": {"value": ref(steps[-1]["id"])}}


class RuntimeTests(unittest.TestCase):
    def setUp(self):
        self.anomaly = load_genome(ROOT / "examples/genomes/anomaly.json")

    def test_all_examples_match_reference_answers(self):
        result = smoke_checks()
        self.assertEqual(result["status"], "passed")
        self.assertEqual(sum(c["runs"] for c in result["cases"].values()), 14)

    def test_threshold_boundary_and_signals(self):
        runtime = Runtime()
        for value, label, count in [(75, "normal", 0), (75.01, "anomaly", 1), (-10, "normal", 0)]:
            with self.subTest(value=value):
                run = runtime.run(self.anomaly, {"value": value})
                self.assertEqual(run["outputs"], {"classification": label})
                self.assertEqual(len(run["signals"]), count)
                self.assertEqual(len(run["trace"]), 4)

    def test_genome_change_changes_behavior_without_runtime_change(self):
        changed = deepcopy(self.anomaly)
        changed["steps"][1]["inputs"]["right"] = literal(100)
        self.assertEqual(Runtime().run(changed, {"value": 80})["outputs"]["classification"], "normal")
        self.assertEqual(Runtime().run(self.anomaly, {"value": 80})["outputs"]["classification"], "anomaly")

    def test_invalid_graphs_fail_validation(self):
        mutations = [
            lambda g: g.update(schema_version=True),
            lambda g: g.update(schema_version=99),
            lambda g: g.update(extra="code"),
            lambda g: g["steps"][0].update(pp="EVAL"),
            lambda g: g["steps"][0].update(version=2),
            lambda g: g["steps"][1].update(id="sample"),
            lambda g: g["steps"][1]["inputs"].update(left=ref("high")),
            lambda g: g["steps"][1]["inputs"].update(left=ref("missing")),
            lambda g: g["steps"][1]["inputs"].update(right=literal(True)),
            lambda g: g["steps"][2]["inputs"].update(if_true=literal(1)),
            lambda g: g["steps"][1]["params"].update(operator="execute"),
            lambda g: g["outputs"].update(result=ref("missing")),
            lambda g: g["steps"][1]["inputs"].update(right={"literal": 1, "ref": "sample"}),
            lambda g: g["steps"][1]["inputs"].update(right=literal(float("inf"))),
        ]
        for index, mutation in enumerate(mutations):
            with self.subTest(index=index):
                changed = deepcopy(self.anomaly)
                mutation(changed)
                with self.assertRaises(GenomeError):
                    Runtime().validate(changed)

    def test_observation_types_missing_and_nonfinite(self):
        for observations in ({}, {"value": True}, {"value": "80"}, {"value": float("nan")}):
            with self.subTest(observations=observations), self.assertRaises(GenomeError):
                Runtime().run(self.anomaly, observations)

    def test_host_step_and_payload_limits(self):
        with self.assertRaisesRegex(GenomeError, "budget"):
            Runtime(max_steps=3).run(self.anomaly, {"value": 100})
        with self.assertRaisesRegex(GenomeError, "bytes"):
            Runtime(max_payload_bytes=32).validate(self.anomaly)

    def test_preflight_prevents_actions_before_bad_later_node(self):
        effects = []
        runtime = Runtime(adapters={"effect": Adapter("number", "number", lambda v: effects.append(v) or v)})
        first = node("a", "ACT", {"value": literal(1)}, {"target": "effect"})
        bad = node("b", "SENSE", {}, {"source": "absent", "type": "number"})
        with self.assertRaises(GenomeError):
            runtime.run(genome(first, bad), {})
        self.assertEqual(effects, [])
        bad["pp"] = "UNKNOWN"
        with self.assertRaises(GenomeError):
            runtime.run(genome(first, bad), {})
        self.assertEqual(effects, [])

    def test_unknown_action_is_denied(self):
        action = node("act", "ACT", {"value": literal(1)}, {"target": "shell"})
        with self.assertRaisesRegex(GenomeError, "unauthorized"):
            Runtime().run(genome(action), {})

    def test_store_persists_only_after_successful_run(self):
        write = node("write", "STORE", {"value": literal("old")},
                     {"mode": "write", "key": "name", "type": "text"})
        runtime = Runtime()
        runtime.run(genome(write), {})
        read = node("read", "STORE", {}, {"mode": "read", "key": "name", "type": "text"})
        self.assertEqual(runtime.run(genome(read), {})["outputs"]["value"], "old")
        write["inputs"]["value"] = literal("new")
        missing = node("missing", "STORE", {}, {"mode": "read", "key": "absent", "type": "text"})
        with self.assertRaises(RunError) as caught:
            runtime.run(genome(write, missing), {})
        self.assertEqual(runtime.store["name"], "old")
        self.assertEqual(caught.exception.trace[-1]["status"], "error")

    def test_store_read_checks_declared_type(self):
        runtime = Runtime()
        runtime.store["name"] = "text"
        read = node("read", "STORE", {}, {"mode": "read", "key": "name", "type": "number"})
        with self.assertRaisesRegex(RunError, "type mismatch"):
            runtime.run(genome(read), {})

    def test_regulation_clamps_and_does_not_modify_genome(self):
        adjust = node("r", "REGULATE", {"value": literal(100)}, {"key": "batch", "min": 1, "max": 4})
        original = genome(adjust)
        copy = deepcopy(original)
        runtime = Runtime(regulation_bounds={"batch": (1, 4)})
        self.assertEqual(runtime.run(original, {})["outputs"]["value"], 4)
        self.assertEqual(runtime.regulation, {"batch": 4})
        self.assertEqual(original, copy)
        adjust["params"]["max"] = 5
        with self.assertRaisesRegex(GenomeError, "host bounds"):
            runtime.run(genome(adjust), {})
        with self.assertRaisesRegex(GenomeError, "unauthorized"):
            Runtime().run(original, {})

    def test_adapter_failure_has_trace_and_no_internal_commit(self):
        def fail(value):
            raise OSError("injected failure")
        runtime = Runtime(adapters={"fail": Adapter("number", "number", fail)})
        write = node("w", "STORE", {"value": literal(1)}, {"mode": "write", "key": "x", "type": "number"})
        act = node("a", "ACT", {"value": ref("w")}, {"target": "fail"})
        with self.assertRaises(RunError) as caught:
            runtime.run(genome(write, act), {})
        self.assertEqual(runtime.store, {})
        self.assertEqual([e["status"] for e in caught.exception.trace], ["ok", "error"])

    def test_adapter_output_contract_is_checked(self):
        runtime = Runtime(adapters={"bad": Adapter("number", "number", lambda value: "wrong")})
        act = node("a", "ACT", {"value": literal(1)}, {"target": "bad"})
        with self.assertRaisesRegex(RunError, "type mismatch"):
            runtime.run(genome(act), {})

    def test_text_transform_cannot_select_arbitrary_method(self):
        transform = node("t", "TRANSFORM", {"value": literal(" x ")}, {"operation": "__class__"})
        with self.assertRaisesRegex(GenomeError, "unknown transformation"):
            Runtime().run(genome(transform), {})

    def test_adapter_must_be_callable(self):
        with self.assertRaisesRegex(GenomeError, "callable"):
            Runtime(adapters={"bad": Adapter("number", "number", None)})

    def test_unencodable_json_is_rejected(self):
        changed = deepcopy(self.anomaly)
        changed["id"] = "\ud800"
        with self.assertRaises(GenomeError):
            Runtime().validate(changed)

    def test_external_effect_is_not_rolled_back_on_later_failure(self):
        effects = []
        runtime = Runtime(adapters={"effect": Adapter("number", "number", lambda v: effects.append(v) or v)})
        act = node("a", "ACT", {"value": literal(1)}, {"target": "effect"})
        missing = node("r", "STORE", {}, {"mode": "read", "key": "absent", "type": "number"})
        with self.assertRaises(RunError) as caught:
            runtime.run(genome(act, missing), {})
        self.assertEqual(effects, [1])
        self.assertEqual(caught.exception.trace[0]["status"], "ok")

    def test_store_budget_failure_does_not_commit_state(self):
        runtime = Runtime(max_payload_bytes=1200)
        runtime.store["prior"] = "x" * 1000
        write = node("w", "STORE", {"value": literal("y" * 300)},
                     {"mode": "write", "key": "new", "type": "text"})
        with self.assertRaisesRegex(RunError, "bytes"):
            runtime.run(genome(write), {})
        self.assertNotIn("new", runtime.store)


if __name__ == "__main__":
    unittest.main()
