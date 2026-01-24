from typing import TypedDict, List
from experiments.parse_intent.test_cases import TEST_CASES


class ExperimentConfig(TypedDict):
    name: str
    parse_intent_version: str
    test_case_ids: List[str]
    results_path: str


ALL_TEST_CASES_IDS = [tc["id"] for tc in TEST_CASES]


EXPERIMENTS: list[ExperimentConfig] = [
    # {
    #     "name": "baseline_pi_v1_0",
    #     "parse_intent_version": "pi_v1.0",
    #     "test_case_ids": ALL_TEST_CASES_IDS,
    #     "results_path": "experiments/parse_intent/results/baseline_pi_v1_0.json",
    # },
    {
        "name": "baseline_pi_v1_1",
        "parse_intent_version": "pi_v1.1",
        "test_case_ids": ALL_TEST_CASES_IDS,
        "results_path": "experiments/parse_intent/results/baseline_pi_v1_1.json",
    },
]
