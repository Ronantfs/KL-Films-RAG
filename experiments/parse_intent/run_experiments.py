import json
import os
from datetime import datetime
from dotenv import load_dotenv
from openai import OpenAI

from kl_mcp_rag.llm.parse_intent.parser import parse_intent
from kl_mcp_rag.llm.parse_intent.parser_versions import PARSE_INTENT_VERSIONS

from experiments.parse_intent.test_cases import TEST_CASES
from experiments.parse_intent.experiments import EXPERIMENTS


def run() -> None:
    print("Running parse intent experiments...")
    load_dotenv()
    client = OpenAI()

    test_case_map = {tc["id"]: tc for tc in TEST_CASES}

    for experiment in EXPERIMENTS:
        parse_intent_version = PARSE_INTENT_VERSIONS[experiment["parse_intent_version"]]

        results = []

        # Run each test case in the experiment
        for tc_id in experiment["test_case_ids"]:
            tc = test_case_map[tc_id]

            # parse query with versioned parser
            returned = parse_intent(
                parse_intent_version,
                client,
                tc["query"],
            )

            success = returned == tc["expected"]

            results.append(
                {
                    "test_case_id": tc["id"],
                    "test_label": tc["test_label"],
                    "raw_query": tc["query"],
                    "returned_data": returned,
                    "expected_data": tc["expected"],
                    "success": success,
                }
            )

        output = {
            "experiment_name": experiment["name"],
            "parse_intent_version": experiment["parse_intent_version"],
            "timestamp": datetime.utcnow().isoformat(),
            "results": results,
        }

        os.makedirs(os.path.dirname(experiment["results_path"]), exist_ok=True)

        with open(experiment["results_path"], "w") as f:
            json.dump(output, f, indent=2)


# launch from launch config / cli
if __name__ == "__main__":
    run()
