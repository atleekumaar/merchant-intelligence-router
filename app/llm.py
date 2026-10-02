"""
LLM Integration module for Merchant Intelligence Router.
Provides structured entity extraction (MerchantQuery) and natural language explanations.
Strictly decoupled from deterministic calculation numbers.
"""

import os
from typing import Optional, Dict, Any

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

from app.state import MerchantQuery


def extract_structured_query(message: str) -> MerchantQuery:
    """
    Extracts structured query parameters (metric, time_period, entity) using Pydantic.
    Attempts to use OpenAI structured output if API key is provided; otherwise uses
    deterministic heuristic parsing.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key:
        try:
            from langchain_openai import ChatOpenAI
            llm = ChatOpenAI(model="gpt-4o-mini", temperature=0, api_key=api_key)
            structured_llm = llm.with_structured_output(MerchantQuery)
            extracted = structured_llm.invoke(
                f"Extract the relevant business parameters from this merchant query: '{message}'"
            )
            if isinstance(extracted, MerchantQuery):
                return extracted
        except Exception:
            pass

    # Deterministic fallback parser
    return _heuristic_query_extraction(message)


def _heuristic_query_extraction(message: str) -> MerchantQuery:
    """Deterministic parameter extraction fallback."""
    msg = message.lower()
    
    # Extract metric
    metric = None
    if any(w in msg for w in ["sale", "sales", "revenue", "earnings", "profit"]):
        metric = "sales_revenue"
    elif any(w in msg for w in ["product", "item", "sku", "selling"]):
        metric = "products"
    elif any(w in msg for w in ["customer", "buyer", "client"]):
        metric = "customers"
    elif any(w in msg for w in ["inventory", "stock", "quantity", "unit"]):
        metric = "inventory"

    # Extract time period
    time_period = None
    if "yesterday" in msg:
        time_period = "yesterday"
    elif "today" in msg:
        time_period = "today"
    elif "last week" in msg or "past week" in msg:
        time_period = "last_week"
    elif "month" in msg:
        time_period = "this_month"
    else:
        time_period = "current_period"

    # Extract entity
    entity = None
    if "top" in msg or "best" in msg:
        entity = "top_performers"
    elif "low" in msg or "critical" in msg or "drop" in msg or "fall" in msg:
        entity = "underperforming_or_alerts"
    else:
        entity = "overall_business"

    return MerchantQuery(metric=metric, time_period=time_period, entity=entity)


def generate_llm_explanation(prompt: str, context_data: Dict[str, Any]) -> Optional[str]:
    """
    Generates a natural-language synthesis given deterministic data numbers.
    Never hallucinates numbers—only explains the supplied context.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return None

    try:
        from langchain_openai import ChatOpenAI
        llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.3, api_key=api_key)
        system_instruction = (
            "You are VyaparMitra, an executive AI merchant consultant. "
            "Explain the provided deterministic business data in a polite, actionable, and encouraging tone. "
            "CRITICAL: Do NOT invent or alter any numerical values. Use only the provided numbers."
        )
        response = llm.invoke([
            {"role": "system", "content": system_instruction},
            {"role": "user", "content": f"Query: {prompt}\nContext Data: {context_data}"}
        ])
        return str(response.content)
    except Exception:
        return None
