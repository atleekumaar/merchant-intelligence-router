"""
Unit tests for Jev Intent Classification and Confidence calculation.
"""

import pytest
from app.classifier import classify_intent_jev, jev_router
from app.state import MerchantState


def test_analytics_classification():
    query = "Why did my revenue fall yesterday?"
    intent, confidence = classify_intent_jev(query)
    assert intent == "analytics"
    assert confidence >= 0.70


def test_products_classification():
    query = "Show top products"
    intent, confidence = classify_intent_jev(query)
    assert intent == "products"
    assert confidence >= 0.70


def test_customers_classification():
    query = "Who are my best customers?"
    intent, confidence = classify_intent_jev(query)
    assert intent == "customers"
    assert confidence >= 0.70


def test_inventory_classification():
    query = "How many items are left?"
    intent, confidence = classify_intent_jev(query)
    assert intent == "inventory"
    assert confidence >= 0.70


def test_support_classification():
    query = "How do I use this dashboard?"
    intent, confidence = classify_intent_jev(query)
    assert intent == "support"
    assert confidence >= 0.70


def test_ambiguous_low_confidence():
    query = "Can you bake a chocolate cake for tomorrow?"
    intent, confidence = classify_intent_jev(query)
    # Ambiguous queries should have low confidence
    assert confidence < 0.70


def test_jev_router_state_mutation():
    state = MerchantState(message="Show me my top 5 products")
    updated = jev_router(state)
    assert updated.intent == "products"
    assert updated.confidence > 0.0
    assert updated.reply is None  # Ensures no business logic is mixed in router
