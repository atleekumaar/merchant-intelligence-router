"""
Unit tests for Confidence Routing decisions.
"""

from app.router import router_node
from app.state import MerchantState, Intent


def test_high_confidence_analytics_routing():
    state = MerchantState(message="Show sales", intent=Intent.ANALYTICS, confidence=0.85)
    destination = router_node(state)
    assert destination == "analytics"


def test_high_confidence_inventory_routing():
    state = MerchantState(message="Show stock", intent=Intent.INVENTORY, confidence=0.88)
    destination = router_node(state)
    assert destination == "inventory"


def test_low_confidence_fallback_to_support():
    state = MerchantState(message="Something weird", intent=Intent.ANALYTICS, confidence=0.45)
    destination = router_node(state)
    # Any confidence below 0.70 must divert to support node
    assert destination == "support"


def test_unknown_intent_fallback():
    state = MerchantState(message="Random", confidence=0.90)
    destination = router_node(state)
    assert destination == "support"
