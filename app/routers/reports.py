from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.schemas import MonthlyReport, CategorySummary
from app.services import ReportService
from app.dependencies import get_current_user
from app.models import User

router = APIRouter(prefix="/reports", tags=["Reports"])


@router.get("/monthly", response_model=MonthlyReport)
def get_monthly_report(
    year: int = Query(..., ge=2000, le=2100, description="Year for the report"),
    month: int = Query(..., ge=1, le=12, description="Month for the report (1-12)"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get monthly expense summary.
    
    - **year**: Year for the report
    - **month**: Month for the report (1-12)
    
    Returns aggregated expense data including:
    - Total expenses for the month
    - Count of expense records
    """
    report = ReportService.get_monthly_report(db, current_user.id, year, month)
    return report


@router.get("/monthly/by-category", response_model=List[CategorySummary])
def get_monthly_by_category(
    year: int = Query(..., ge=2000, le=2100, description="Year for the report"),
    month: int = Query(..., ge=1, le=12, description="Month for the report (1-12)"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get monthly expense breakdown by category.
    
    - **year**: Year for the report
    - **month**: Month for the report (1-12)
    
    Returns expense totals grouped by category for the specified month.
    """
    report = ReportService.get_expenses_by_category(db, current_user.id, year, month)
    return report
