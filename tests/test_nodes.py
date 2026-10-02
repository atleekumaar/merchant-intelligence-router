"""
Unit tests for Specialized Business Nodes.
"""

from app.state import MerchantState
from app.nodes.analytics import analytics_node
from app.nodes.products import products_node
from app.nodes.customers import customers_node
from app.nodes.inventory import inventory_node
from app.nodes.support import support_node


def test_analytics_node():
    state = MerchantState(message="Why did sales drop yesterday?")
    out = analytics_node(state)
    assert out.reply is not None
    assert "₹31,200" in out.reply or "revenue" in out.reply.lower()
    assert "yesterday" in out.data


def test_products_node():
    state = MerchantState(message="Show top products")
    out = products_node(state)
    assert out.reply is not None
    assert "Organic Green Tea" in out.reply
    assert "top_products" in out.data


def test_customers_node():
    state = MerchantState(message="Best customers")
    out = customers_node(state)
    assert out.reply is not None
    assert "Aarav Sharma" in out.reply
    assert "top_customers" in out.data


def test_inventory_node():
    state = MerchantState(message="Check inventory")
    out = inventory_node(state)
    assert out.reply is not None
    assert "Inventory Status Overview" in out.reply
    assert "low_stock_items" in out.data


def test_support_node():
    state = MerchantState(message="Help me", confidence=0.90)
    out = support_node(state)
    assert out.reply is not None
    assert "VyaparMitra Merchant Assistant Help Center" in out.reply
