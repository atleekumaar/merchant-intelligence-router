"""
Confidence Router module for Merchant Intelligence Router.
Evaluates classifier certainty against a configurable threshold to determine execution branch.
"""

import os
from typing import Union

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

from app.state import MerchantState, Intent

DEFAULT_THRESHOLD: float = 0.70


def get_confidence_threshold() -> float:
    """Retrieve configurable confidence threshold from environment variables."""
    raw_val = os.getenv("CONFIDENCE_THRESHOLD")
    if raw_val is not None:
        try:
            val = float(raw_val)
            if 0.0 <= val <= 1.0:
                return val
        except ValueError:
            pass
    return DEFAULT_THRESHOLD


def router_node(state: MerchantState) -> str:
    """
    LangGraph Conditional Routing Function.
    Evaluates confidence score against the threshold:
      - If confidence < threshold: divert to 'support' node for clarification.
      - Otherwise: route directly to the detected intent handler.
    """
    threshold = get_confidence_threshold()

    if state.confidence < threshold:
        return "support"

    if state.intent:
        intent_str = state.intent.value if isinstance(state.intent, Intent) else str(state.intent)
        valid_intents = {"analytics", "products", "customers", "inventory", "support"}
        if intent_str in valid_intents:
            return intent_str

    return "support"
