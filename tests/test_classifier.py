"""
Unit tests for Local Jev-Compatible Classifier (TF-IDF + Cosine Similarity).
"""

import pytest
from app.classifier import JevCompatibleClassifier, BaseIntentClassifier, normalize_text
from app.state import Intent, ClassificationResult


@pytest.fixture
def classifier():
    return JevCompatibleClassifier()


def test_is_base_intent_classifier_subclass(classifier):
    assert isinstance(classifier, BaseIntentClassifier)


@pytest.mark.parametrize("query", [
    "how much did I sell today?",
    "show my revenue",
    "what were my sales this week?",
    "why were my sales low yesterday?",
    "how are my sales doing"
])
def test_analytics_intent_classification(classifier, query):
    result = classifier.classify(query)
    assert result.intent == Intent.ANALYTICS
    assert result.confidence >= 0.70


@pytest.mark.parametrize("query", [
    "show my products",
    "what is my best selling product?",
    "show me my top 5 products",
    "which product sells the most",
    "show product catalog"
])
def test_products_intent_classification(classifier, query):
    result = classifier.classify(query)
    assert result.intent == Intent.PRODUCTS
    assert result.confidence >= 0.70


@pytest.mark.parametrize("query", [
    "show my customers",
    "who are my repeat customers?",
    "which customers bought from me most",
    "who are my best customers",
    "which customers buy frequently"
])
def test_customers_intent_classification(classifier, query):
    result = classifier.classify(query)
    assert result.intent == Intent.CUSTOMERS
    assert result.confidence >= 0.70


@pytest.mark.parametrize("query", [
    "which products are low in stock?",
    "what should I reorder?",
    "how much inventory do I have?",
    "how many items are left?",
    "stock levels"
])
def test_inventory_intent_classification(classifier, query):
    result = classifier.classify(query)
    assert result.intent == Intent.INVENTORY
    assert result.confidence >= 0.70


@pytest.mark.parametrize("query", [
    "help me",
    "how does this work?",
    "how do I use this dashboard",
    "I need assistance",
    "what can you do"
])
def test_support_intent_classification(classifier, query):
    result = classifier.classify(query)
    assert result.intent == Intent.SUPPORT
    assert result.confidence >= 0.70


@pytest.mark.parametrize("query", [
    "show me something useful",
    "tell me about my business",
    "what should I know?",
    "give me an update",
    "tell me the history of ancient Rome"
])
def test_ambiguous_queries_lower_confidence(classifier, query):
    result = classifier.classify(query)
    # Ambiguous inputs must not receive blind high confidence
    assert result.confidence < 0.70


@pytest.mark.parametrize("empty_input", ["", "   ", "\n\t  "])
def test_empty_and_whitespace_inputs(classifier, empty_input):
    result = classifier.classify(empty_input)
    assert result.intent == Intent.SUPPORT
    assert result.confidence <= 0.50


def test_classifier_explain_mode(classifier):
    explanation = classifier.explain("How much did I sell today?")
    assert "input" in explanation
    assert "intent_scores" in explanation
    assert "selected_intent" in explanation
    assert "confidence" in explanation
    assert explanation["selected_intent"] == "analytics"
    assert explanation["confidence"] >= 0.70
    assert len(explanation["intent_scores"]) == 5


def test_normalization_and_synonyms():
    norm = normalize_text("  HOW MUCH TURNOVER DID I MAKE TODAY???  ")
    assert "sales revenue" in norm or "turnover" in norm
    assert "?" not in norm
