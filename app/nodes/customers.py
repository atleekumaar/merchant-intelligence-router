"""
Customers Node: Handles customer segmentation, repeat buyer queries, and top-spender rankings.
"""

from app.state import MerchantState
from app.data.mock_data import get_top_customers


def customers_node(state: MerchantState) -> MerchantState:
    """Deterministic customer ranking and reply generation."""
    top_custs = get_top_customers(limit=5)
    state.data = {"top_customers": top_custs}

    customer_lines = "\n".join(
        f"  {idx}. **{c['name']}** ({c['city']}) - **₹{c['total_spent']:,}** across {c['orders_count']} orders [{c['segment']}]"
        for idx, c in enumerate(top_custs, start=1)
    )

    state.reply = (
        f"👥 **Top Customers by Total Spend**:\n"
        f"{customer_lines}\n\n"
        f"💡 *Tip: High-frequency customer '{top_custs[0]['name']}' has placed {top_custs[0]['orders_count']} orders to date.*"
    )
    return state
