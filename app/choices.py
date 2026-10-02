"""
Local Choice abstraction for Merchant Intelligence Router.
Reproduces the typed choice structure inspired by Jev's discrete decision model locally.

NOTE: This is a local compatible abstraction for zero-cost development and education.
It is not the official TypeSafe AI Jev service.
"""

from typing import List
from pydantic import BaseModel, Field


class Choice(BaseModel):
    """
    Represents a discrete classification choice with semantic description and training examples.
    """
    name: str = Field(..., description="Unique categorical intent name")
    description: str = Field(..., description="Semantic purpose and scope of the intent category")
    examples: List[str] = Field(default_factory=list, description="Representative example phrases")


MERCHANT_CHOICES: List[Choice] = [
    Choice(
        name="analytics",
        description="Questions about sales volume, revenue fluctuations, growth trends, financial performance, and historical comparisons",
        examples=[
            "how much did I sell today",
            "show today's sales",
            "what was my revenue this week",
            "sales performance",
            "how are my sales doing",
            "why were my sales low yesterday",
            "why did revenue drop yesterday",
            "show my revenue trend",
            "how much money did I make today",
            "what was my daily turnover",
            "compare sales between yesterday and today",
            "show financial earnings overview",
            "how is my business revenue growth"
        ]
    ),
    Choice(
        name="products",
        description="Questions regarding top products, best-selling SKUs, product performance, item rankings, and catalog details",
        examples=[
            "show my products",
            "best selling products",
            "which product sells the most",
            "product performance",
            "show product catalog",
            "show me my top 5 products",
            "what is my best selling product",
            "top performing items in catalog",
            "which SKU has the highest sales",
            "list all active products and prices",
            "show highest rated product items",
            "most popular items among buyers"
        ]
    ),
    Choice(
        name="customers",
        description="Questions about customer behavior, top buyers, repeat purchasers, customer spend analysis, and VIP segmentation",
        examples=[
            "show my customers",
            "who are my repeat customers",
            "customer information",
            "which customers buy frequently",
            "customer analysis",
            "which customers bought from me most",
            "who are my best customers",
            "show highest spending clients",
            "list VIP customer accounts",
            "who is my most loyal buyer",
            "show top customer purchase history",
            "who spent the most money at my store"
        ]
    ),
    Choice(
        name="inventory",
        description="Questions concerning stock availability, low inventory warnings, reorder thresholds, out-of-stock items, and warehouse levels",
        examples=[
            "which products are low in stock",
            "show inventory",
            "what needs to be restocked",
            "stock levels",
            "inventory status",
            "how much inventory do I have",
            "how many items are left",
            "which items are out of stock",
            "check remaining stock quantity",
            "what should I reorder now",
            "show critical stock alerts",
            "available units in warehouse"
        ]
    ),
    Choice(
        name="support",
        description="Questions regarding how to use the dashboard, general troubleshooting, help requests, system navigation, and guidance",
        examples=[
            "help me",
            "I don't understand",
            "what can you do",
            "how does this work",
            "I need assistance",
            "how do I use this dashboard",
            "guide me through the system",
            "what features are available",
            "how can this tool help my store",
            "help with navigation",
            "hello who are you",
            "I am confused about this assistant"
        ]
    )
]
