"""
Unit tests for Confidence Routing decisions.
"""

from app.router import router_node
from app.state import MerchantState


def test_high_confidence_routing():
    state = MerchantState(message="Show sales", intent="analytics", confidence=0.85)
    destination = router_node(state)
    assert destination == "analytics"


def test_low_confidence_fallback_to_support():
    state = MerchantState(message="Something weird", intent="analytics", confidence=0.45)
    destination = router_node(state)
    assert destination == "support"


def test_unknown_intent_fallback():
    state = MerchantState(message="Random", intent="non_existent_intent", confidence=0.90)
    destination = router_node(state)
    assert destination == "support"
