from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field, ConfigDict


class MerchantQuery(BaseModel):
    """Structured extraction of merchant intent parameters."""
    metric: Optional[str] = Field(
        default=None, 
        description="The primary metric of interest (e.g. 'sales', 'revenue', 'order_count', 'stock')"
    )
    time_period: Optional[str] = Field(
        default=None, 
        description="The relevant time frame (e.g. 'yesterday', 'last_week', 'this_month')"
    )
    entity: Optional[str] = Field(
        default=None, 
        description="The entity or segment being queried (e.g. 'overall_business', 'top_products', 'repeat_customers')"
    )


class MerchantState(BaseModel):
    """
    Central state container for the Merchant Intelligence Router agent.
    Maintains user input, classification metadata, retrieved data, and the final response.
    """
    model_config = ConfigDict(arbitrary_types_allowed=True)

    message: str = Field(..., description="The original natural language message from the merchant")
    intent: Optional[str] = Field(default=None, description="The classified intent category")
    confidence: float = Field(default=0.0, ge=0.0, le=1.0, description="Confidence score of classification (0.0 to 1.0)")
    structured_query: Optional[MerchantQuery] = Field(default=None, description="Extracted structured query parameters")
    data: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Deterministic business calculation results")
    reply: Optional[str] = Field(default=None, description="The final response delivered to the merchant")
