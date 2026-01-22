from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.schemas import CategoryCreate, CategoryResponse
from app.services import CategoryService
from app.dependencies import get_current_user
from app.models import User

router = APIRouter(prefix="/categories", tags=["Categories"])


@router.post("/", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
def create_category(
    category_data: CategoryCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Create a new expense category.
    
    - **name**: Category name (required)
    - **description**: Optional category description
    
    Each category is associated with the authenticated user.
    """
    category = CategoryService.create_category(db, category_data, current_user.id)
    return category


@router.get("/", response_model=List[CategoryResponse])
def get_categories(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Retrieve all categories for the authenticated user.
    
    Returns a list of all categories created by the current user.
    """
    categories = CategoryService.get_user_categories(db, current_user.id)
    return categories


@router.get("/{category_id}", response_model=CategoryResponse)
def get_category(
    category_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Retrieve a specific category by ID.
    
    Returns 404 if category doesn't exist.
    Returns 403 if category doesn't belong to the current user.
    """
    category = CategoryService.get_category_by_id(db, category_id, current_user.id)
    return category


@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(
    category_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Delete a category.
    
    Warning: This will also delete all expenses associated with this category.
    """
    CategoryService.delete_category(db, category_id, current_user.id)
    return None
