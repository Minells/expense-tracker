from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import JWTError
from app.database import get_db
from app.models import User
from app.utils import decode_access_token, UnauthorizedException
from app.services import AuthService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    """
    Dependency to extract and validate the current authenticated user from JWT token.
    
    Args:
        token: JWT token from Authorization header
        db: Database session
        
    Returns:
        Authenticated User instance
        
    Raises:
        UnauthorizedException: If token is invalid or user not found
    """
    payload = decode_access_token(token)
    
    if payload is None:
        raise UnauthorizedException(detail="Could not validate credentials")
    
    user_id: str = payload.get("sub")
    if user_id is None:
        raise UnauthorizedException(detail="Could not validate credentials")
    
    try:
        user_id_int = int(user_id)
    except ValueError:
        raise UnauthorizedException(detail="Invalid token payload")
    
    user = AuthService.get_user_by_id(db, user_id_int)
    if user is None:
        raise UnauthorizedException(detail="User not found")
    
    return user
