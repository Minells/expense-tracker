from pydantic import BaseModel


class Token(BaseModel):
    """Schema for JWT token response."""
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """Schema for data encoded in JWT token."""
    user_id: int
    email: str
