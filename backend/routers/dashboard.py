# backend/routers/dashboard.py
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, cast, Float, extract
from backend.database import get_db
from backend.models.invoice_model import Invoice
from typing import Optional

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

@router.get("/stats")
def get_dashboard_stats(db: Session = Depends(get_db)):
    """Return general invoice statistics for dashboard"""
    try:
        total_invoices = db.query(func.count(Invoice.id)).scalar() or 0
        total_spent = db.query(func.sum(cast(Invoice.total_amount, Float))).scalar() or 0

        # Top vendors by frequency
        top_vendors_query = (
            db.query(Invoice.vendor, func.count(Invoice.id).label("count"))
            .group_by(Invoice.vendor)
            .order_by(func.count(Invoice.id).desc())
            .limit(5)
            .all()
        )

        top_vendors = [{"vendor": v[0], "count": v[1]} for v in top_vendors_query]

        return {
            "total_invoices": total_invoices,
            "total_spent": float(total_spent),
            "top_vendors": top_vendors,
        }

    except Exception as e:
        return {"error": str(e)}

@router.get("/filter")
def filter_invoices(
    category: Optional[str] = Query(None, description="Filter by category (e.g., 'مطعم', 'مقهى')"),
    month: Optional[int] = Query(None, ge=0, le=11, description="Filter by month (0-11, JavaScript style)"),
    payment_method: Optional[str] = Query(None, description="Filter by payment method"),
    db: Session = Depends(get_db)
):
    """
    Filter invoices with SQL queries for better performance
    Returns filtered invoices matching the criteria
    
    Note: month is 0-indexed (0=January, 11=December) to match JavaScript Date.getMonth()
    """
    try:
        # Start with base query
        query = db.query(Invoice)
        
        # 1. Filter by category (invoice_type or category JSON field)
        if category and category != "all":
            # Try to match invoice_type first (more efficient)
            query = query.filter(
                (Invoice.invoice_type == category) | 
                (Invoice.category.like(f'%"ar": "{category}"%'))
            )
        
        # 2. Filter by month (using SQL extract)
        # Note: SQL extract returns 1-12, so we add 1 to match
        if month is not None:
            query = query.filter(extract('month', Invoice.invoice_date) == month + 1)
        
        # 3. Filter by payment method (case-insensitive)
        if payment_method and payment_method != "all":
            query = query.filter(Invoice.payment_method.ilike(f"%{payment_method}%"))
        
        # Execute query
        invoices = query.order_by(Invoice.created_at.desc()).all()
        
        # Convert to dict
        result = []
        for inv in invoices:
            result.append({
                "id": inv.id,
                "vendor": inv.vendor,
                "invoice_number": inv.invoice_number,
                "invoice_date": inv.invoice_date.isoformat() if inv.invoice_date else None,
                "invoice_type": inv.invoice_type,
                "total_amount": str(inv.total_amount) if inv.total_amount else "0",
                "tax": str(inv.tax) if inv.tax else "0",
                "payment_method": inv.payment_method,
                "category": inv.category,
                "created_at": inv.created_at.isoformat() if inv.created_at else None,
                "ai_insight": inv.ai_insight,
            })
        
        return result
        
    except Exception as e:
        return {"error": str(e), "invoices": []}

@router.get("/filtered-stats")
def get_filtered_stats(
    category: Optional[str] = Query(None),
    month: Optional[int] = Query(None, ge=0, le=11),
    payment_method: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """
    Get statistics for filtered invoices
    Returns aggregated stats based on filters
    """
    try:
        # Start with base query
        query = db.query(Invoice)
        
        # Apply same filters as /filter endpoint
        if category and category != "all":
            query = query.filter(
                (Invoice.invoice_type == category) | 
                (Invoice.category.like(f'%"ar": "{category}"%'))
            )
        
        if month is not None:
            query = query.filter(extract('month', Invoice.invoice_date) == month + 1)
        
        if payment_method and payment_method != "all":
            query = query.filter(Invoice.payment_method.ilike(f"%{payment_method}%"))
        
        # Calculate stats
        total_invoices = query.count()
        total_spent = db.query(func.sum(cast(Invoice.total_amount, Float))).filter(
            Invoice.id.in_([inv.id for inv in query.all()])
        ).scalar() or 0.0
        
        total_tax = db.query(func.sum(cast(Invoice.tax, Float))).filter(
            Invoice.id.in_([inv.id for inv in query.all()])
        ).scalar() or 0.0
        
        avg_invoice = total_spent / total_invoices if total_invoices > 0 else 0.0
        
        return {
            "total_invoices": total_invoices,
            "total_spent": float(total_spent),
            "total_tax": float(total_tax),
            "avg_invoice": float(avg_invoice),
        }
        
    except Exception as e:
        return {"error": str(e)}

@router.get("/ping")
def ping():
    return {"message": "✅ Dashboard endpoint is live!"}
