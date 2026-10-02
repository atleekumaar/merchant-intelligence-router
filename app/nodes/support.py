"""
Support Node: Handles general merchant support, ambiguous inputs, and low-confidence fallbacks.
"""

from app.state import MerchantState


def support_node(state: MerchantState) -> MerchantState:
    """Provides user guidance, system help, and clarification for low-confidence inputs."""
    confidence_pct = int(state.confidence * 100)
    
    is_low_conf = state.confidence < 0.70 and state.intent is not None
    
    if is_low_conf:
        lead_in = (
            f"🤔 I'm not entirely sure how to handle your query (Confidence: {confidence_pct}%).\n"
            f"Here are the specific areas I can help you with:"
        )
    else:
        lead_in = (
            f"👋 **VyaparMitra Merchant Assistant Help Center**:\n"
            f"I can analyze your business data and answer questions across these areas:"
        )

    state.reply = (
        f"{lead_in}\n\n"
        f"1. 📊 **Analytics**: Ask *'Why were sales low yesterday?'* or *'Show my revenue trend'*.\n"
        f"2. 📦 **Products**: Ask *'What are my top 5 products?'* or *'Show best sellers'*.\n"
        f"3. 👥 **Customers**: Ask *'Who are my best customers?'* or *'Show repeat buyers'*.\n"
        f"4. 📋 **Inventory**: Ask *'How much stock do I have?'* or *'Show low inventory items'*.\n"
        f"5. ❓ **Support**: Ask *'How do I use this dashboard?'* for system navigation.\n\n"
        f"Please try rephrasing your question or selecting one of the categories above."
    )
    return state
