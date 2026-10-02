"""
Analytics Node: Handles sales trends, revenue calculations, and period-over-period performance.
"""

from app.state import MerchantState
from app.data.mock_data import get_sales_analytics
from app.llm import extract_structured_query, generate_llm_explanation


def analytics_node(state: MerchantState) -> MerchantState:
    """Deterministic analytics computation with optional LLM explanation synthesis."""
    # 1. Extract structured query parameters
    state.structured_query = extract_structured_query(state.message)

    # 2. Retrieve deterministic metrics
    analytics_data = get_sales_analytics()
    state.data = analytics_data

    # 3. Optional LLM Explanation
    llm_summary = generate_llm_explanation(state.message, analytics_data)
    if llm_summary:
        state.reply = llm_summary
        return state

    # 4. Pure deterministic natural language response
    yesterday = analytics_data["yesterday"]
    day_before = analytics_data["day_before"]
    rev_change = analytics_data["revenue_pct_change"]
    orders_change = analytics_data["orders_pct_change"]

    status = "drop" if rev_change < 0 else "increase"
    abs_rev_change = abs(rev_change)
    abs_orders_change = abs(orders_change)

    state.reply = (
        f"📊 **Sales Analytics Summary**:\n"
        f"• Yesterday ({yesterday['date']}), your revenue was **₹{yesterday['revenue']:,}** across **{yesterday['orders']} orders**.\n"
        f"• Compared to the previous day ({day_before['date']} at ₹{day_before['revenue']:,}), revenue saw a **{status} of {abs_rev_change:.1f}%**.\n"
        f"• Order volume also saw a **{status} of {abs_orders_change:.1f}%** (Avg order value: ₹{yesterday['avg_order_value']:.2f})."
    )
    return state
