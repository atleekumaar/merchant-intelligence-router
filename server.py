"""
FastAPI Backend Server for Merchant Intelligence Router.
Exposes REST endpoints for intent classification, LangGraph execution, and serves the frontend.
"""

import sys
import os
from typing import Dict, Any, Optional
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

# Ensure app package is in path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.state import MerchantState, Intent
from app.classifier import default_classifier, normalize_text
from app.router import get_confidence_threshold, router_node
from app.graph import run_merchant_agent
from app.choices import MERCHANT_CHOICES
from app.data.mock_data import (
    get_sales_analytics,
    get_top_products,
    get_top_customers,
    get_inventory_summary,
    PRODUCTS_DATA,
    CUSTOMERS_DATA,
    DAILY_SALES_DATA,
    INVENTORY_DATA
)

app = FastAPI(
    title="Merchant Intelligence Router API",
    description="Interactive backend API for Jev-style Intent Classification and LangGraph Routing",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class QueryRequest(BaseModel):
    message: str


class QueryResponse(BaseModel):
    message: str
    intent: Optional[str]
    confidence: float
    threshold: float
    passes_threshold: bool
    routed_node: str
    reply: str
    structured_query: Optional[Dict[str, Any]] = None
    data: Optional[Dict[str, Any]] = None
    scores: Dict[str, float] = {}


@app.post("/api/query", response_model=QueryResponse)
def execute_query(req: QueryRequest):
    """Executes the complete LangGraph StateGraph pipeline for a merchant query."""
    if not req.message.strip():
        raise HTTPException(status_code=400, detail="Query message cannot be empty.")

    # 1. Run through Jev-compatible classifier for score inspection
    explanation = default_classifier.explain(req.message)
    threshold = get_confidence_threshold()

    # 2. Run through full LangGraph pipeline
    final_state = run_merchant_agent(req.message)
    
    intent_str = final_state.intent.value if isinstance(final_state.intent, Intent) else str(final_state.intent or "support")
    routed_to = router_node(final_state)

    structured_dict = None
    if final_state.structured_query:
        structured_dict = {k: v for k, v in final_state.structured_query.model_dump().items() if v is not None}

    return QueryResponse(
        message=req.message,
        intent=intent_str,
        confidence=final_state.confidence,
        threshold=threshold,
        passes_threshold=final_state.confidence >= threshold,
        routed_node=routed_to,
        reply=final_state.reply,
        structured_query=structured_dict,
        data=final_state.data,
        scores=explanation["intent_scores"]
    )


@app.post("/api/classify")
def classify_message(req: QueryRequest):
    """Returns classification scores without executing downstream business workflows."""
    return default_classifier.explain(req.message)


@app.get("/api/choices")
def get_choices():
    """Returns all available Choice categories, descriptions, and representative phrases."""
    return [choice.model_dump() for choice in MERCHANT_CHOICES]


@app.get("/api/mock-data")
def get_mock_datasets():
    """Returns raw deterministic mock data for frontend inspection."""
    return {
        "products": PRODUCTS_DATA,
        "customers": CUSTOMERS_DATA,
        "daily_sales": DAILY_SALES_DATA,
        "inventory": INVENTORY_DATA,
        "analytics_summary": get_sales_analytics(),
        "inventory_summary": get_inventory_summary()
    }


# Ensure static files directory exists
STATIC_DIR = os.path.join(os.path.dirname(__file__), "static")
os.makedirs(STATIC_DIR, exist_ok=True)

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


@app.get("/")
def serve_index():
    """Serve the single-page frontend application."""
    index_path = os.path.join(STATIC_DIR, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"message": "Merchant Intelligence Router API is active. Frontend is loading."}


if __name__ == "__main__":
    import uvicorn
    print("Starting Merchant Intelligence Router server at http://localhost:8000 ...")
    uvicorn.run("server:app", host="127.0.0.1", port=8000, reload=True)
