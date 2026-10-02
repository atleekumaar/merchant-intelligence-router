"""
Deterministic mock dataset and retrieval helpers for Merchant Intelligence Router.
All monetary values are represented in Indian Rupees (INR - ₹).
"""

from typing import List, Dict, Any, Optional

PRODUCTS_DATA: List[Dict[str, Any]] = [
    {"id": "PROD-001", "name": "Organic Green Tea (250g)", "category": "Beverages", "price": 450, "units_sold": 1240, "rating": 4.8},
    {"id": "PROD-002", "name": "Cold-Pressed Mustard Oil (1L)", "category": "Cooking", "price": 280, "units_sold": 980, "rating": 4.6},
    {"id": "PROD-003", "name": "Whole Wheat Atta (5kg)", "category": "Staples", "price": 310, "units_sold": 850, "rating": 4.5},
    {"id": "PROD-004", "name": "Raw Wildflower Honey (500g)", "category": "Sweeteners", "price": 520, "units_sold": 620, "rating": 4.9},
    {"id": "PROD-005", "name": "Alphonso Mango Pulp (850g)", "category": "Preserves", "price": 390, "units_sold": 410, "rating": 4.7},
]

CUSTOMERS_DATA: List[Dict[str, Any]] = [
    {"id": "CUST-101", "name": "Aarav Sharma", "orders_count": 28, "total_spent": 42500, "city": "Mumbai", "segment": "VIP"},
    {"id": "CUST-102", "name": "Priya Patel", "orders_count": 22, "total_spent": 31800, "city": "Ahmedabad", "segment": "VIP"},
    {"id": "CUST-103", "name": "Rohan Gupta", "orders_count": 15, "total_spent": 19400, "city": "Delhi", "segment": "Regular"},
    {"id": "CUST-104", "name": "Sneha Iyer", "orders_count": 12, "total_spent": 14200, "city": "Bengaluru", "segment": "Regular"},
    {"id": "CUST-105", "name": "Vikram Singh", "orders_count": 3, "total_spent": 3100, "city": "Jaipur", "segment": "New"},
]

DAILY_SALES_DATA: List[Dict[str, Any]] = [
    {"date": "2026-09-28", "revenue": 48500, "orders": 65, "avg_order_value": 746.15},
    {"date": "2026-09-29", "revenue": 52000, "orders": 72, "avg_order_value": 722.22},
    {"date": "2026-09-30", "revenue": 56400, "orders": 78, "avg_order_value": 723.08},
    {"date": "2026-10-01", "revenue": 31200, "orders": 41, "avg_order_value": 760.98},  # Low sales day (yesterday)
    {"date": "2026-10-02", "revenue": 49100, "orders": 66, "avg_order_value": 743.94},  # Today
]

INVENTORY_DATA: List[Dict[str, Any]] = [
    {"id": "PROD-001", "name": "Organic Green Tea (250g)", "stock_quantity": 18, "reorder_threshold": 30, "status": "LOW_STOCK"},
    {"id": "PROD-002", "name": "Cold-Pressed Mustard Oil (1L)", "stock_quantity": 85, "reorder_threshold": 25, "status": "OPTIMAL"},
    {"id": "PROD-003", "name": "Whole Wheat Atta (5kg)", "stock_quantity": 4, "reorder_threshold": 20, "status": "CRITICAL"},
    {"id": "PROD-004", "name": "Raw Wildflower Honey (500g)", "stock_quantity": 42, "reorder_threshold": 15, "status": "OPTIMAL"},
    {"id": "PROD-005", "name": "Alphonso Mango Pulp (850g)", "stock_quantity": 0, "reorder_threshold": 10, "status": "OUT_OF_STOCK"},
]


# Deterministic Data Retrieval & Computation Functions

def get_sales_analytics(days: int = 5) -> Dict[str, Any]:
    """Calculate deterministic sales metrics comparing yesterday vs day before yesterday."""
    recent_sales = DAILY_SALES_DATA[-days:]
    if len(recent_sales) >= 2:
        yesterday = recent_sales[-2]
        day_before = recent_sales[-3]
        rev_yesterday = yesterday["revenue"]
        rev_day_before = day_before["revenue"]
        pct_change = ((rev_yesterday - rev_day_before) / rev_day_before) * 100
        order_pct_change = ((yesterday["orders"] - day_before["orders"]) / day_before["orders"]) * 100
    else:
        yesterday = recent_sales[-1]
        day_before = {}
        pct_change = 0.0
        order_pct_change = 0.0

    total_revenue = sum(item["revenue"] for item in recent_sales)
    total_orders = sum(item["orders"] for item in recent_sales)

    return {
        "recent_sales": recent_sales,
        "yesterday": yesterday,
        "day_before": day_before,
        "revenue_pct_change": round(pct_change, 2),
        "orders_pct_change": round(order_pct_change, 2),
        "total_revenue": total_revenue,
        "total_orders": total_orders,
    }


def get_top_products(limit: int = 5) -> List[Dict[str, Any]]:
    """Return top products sorted strictly by units sold."""
    return sorted(PRODUCTS_DATA, key=lambda p: p["units_sold"], reverse=True)[:limit]


def get_top_customers(limit: int = 5) -> List[Dict[str, Any]]:
    """Return top customers sorted strictly by total spend."""
    return sorted(CUSTOMERS_DATA, key=lambda c: c["total_spent"], reverse=True)[:limit]


def get_inventory_summary() -> Dict[str, Any]:
    """Return inventory health breakdown and items needing restock."""
    low_stock = [item for item in INVENTORY_DATA if item["stock_quantity"] <= item["reorder_threshold"]]
    out_of_stock = [item for item in INVENTORY_DATA if item["stock_quantity"] == 0]
    total_items = len(INVENTORY_DATA)
    total_units = sum(item["stock_quantity"] for item in INVENTORY_DATA)

    return {
        "total_unique_items": total_items,
        "total_units_in_stock": total_units,
        "low_stock_items": low_stock,
        "out_of_stock_items": out_of_stock,
        "all_inventory": INVENTORY_DATA
    }
