"""
Inventory Node: Handles stock inquiries, low stock warnings, and reorder alerts.
"""

from app.state import MerchantState
from app.data.mock_data import get_inventory_summary


def inventory_node(state: MerchantState) -> MerchantState:
    """Deterministic inventory calculation and alert synthesis."""
    inv_summary = get_inventory_summary()
    state.data = inv_summary

    low_stock = inv_summary["low_stock_items"]
    out_of_stock = inv_summary["out_of_stock_items"]
    total_units = inv_summary["total_units_in_stock"]
    total_items = inv_summary["total_unique_items"]

    alerts = []
    for item in low_stock:
        if item["stock_quantity"] == 0:
            alerts.append(f"  🔴 **{item['name']}**: OUT OF STOCK (Reorder threshold: {item['reorder_threshold']})")
        else:
            alerts.append(f"  ⚠️ **{item['name']}**: {item['stock_quantity']} units left (Reorder threshold: {item['reorder_threshold']})")

    alerts_str = "\n".join(alerts) if alerts else "  ✅ All items are currently well-stocked."

    state.reply = (
        f"📋 **Inventory Status Overview**:\n"
        f"• Total catalog items: **{total_items}** ({total_units} total units in stock).\n"
        f"• Items requiring attention:\n"
        f"{alerts_str}\n\n"
        f"💡 *Action needed: Please reorder items marked with 🔴 and ⚠️ promptly.*"
    )
    return state
