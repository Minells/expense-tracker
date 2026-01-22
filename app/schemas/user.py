from pydantic import BaseModel, EmailStr
from datetime import datetime


class UserBase(BaseModel):
    """Base user schema with common attributes."""
    email: EmailStr


class UserCreate(UserBase):
    """Schema for user registration."""
    password: str


class UserResponse(UserBase):
    """Schema for user data in API responses."""
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


class UserInDB(UserBase):
    """Internal schema representing user as stored in database."""
    id: int
    hashed_password: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
