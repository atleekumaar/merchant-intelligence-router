"""
Unit tests for MerchantState schema and validation.
"""

import pytest
from pydantic import ValidationError
from app.state import MerchantState, MerchantQuery, Intent


def test_merchant_state_defaults():
    state = MerchantState(message="Hello")
    assert state.message == "Hello"
    assert state.intent is None
    assert state.confidence == 0.0
    assert state.structured_query is None
    assert state.data == {}
    assert state.reply == ""


def test_merchant_state_confidence_validation():
    # Confidence must be between 0.0 and 1.0
    with pytest.raises(ValidationError):
        MerchantState(message="Hello", confidence=1.5)

    with pytest.raises(ValidationError):
        MerchantState(message="Hello", confidence=-0.2)


def test_merchant_query_structure():
    query = MerchantQuery(metric="sales", time_period="yesterday", entity="overall_business")
    assert query.metric == "sales"
    assert query.time_period == "yesterday"
    assert query.entity == "overall_business"
