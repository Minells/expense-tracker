from sqlalchemy.orm import Session
from sqlalchemy import func, extract
from app.models import Expense, Category
from app.schemas import MonthlyReport, CategorySummary
from typing import List
from decimal import Decimal


class ReportService:
    """Service layer for expense reporting and analytics."""
    
    @staticmethod
    def get_monthly_report(db: Session, user_id: int, year: int, month: int) -> MonthlyReport:
        """
        Generate a monthly expense report for a user.
        
        Args:
            db: Database session
            user_id: User ID
            year: Year for the report
            month: Month for the report (1-12)
            
        Returns:
            MonthlyReport with aggregated expense data
        """
        result = db.query(
            func.coalesce(func.sum(Expense.amount), 0).label("total"),
            func.count(Expense.id).label("count")
        ).filter(
            Expense.user_id == user_id,
            extract('year', Expense.date) == year,
            extract('month', Expense.date) == month
        ).first()
        
        return MonthlyReport(
            year=year,
            month=month,
            total_expenses=Decimal(str(result.total)),
            expense_count=result.count
        )
    
    @staticmethod
    def get_expenses_by_category(
        db: Session,
        user_id: int,
        year: int,
        month: int
    ) -> List[CategorySummary]:
        """
        Get expense breakdown by category for a specific month.
        
        Args:
            db: Database session
            user_id: User ID
            year: Year for the report
            month: Month for the report (1-12)
            
        Returns:
            List of CategorySummary with expenses grouped by category
        """
        results = db.query(
            Category.id,
            Category.name,
            func.sum(Expense.amount).label("total"),
            func.count(Expense.id).label("count")
        ).join(
            Expense, Expense.category_id == Category.id
        ).filter(
            Expense.user_id == user_id,
            extract('year', Expense.date) == year,
            extract('month', Expense.date) == month
        ).group_by(
            Category.id, Category.name
        ).all()
        
        return [
            CategorySummary(
                category_id=result.id,
                category_name=result.name,
                total_amount=Decimal(str(result.total)),
                expense_count=result.count
            )
            for result in results
        ]
