from decimal import Decimal
from pydantic import BaseModel
from datetime import date


class MonthlyReport(BaseModel):
    """Schema for monthly expense report."""
    year: int
    month: int
    total_expenses: Decimal
    expense_count: int
    
    class Config:
        from_attributes = True


class CategorySummary(BaseModel):
    """Schema for expense summary by category."""
    category_id: int
    category_name: str
    total_amount: Decimal
    expense_count: int
    
    class Config:
        from_attributes = True


class DateRangeReport(BaseModel):
    """Schema for date range expense report."""
    start_date: date
    end_date: date
    total_expenses: Decimal
    expense_count: int
    by_category: list[CategorySummary]
    
    class Config:
        from_attributes = True
