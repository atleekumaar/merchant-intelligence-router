"""
Integration tests for the compiled LangGraph execution.
"""

from app.graph import run_merchant_agent


def test_full_graph_analytics_flow():
    state = run_merchant_agent("Why were my sales low yesterday?")
    assert state.intent == "analytics"
    assert state.confidence >= 0.70
    assert state.reply is not None
    assert "Sales Analytics" in state.reply or "revenue" in state.reply.lower()


def test_full_graph_products_flow():
    state = run_merchant_agent("Show me my top 5 products")
    assert state.intent == "products"
    assert state.confidence >= 0.70
    assert "Top Best-Selling Products" in state.reply


def test_full_graph_customers_flow():
    state = run_merchant_agent("Which customers bought from me most?")
    assert state.intent == "customers"
    assert state.confidence >= 0.70
    assert "Top Customers by Total Spend" in state.reply


def test_full_graph_inventory_flow():
    state = run_merchant_agent("How much inventory do I have?")
    assert state.intent == "inventory"
    assert state.confidence >= 0.70
    assert "Inventory Status Overview" in state.reply


def test_full_graph_support_flow():
    state = run_merchant_agent("I need help using the dashboard")
    assert state.intent == "support"
    assert state.confidence >= 0.70
    assert "Help Center" in state.reply


def test_full_graph_ambiguous_routes_to_support():
    state = run_merchant_agent("Tell me the history of ancient Rome")
    assert state.confidence < 0.70
    # Even if an intent was guessed, low confidence forces routing to support
    assert "I'm not entirely sure how to handle your query" in state.reply
