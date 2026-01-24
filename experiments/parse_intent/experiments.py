from typing import TypedDict, List


class ExperimentConfig(TypedDict):
    name: str
    parse_intent_version: str
    test_case_ids: List[str]
    results_path: str


EXPERIMENTS: list[ExperimentConfig] = [
    {
        "name": "baseline_pi_v1_0",
        "parse_intent_version": "pi_v1.0",
        "test_case_ids": ["tc_001", "tc_002"],
        "results_path": "experiments/parse_intent/results/baseline_pi_v1_0.json",
    }
]
