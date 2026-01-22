from pydantic import BaseModel, Field, field_validator
from datetime import date, datetime
from decimal import Decimal
from typing import Optional


class ExpenseBase(BaseModel):
    """Base expense schema with common attributes."""
    amount: Decimal = Field(..., gt=0, decimal_places=2, description="Expense amount, must be positive")
    date: date
    description: str = Field(..., min_length=1, max_length=500)
    category_id: int


class ExpenseCreate(ExpenseBase):
    """Schema for creating a new expense."""
    
    @field_validator('amount')
    @classmethod
    def validate_amount(cls, v: Decimal) -> Decimal:
        if v <= 0:
            raise ValueError('Amount must be positive')
        return v.quantize(Decimal('0.01'))


class ExpenseUpdate(BaseModel):
    """Schema for updating an existing expense."""
    amount: Optional[Decimal] = Field(None, gt=0, decimal_places=2)
    date: Optional[date] = None
    description: Optional[str] = Field(None, min_length=1, max_length=500)
    category_id: Optional[int] = None


class ExpenseResponse(ExpenseBase):
    """Schema for expense data in API responses."""
    id: int
    user_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


class ExpenseWithCategory(ExpenseResponse):
    """Schema for expense with category details."""
    category_name: str
    
    class Config:
        from_attributes = True
