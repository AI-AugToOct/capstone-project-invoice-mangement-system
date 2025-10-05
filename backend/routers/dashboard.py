# backend/routers/dashboard.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func, cast, Float
from backend.database import get_db
from backend.models.invoice_model import Invoice

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

@router.get("/ping")
def ping():
    return {"message": "✅ Dashboard endpoint is live!"}
