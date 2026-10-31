"""Public-fixture smoke checks, not a held-out compositionality experiment."""

import argparse
from collections import deque
import hashlib
import json
from pathlib import Path
import platform
from time import perf_counter_ns

from .runtime import Adapter, Runtime

ROOT = Path(__file__).resolve().parent.parent


def load_genome(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def load_inputs(path):
    return [json.loads(line) for line in Path(path).read_text(encoding="utf-8").splitlines() if line]


def smoke_checks():
    """Run all genomes on the same Runtime class and compare simple reference answers."""
    cases, hashes = {}, {}
    for stem in ("anomaly", "normalize", "queue"):
        genome_path = ROOT / "examples" / "genomes" / f"{stem}.json"
        inputs_path = ROOT / "examples" / "inputs" / f"{stem}.jsonl"
        for path in (genome_path, inputs_path):
            hashes[path.relative_to(ROOT).as_posix()] = hashlib.sha256(path.read_bytes()).hexdigest()
        genome, inputs = load_genome(genome_path), load_inputs(inputs_path)
        queue, reference_queue, removed, expected_removed = deque(), deque(), [], []

        def take(count):
            if type(count) is not int or not 1 <= count <= 4:
                raise ValueError("queue_take expects an integer between 1 and 4")
            batch = [queue.popleft() for _ in range(min(count, len(queue)))]
            removed.extend(batch)
            return len(batch)

        runtime = Runtime(adapters={"queue_take": Adapter("number", "number", take)},
                          regulation_bounds={"batch_size": (1, 4)})
        runs, expected, latencies = [], [], []
        for index, event in enumerate(inputs):
            observations = event
            if stem == "queue":
                items = [(index, i) for i in range(event["arrivals"])]
                queue.extend(items)
                reference_queue.extend(items)
                observations = {"queue_depth": len(queue)}
                batch_size = 4 if len(reference_queue) > 3 else 1
                consumed = min(batch_size, len(reference_queue))
                for _ in range(consumed):
                    expected_removed.append(reference_queue.popleft())
                expected.append({"batch_size": batch_size, "processed": consumed})
            elif stem == "anomaly":
                expected.append({"classification": "anomaly" if event["value"] > 75 else "normal"})
            else:
                expected.append({"name": event["name"].strip().lower()})
            started = perf_counter_ns()
            runs.append(runtime.run(genome, observations))
            latencies.append(perf_counter_ns() - started)
        checks = [run["outputs"] == reference for run, reference in zip(runs, expected)]
        if stem == "queue":
            checks.append(list(queue) == list(reference_queue))
            checks.append(removed == expected_removed)
        cases[stem] = {"passed": all(checks), "runs": len(runs),
                       "outputs": [run["outputs"] for run in runs],
                       "signals": [run["signals"] for run in runs],
                       "elapsed_ns": latencies, "traces": [run["trace"] for run in runs]}
    for path in sorted((ROOT / "programmo_evolvens").glob("*.py")):
        hashes[path.relative_to(ROOT).as_posix()] = hashlib.sha256(path.read_bytes()).hexdigest()
    return {"status": "passed" if all(c["passed"] for c in cases.values()) else "failed",
            "scope": "public-fixture smoke checks; not E0 completion or held-out evidence",
            "python": platform.python_version(), "platform": platform.platform(),
            "sha256": hashes, "cases": cases}


def main():
    parser = argparse.ArgumentParser(description="Programmo Evolvens: public-fixture smoke checks")
    parser.add_argument("--output", type=Path, help="optional JSON report with traces and checksums")
    args = parser.parse_args()
    report = smoke_checks()
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    for key, case in report["cases"].items():
        print(f"{key}: {'PASS' if case['passed'] else 'FAIL'} ({case['runs']} inputs)")
    print(report["scope"])
    return 0 if report["status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
