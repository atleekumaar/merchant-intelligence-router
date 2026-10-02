"""
Integration tests for the compiled LangGraph execution.
"""

from app.graph import run_merchant_agent
from app.state import Intent


def test_full_graph_analytics_flow():
    state = run_merchant_agent("how much did I sell today?")
    assert state.intent == Intent.ANALYTICS
    assert state.confidence >= 0.70
    assert "Sales Analytics" in state.reply or "revenue" in state.reply.lower()


def test_full_graph_products_flow():
    state = run_merchant_agent("show my products")
    assert state.intent == Intent.PRODUCTS
    assert state.confidence >= 0.70
    assert "Top Best-Selling Products" in state.reply


def test_full_graph_customers_flow():
    state = run_merchant_agent("who are my repeat customers?")
    assert state.intent == Intent.CUSTOMERS
    assert state.confidence >= 0.70
    assert "Top Customers by Total Spend" in state.reply


def test_full_graph_inventory_flow():
    state = run_merchant_agent("which products are low in stock?")
    assert state.intent == Intent.INVENTORY
    assert state.confidence >= 0.70
    assert "Inventory Status Overview" in state.reply


def test_full_graph_support_flow():
    state = run_merchant_agent("help me")
    assert state.intent == Intent.SUPPORT
    assert state.confidence >= 0.70
    assert "Help Center" in state.reply or "VyaparMitra" in state.reply


def test_full_graph_ambiguous_routes_to_support():
    state = run_merchant_agent("tell me about my business")
    # Ambiguous input receives low confidence (< 0.70) and is diverted to support node
    assert state.confidence < 0.70
    assert "not entirely sure" in state.reply.lower() or "help center" in state.reply.lower()
