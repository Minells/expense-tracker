from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class CategoryBase(BaseModel):
    """Base category schema with common attributes."""
    name: str
    description: Optional[str] = None


class CategoryCreate(CategoryBase):
    """Schema for creating a new category."""
    pass


class CategoryUpdate(BaseModel):
    """Schema for updating an existing category."""
    name: Optional[str] = None
    description: Optional[str] = None


class CategoryResponse(CategoryBase):
    """Schema for category data in API responses."""
    id: int
    user_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True
