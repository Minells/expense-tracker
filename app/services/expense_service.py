from sqlalchemy.orm import Session
from sqlalchemy import and_
from app.models import Expense, Category
from app.schemas import ExpenseCreate, ExpenseUpdate
from app.utils import NotFoundException, ForbiddenException, BadRequestException
from typing import List, Optional
from datetime import date


class ExpenseService:
    """Service layer for expense management."""
    
    @staticmethod
    def create_expense(db: Session, expense_data: ExpenseCreate, user_id: int) -> Expense:
        """
        Create a new expense for a user.
        
        Args:
            db: Database session
            expense_data: Expense creation data
            user_id: ID of the user creating the expense
            
        Returns:
            Created expense instance
            
        Raises:
            BadRequestException: If category doesn't exist or doesn't belong to user
        """
        category = db.query(Category).filter(
            and_(Category.id == expense_data.category_id, Category.user_id == user_id)
        ).first()
        
        if not category:
            raise BadRequestException(detail="Category not found or does not belong to you")
        
        new_expense = Expense(
            amount=expense_data.amount,
            date=expense_data.date,
            description=expense_data.description,
            category_id=expense_data.category_id,
            user_id=user_id
        )
        
        db.add(new_expense)
        db.commit()
        db.refresh(new_expense)
        
        return new_expense
    
    @staticmethod
    def get_user_expenses(
        db: Session,
        user_id: int,
        from_date: Optional[date] = None,
        to_date: Optional[date] = None,
        category_id: Optional[int] = None
    ) -> List[Expense]:
        """
        Retrieve expenses for a user with optional filters.
        
        Args:
            db: Database session
            user_id: User ID
            from_date: Optional filter for expenses from this date
            to_date: Optional filter for expenses up to this date
            category_id: Optional filter for specific category
            
        Returns:
            List of expense instances
        """
        query = db.query(Expense).filter(Expense.user_id == user_id)
        
        if from_date:
            query = query.filter(Expense.date >= from_date)
        
        if to_date:
            query = query.filter(Expense.date <= to_date)
        
        if category_id:
            query = query.filter(Expense.category_id == category_id)
        
        return query.order_by(Expense.date.desc()).all()
    
    @staticmethod
    def get_expense_by_id(db: Session, expense_id: int, user_id: int) -> Expense:
        """
        Retrieve an expense by ID, ensuring it belongs to the user.
        
        Args:
            db: Database session
            expense_id: Expense ID
            user_id: User ID for authorization check
            
        Returns:
            Expense instance
            
        Raises:
            NotFoundException: If expense doesn't exist
            ForbiddenException: If expense doesn't belong to user
        """
        expense = db.query(Expense).filter(Expense.id == expense_id).first()
        
        if not expense:
            raise NotFoundException(detail="Expense not found")
        
        if expense.user_id != user_id:
            raise ForbiddenException(detail="Not authorized to access this expense")
        
        return expense
    
    @staticmethod
    def update_expense(
        db: Session,
        expense_id: int,
        expense_data: ExpenseUpdate,
        user_id: int
    ) -> Expense:
        """
        Update an existing expense.
        
        Args:
            db: Database session
            expense_id: Expense ID
            expense_data: Updated expense data
            user_id: User ID for authorization check
            
        Returns:
            Updated expense instance
            
        Raises:
            NotFoundException: If expense doesn't exist
            ForbiddenException: If expense doesn't belong to user
            BadRequestException: If new category doesn't belong to user
        """
        expense = ExpenseService.get_expense_by_id(db, expense_id, user_id)
        
        update_data = expense_data.model_dump(exclude_unset=True)
        
        if "category_id" in update_data:
            category = db.query(Category).filter(
                and_(Category.id == update_data["category_id"], Category.user_id == user_id)
            ).first()
            
            if not category:
                raise BadRequestException(detail="Category not found or does not belong to you")
        
        for field, value in update_data.items():
            setattr(expense, field, value)
        
        db.commit()
        db.refresh(expense)
        
        return expense
    
    @staticmethod
    def delete_expense(db: Session, expense_id: int, user_id: int) -> None:
        """
        Delete an expense.
        
        Args:
            db: Database session
            expense_id: Expense ID
            user_id: User ID for authorization check
            
        Raises:
            NotFoundException: If expense doesn't exist
            ForbiddenException: If expense doesn't belong to user
        """
        expense = ExpenseService.get_expense_by_id(db, expense_id, user_id)
        
        db.delete(expense)
        db.commit()
