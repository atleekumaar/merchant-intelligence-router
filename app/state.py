"""
Type-safe state definitions for Merchant Intelligence Router.
"""

from enum import Enum
from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field, ConfigDict


class Intent(str, Enum):
    """Supported merchant intent categories."""
    ANALYTICS = "analytics"
    PRODUCTS = "products"
    CUSTOMERS = "customers"
    INVENTORY = "inventory"
    SUPPORT = "support"


class ClassificationResult(BaseModel):
    """Standardized prediction output from the intent classifier."""
    intent: Intent = Field(..., description="The predicted intent category")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence score between 0.0 and 1.0")
    scores: Dict[str, float] = Field(default_factory=dict, description="Raw similarity distribution across all choices")


class MerchantQuery(BaseModel):
    """Structured extraction of merchant intent parameters."""
    metric: Optional[str] = Field(
        default=None, 
        description="The primary metric of interest (e.g. 'sales', 'revenue', 'order_count', 'stock')"
    )
    time_period: Optional[str] = Field(
        default=None, 
        description="The relevant time frame (e.g. 'yesterday', 'today', 'last_week', 'this_month')"
    )
    entity: Optional[str] = Field(
        default=None, 
        description="The entity or segment being queried (e.g. 'overall_business', 'top_products', 'repeat_customers')"
    )


class MerchantState(BaseModel):
    """
    Central state container flowing through the LangGraph StateGraph.
    """
    model_config = ConfigDict(arbitrary_types_allowed=True)

    message: str = Field(..., description="Original user message")
    intent: Optional[Intent] = Field(default=None, description="Classified intent")
    confidence: float = Field(default=0.0, ge=0.0, le=1.0, description="Confidence score")
    structured_query: Optional[MerchantQuery] = Field(default=None, description="Extracted query filters")
    data: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Deterministic business calculation data")
    reply: str = Field(default="", description="Final response message for the merchant")
