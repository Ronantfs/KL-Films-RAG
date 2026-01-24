from typing import Dict, Literal, TypedDict

from kl_mcp_rag.llm.parse_intent.llm_models import ModelVersions
from kl_mcp_rag.llm.parse_intent.prompts import PromptVersions
from enum import Enum


class ParseIntentVersion(TypedDict):
    model_version: str  # key of MODEL_VERSIONS
    prompt_version: str  # key of PROMPT_VERSIONS


PARSE_INTENT_VERSIONS: Dict[str, ParseIntentVersion] = {
    "pi_v1.0": {
        "model_version": ModelVersions.GPT_4_1_MINI.value,
        "prompt_version": PromptVersions.V1_0.value,
    },
}
