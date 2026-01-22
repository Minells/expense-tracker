from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date
from app.database import get_db
from app.schemas import ExpenseCreate, ExpenseResponse
from app.services import ExpenseService
from app.dependencies import get_current_user
from app.models import User

router = APIRouter(prefix="/expenses", tags=["Expenses"])


@router.post("/", response_model=ExpenseResponse, status_code=status.HTTP_201_CREATED)
def create_expense(
    expense_data: ExpenseCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Create a new expense record.
    
    - **amount**: Expense amount (must be positive, max 2 decimal places)
    - **date**: Date of the expense
    - **description**: Expense description
    - **category_id**: ID of the category (must belong to current user)
    
    The expense is automatically associated with the authenticated user.
    """
    expense = ExpenseService.create_expense(db, expense_data, current_user.id)
    return expense


@router.get("/", response_model=List[ExpenseResponse])
def get_expenses(
    from_date: Optional[date] = Query(None, description="Filter expenses from this date"),
    to_date: Optional[date] = Query(None, description="Filter expenses up to this date"),
    category_id: Optional[int] = Query(None, description="Filter by category ID"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Retrieve expenses for the authenticated user.
    
    Optional filters:
    - **from_date**: Get expenses from this date onwards
    - **to_date**: Get expenses up to this date
    - **category_id**: Get expenses only from specific category
    
    Results are ordered by date (newest first).
    """
    expenses = ExpenseService.get_user_expenses(
        db, current_user.id, from_date, to_date, category_id
    )
    return expenses


@router.get("/{expense_id}", response_model=ExpenseResponse)
def get_expense(
    expense_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Retrieve a specific expense by ID.
    
    Returns 404 if expense doesn't exist.
    Returns 403 if expense doesn't belong to the current user.
    """
    expense = ExpenseService.get_expense_by_id(db, expense_id, current_user.id)
    return expense


@router.delete("/{expense_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_expense(
    expense_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Delete an expense record.
    """
    ExpenseService.delete_expense(db, expense_id, current_user.id)
    return None
