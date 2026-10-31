"""Sequential scalar data-flow prototype; trusted host adapters, no code in genomes."""

from copy import deepcopy
from dataclasses import dataclass
import json
import math
import operator
from time import perf_counter_ns
from typing import Callable


class GenomeError(ValueError):
    """Invalid genome or contract."""


class RunError(ValueError):
    """Failed execution, including the trace up to the failure."""

    def __init__(self, message, trace):
        super().__init__(message)
        self.trace = trace


def scalar_type(value):
    if isinstance(value, bool):
        return "bool"
    if isinstance(value, (int, float)):
        try:
            if math.isfinite(value):
                return "number"
        except OverflowError:
            pass
    if isinstance(value, str):
        return "text"
    raise GenomeError("expected a finite number, boolean or text")


def require(condition, message):
    if not condition:
        raise GenomeError(message)


def keys(value, required, optional=()):
    require(isinstance(value, dict), "expected an object")
    require(set(required) <= value.keys() <= set(required) | set(optional),
            f"expected fields {sorted(required)}, optional {sorted(optional)}")


def name(value):
    require(isinstance(value, str) and 0 < len(value) <= 80,
            "name must contain 1–80 characters")


def bounded_json(value, limit):
    try:
        encoded = json.dumps(value, ensure_ascii=False, allow_nan=False).encode("utf-8")
    except (TypeError, ValueError, OverflowError, RecursionError, UnicodeError) as exc:
        raise GenomeError("value must be finite JSON") from exc
    require(len(encoded) <= limit, f"JSON payload exceeds {limit} bytes")


@dataclass(frozen=True)
class Adapter:
    """Trusted host implementation of a declared scalar external effect."""

    input_type: str
    output_type: str
    handler: Callable


COMPARISONS = {"gt": operator.gt, "ge": operator.ge, "lt": operator.lt,
               "le": operator.le, "eq": operator.eq}
TYPES = {"number", "text", "bool"}


class Runtime:
    """A fixed eight-PP registry with explicit host limits and permissions."""

    def __init__(self, *, adapters=None, regulation_bounds=None,
                 max_steps=64, max_payload_bytes=65536):
        require(type(max_steps) is int and 1 <= max_steps <= 4096, "invalid host step limit")
        require(type(max_payload_bytes) is int and max_payload_bytes > 0, "invalid payload limit")
        self.max_steps = max_steps
        self.max_payload_bytes = max_payload_bytes
        self.adapters = dict(adapters or {})
        for key, adapter in self.adapters.items():
            name(key)
            require(isinstance(adapter, Adapter), "expected Adapter")
            require(adapter.input_type in TYPES and adapter.output_type in TYPES,
                    "invalid adapter types")
            require(callable(adapter.handler), "adapter handler must be callable")
        self.bounds = deepcopy(regulation_bounds or {})
        for key, bounds in self.bounds.items():
            name(key)
            require(isinstance(bounds, (list, tuple)) and len(bounds) == 2,
                    "expected lower and upper bounds")
            require(all(scalar_type(v) == "number" for v in bounds) and bounds[0] <= bounds[1],
                    "invalid host regulation bounds")
        self.store = {}
        self.regulation = {}

    def validate(self, genome):
        """Check every node before any external effect. References must point backwards."""
        bounded_json(genome, self.max_payload_bytes)
        keys(genome, {"schema_version", "id", "steps", "outputs"})
        require(type(genome["schema_version"]) is int and genome["schema_version"] == 0,
                "unsupported schema_version")
        name(genome["id"])
        steps = genome["steps"]
        require(isinstance(steps, list) and 0 < len(steps) <= self.max_steps,
                "step budget exceeded or empty genome")
        known = {}
        for node in steps:
            try:
                keys(node, {"id", "pp", "version", "inputs", "params"})
                name(node["id"])
                require(node["id"] not in known, "duplicate node id")
                require(type(node["version"]) is int and node["version"] == 1,
                        "unsupported primitive version")
                require(isinstance(node["pp"], str), "invalid PP name")
                inputs, params = node["inputs"], node["params"]
                require(isinstance(inputs, dict), "inputs must be an object")
                types = {port: self._binding_type(binding, known)
                         for port, binding in inputs.items()}
                output = self._contract(node["pp"], inputs, params, types)
                known[node["id"]] = output
            except (GenomeError, TypeError, KeyError) as exc:
                label = node.get("id", "?") if isinstance(node, dict) else "?"
                raise GenomeError(f"node {label}: {exc}") from exc
        outputs = genome["outputs"]
        require(isinstance(outputs, dict) and bool(outputs), "outputs must be a nonempty object")
        for key, binding in outputs.items():
            name(key)
            self._binding_type(binding, known)
        return known

    @staticmethod
    def _binding_type(binding, known):
        require(isinstance(binding, dict) and len(binding) == 1, "invalid binding")
        if "literal" in binding:
            return scalar_type(binding["literal"])
        require("ref" in binding and isinstance(binding["ref"], str), "invalid reference")
        require(binding["ref"] in known, "unknown or forward reference (cycles unsupported)")
        return known[binding["ref"]]

    def _contract(self, pp, inputs, params, types):
        def ports(expected):
            keys(inputs, expected)
            for port, kind in expected.items():
                if kind != "scalar":
                    require(types[port] == kind, f"{port} requires {kind}")

        if pp == "SENSE":
            ports({})
            keys(params, {"source", "type"})
            name(params["source"])
            require(params["type"] in TYPES, "invalid observation type")
            return params["type"]
        if pp == "COMPARE":
            ports({"left": "number", "right": "number"})
            keys(params, {"operator"})
            require(params["operator"] in COMPARISONS, "unknown comparison")
            return "bool"
        if pp == "TRANSFORM":
            keys(params, {"operation"})
            require(params["operation"] in {"strip", "lower"}, "unknown transformation")
            ports({"value": "text"})
            return "text"
        if pp == "DECIDE":
            ports({"condition": "bool", "if_true": "scalar", "if_false": "scalar"})
            keys(params, set())
            require(types["if_true"] == types["if_false"], "branch types differ")
            return types["if_true"]
        if pp == "ACT":
            keys(params, {"target"})
            name(params["target"])
            require(params["target"] in self.adapters, "unauthorized or unknown action")
            adapter = self.adapters[params["target"]]
            ports({"value": adapter.input_type})
            return adapter.output_type
        if pp == "STORE":
            keys(params, {"mode", "key", "type"})
            name(params["key"])
            require(params["type"] in TYPES, "invalid storage type")
            require(params["mode"] in {"read", "write"}, "unknown storage mode")
            ports({"value": params["type"]} if params["mode"] == "write" else {})
            return params["type"]
        if pp == "SIGNAL":
            keys(params, {"channel"})
            name(params["channel"])
            ports({"value": "scalar", "when": "bool"})
            return types["value"]
        if pp == "REGULATE":
            keys(params, {"key", "min", "max"})
            name(params["key"])
            require(params["key"] in self.bounds, "unauthorized regulator")
            require(scalar_type(params["min"]) == scalar_type(params["max"]) == "number",
                    "regulation bounds must be numeric")
            low, high = self.bounds[params["key"]]
            require(low <= params["min"] <= params["max"] <= high,
                    "genome bounds exceed host bounds")
            ports({"value": "number"})
            return "number"
        raise GenomeError(f"unknown primitive {pp}")

    def run(self, genome, observations):
        genome = deepcopy(genome)
        known = self.validate(genome)
        require(isinstance(observations, dict), "observations must be an object")
        bounded_json(observations, self.max_payload_bytes)
        observations = deepcopy(observations)
        values, signals, trace = {}, [], []
        state, regulation = deepcopy(self.store), deepcopy(self.regulation)
        # Check every external observation before any node can have an effect.
        for node in genome["steps"]:
            if node["pp"] == "SENSE":
                source = node["params"]["source"]
                require(source in observations, f"missing observation {source}")
                require(scalar_type(observations[source]) == known[node["id"]],
                        f"observation {source}: type mismatch")

        def resolve(binding):
            return binding["literal"] if "literal" in binding else values[binding["ref"]]

        for node in genome["steps"]:
            started = perf_counter_ns()
            pp, params = node["pp"], node["params"]
            inputs = {key: resolve(binding) for key, binding in node["inputs"].items()}
            try:
                if pp == "SENSE":
                    value = observations[params["source"]]
                elif pp == "COMPARE":
                    value = COMPARISONS[params["operator"]](inputs["left"], inputs["right"])
                elif pp == "TRANSFORM":
                    value = getattr(inputs["value"], params["operation"])()
                elif pp == "DECIDE":
                    value = inputs["if_true"] if inputs["condition"] else inputs["if_false"]
                elif pp == "ACT":
                    value = self.adapters[params["target"]].handler(inputs["value"])
                elif pp == "STORE":
                    if params["mode"] == "write":
                        state[params["key"]] = inputs["value"]
                    value = state[params["key"]]
                elif pp == "SIGNAL":
                    value = inputs["value"]
                    if inputs["when"]:
                        signals.append({"channel": params["channel"], "value": value})
                elif pp == "REGULATE":
                    value = max(params["min"], min(params["max"], inputs["value"]))
                    regulation[params["key"]] = value
                require(scalar_type(value) == known[node["id"]], "output type mismatch")
                bounded_json({"values": values, "next": value, "store": state,
                              "regulation": regulation, "signals": signals}, self.max_payload_bytes)
                values[node["id"]] = value
                trace.append({"node": node["id"], "pp": pp, "status": "ok",
                              "value": value, "elapsed_ns": perf_counter_ns() - started})
            except Exception as exc:
                trace.append({"node": node["id"], "pp": pp, "status": "error",
                              "error": str(exc), "elapsed_ns": perf_counter_ns() - started})
                raise RunError(f"node {node['id']}: {exc}", trace) from exc
        self.store, self.regulation = state, regulation
        return {"genome_id": genome["id"], "outputs": {key: resolve(binding)
                for key, binding in genome["outputs"].items()}, "signals": signals, "trace": trace}
