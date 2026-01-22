from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import UserCreate, UserResponse, Token
from app.services import AuthService

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """
    Register a new user account.
    
    - **email**: Valid email address (must be unique)
    - **password**: Password for the account
    
    Returns the created user information (without password).
    """
    user = AuthService.register_user(db, user_data)
    return user


@router.post("/login", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """
    Authenticate and receive a JWT access token.
    
    - **username**: User email (OAuth2 spec uses 'username')
    - **password**: User password
    
    Returns a JWT token to use for authenticated requests.
    """
    user = AuthService.authenticate_user(db, form_data.username, form_data.password)
    access_token = AuthService.create_user_token(user)
    
    return Token(access_token=access_token, token_type="bearer")
