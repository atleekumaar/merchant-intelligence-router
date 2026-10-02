"""
Products Node: Handles product catalog rankings and top-selling SKU queries.
"""

from app.state import MerchantState
from app.data.mock_data import get_top_products


def products_node(state: MerchantState) -> MerchantState:
    """Deterministic product ranking computation and reply generation."""
    top_prods = get_top_products(limit=5)
    state.data = {"top_products": top_prods}

    product_lines = "\n".join(
        f"  {idx}. **{p['name']}** ({p['category']}): **{p['units_sold']:,} units sold** | Price: ₹{p['price']} | Rating: ⭐ {p['rating']}"
        for idx, p in enumerate(top_prods, start=1)
    )

    state.reply = (
        f"📦 **Top Best-Selling Products**:\n"
        f"{product_lines}\n\n"
        f"💡 *Tip: Your top performer is '{top_prods[0]['name']}' with {top_prods[0]['units_sold']} units sold.*"
    )
    return state
