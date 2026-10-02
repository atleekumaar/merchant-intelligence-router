"""
Confidence Router module.
Directs graph execution to specialized nodes or falls back to support based on confidence threshold.
"""

import os

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

from app.state import MerchantState

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
    Conditional routing function for LangGraph.
    Evaluates confidence score against the threshold.
    Returns the name of the next node to execute.
    """
    threshold = get_confidence_threshold()
    
    # If confidence is below threshold, divert to support node for clarification
    if state.confidence < threshold:
        return "support"
    
    # Otherwise route directly to the classified intent
    valid_intents = {"analytics", "products", "customers", "inventory", "support"}
    if state.intent in valid_intents:
        return state.intent
    
    return "support"
