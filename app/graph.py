"""
LangGraph StateGraph configuration for Merchant Intelligence Router.
Orchestrates state transitions from Jev Classifier -> Confidence Router -> Specialized Business Nodes.
"""

from typing import Union, Dict, Any
from langgraph.graph import StateGraph, START, END

from app.state import MerchantState
from app.classifier import jev_router
from app.router import router_node
from app.nodes.analytics import analytics_node
from app.nodes.products import products_node
from app.nodes.customers import customers_node
from app.nodes.inventory import inventory_node
from app.nodes.support import support_node


def build_merchant_graph():
    """
    Constructs and compiles the StateGraph workflow.
    
    Graph Topology:
        START -> jev_router -> (router_node) -> [analytics, products, customers, inventory, support] -> END
    """
    workflow = StateGraph(MerchantState)

    # 1. Register Nodes
    workflow.add_node("jev_router", jev_router)
    workflow.add_node("analytics", analytics_node)
    workflow.add_node("products", products_node)
    workflow.add_node("customers", customers_node)
    workflow.add_node("inventory", inventory_node)
    workflow.add_node("support", support_node)

    # 2. Define Entry Point
    workflow.add_edge(START, "jev_router")

    # 3. Define Conditional Routing from jev_router
    workflow.add_conditional_edges(
        "jev_router",
        router_node,
        {
            "analytics": "analytics",
            "products": "products",
            "customers": "customers",
            "inventory": "inventory",
            "support": "support",
        }
    )

    # 4. Define Exit Transitions
    workflow.add_edge("analytics", END)
    workflow.add_edge("products", END)
    workflow.add_edge("customers", END)
    workflow.add_edge("inventory", END)
    workflow.add_edge("support", END)

    # 5. Compile the executable graph
    return workflow.compile()


# Singleton compiled graph instance for quick reuse
merchant_app = build_merchant_graph()


def run_merchant_agent(message: str) -> MerchantState:
    """Convenience execution helper for running a user message through the graph."""
    initial_state = MerchantState(message=message)
    result = merchant_app.invoke(initial_state)
    # Return as MerchantState object
    if isinstance(result, dict):
        return MerchantState(**result)
    return result
