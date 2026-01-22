from sqlalchemy.orm import Session
from app.models import Category
from app.schemas import CategoryCreate, CategoryUpdate
from app.utils import NotFoundException, ForbiddenException
from typing import List


class CategoryService:
    """Service layer for category management."""
    
    @staticmethod
    def create_category(db: Session, category_data: CategoryCreate, user_id: int) -> Category:
        """
        Create a new category for a user.
        
        Args:
            db: Database session
            category_data: Category creation data
            user_id: ID of the user creating the category
            
        Returns:
            Created category instance
        """
        new_category = Category(
            name=category_data.name,
            description=category_data.description,
            user_id=user_id
        )
        
        db.add(new_category)
        db.commit()
        db.refresh(new_category)
        
        return new_category
    
    @staticmethod
    def get_user_categories(db: Session, user_id: int) -> List[Category]:
        """
        Retrieve all categories for a specific user.
        
        Args:
            db: Database session
            user_id: User ID
            
        Returns:
            List of category instances
        """
        return db.query(Category).filter(Category.user_id == user_id).all()
    
    @staticmethod
    def get_category_by_id(db: Session, category_id: int, user_id: int) -> Category:
        """
        Retrieve a category by ID, ensuring it belongs to the user.
        
        Args:
            db: Database session
            category_id: Category ID
            user_id: User ID for authorization check
            
        Returns:
            Category instance
            
        Raises:
            NotFoundException: If category doesn't exist
            ForbiddenException: If category doesn't belong to user
        """
        category = db.query(Category).filter(Category.id == category_id).first()
        
        if not category:
            raise NotFoundException(detail="Category not found")
        
        if category.user_id != user_id:
            raise ForbiddenException(detail="Not authorized to access this category")
        
        return category
    
    @staticmethod
    def update_category(
        db: Session,
        category_id: int,
        category_data: CategoryUpdate,
        user_id: int
    ) -> Category:
        """
        Update an existing category.
        
        Args:
            db: Database session
            category_id: Category ID
            category_data: Updated category data
            user_id: User ID for authorization check
            
        Returns:
            Updated category instance
            
        Raises:
            NotFoundException: If category doesn't exist
            ForbiddenException: If category doesn't belong to user
        """
        category = CategoryService.get_category_by_id(db, category_id, user_id)
        
        update_data = category_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(category, field, value)
        
        db.commit()
        db.refresh(category)
        
        return category
    
    @staticmethod
    def delete_category(db: Session, category_id: int, user_id: int) -> None:
        """
        Delete a category.
        
        Args:
            db: Database session
            category_id: Category ID
            user_id: User ID for authorization check
            
        Raises:
            NotFoundException: If category doesn't exist
            ForbiddenException: If category doesn't belong to user
        """
        category = CategoryService.get_category_by_id(db, category_id, user_id)
        
        db.delete(category)
        db.commit()
