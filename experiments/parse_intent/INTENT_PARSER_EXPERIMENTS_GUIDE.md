# KL-Films-RAG – Intent Parser Experiments Guide

- use VS code launch to run/debug
---

## 2. How to Define Test Cases

**File:**
```
experiments/parse_intent/test_cases.py
```

Each test case defines:
- `id` – unique identifier
- `query` – raw user query
- `test_label` – human-readable description
- `expected` – expected parsed intent output

**Example:**
```python
{
    "id": "tc_001",
    "query": "Is Star Wars showing next weekend?",
    "test_label": "film + date, no cinema",
    "expected": {
        "cinemas": [],
        "date_expression": "next weekend",
        "film_mention": "Star Wars",
    },
}
```

Test cases are used to evaluate parser version performances in Experiements: 
---

## 3. How to Define Experiments

**File:**
```
experiments/parse_intent/experiments.py
```
experiements specify versions of prompts and models used by parser on test cases. Each experiement recrods results to disk. 

**Example:**
```python
{
    "name": "baseline_pi_v1_0",
    "parse_intent_version": "pi_v1.0",
    "test_case_ids": ["tc_001", "tc_002"],
    "results_path": "experiments/parse_intent/results/baseline_pi_v1_0.json",
}
```

Parser versions are defined centrally in:
```
kl_mcp_rag/llm/parse_intent/parser_versions.py
```

---

## 4. Experiement Results

Results are written as JSON files to:
```
experiments/parse_intent/results/
```


# updates from results: 
for a given model version, update the prompt versions used by appending context so more test cases pass. 

