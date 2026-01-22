from sqlalchemy.orm import Session
from app.models import User
from app.schemas import UserCreate
from app.utils import hash_password, verify_password, create_access_token, ConflictException, UnauthorizedException
from datetime import timedelta


class AuthService:
    """Service layer for authentication and user management."""
    
    @staticmethod
    def register_user(db: Session, user_data: UserCreate) -> User:
        """
        Register a new user with hashed password.
        
        Args:
            db: Database session
            user_data: User registration data
            
        Returns:
            Created user instance
            
        Raises:
            ConflictException: If email already exists
        """
        existing_user = db.query(User).filter(User.email == user_data.email).first()
        if existing_user:
            raise ConflictException(detail="Email already registered")
        
        hashed_password = hash_password(user_data.password)
        
        new_user = User(
            email=user_data.email,
            hashed_password=hashed_password
        )
        
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        
        return new_user
    
    @staticmethod
    def authenticate_user(db: Session, email: str, password: str) -> User:
        """
        Authenticate user by email and password.
        
        Args:
            db: Database session
            email: User email
            password: Plaintext password
            
        Returns:
            Authenticated user instance
            
        Raises:
            UnauthorizedException: If credentials are invalid
        """
        user = db.query(User).filter(User.email == email).first()
        
        if not user or not verify_password(password, user.hashed_password):
            raise UnauthorizedException(detail="Incorrect email or password")
        
        return user
    
    @staticmethod
    def create_user_token(user: User) -> str:
        """
        Create JWT token for authenticated user.
        
        Args:
            user: User instance
            
        Returns:
            JWT access token string
        """
        token_data = {
            "sub": str(user.id),
            "email": user.email
        }
        
        return create_access_token(data=token_data)
    
    @staticmethod
    def get_user_by_id(db: Session, user_id: int) -> User | None:
        """
        Retrieve user by ID.
        
        Args:
            db: Database session
            user_id: User ID
            
        Returns:
            User instance if found, None otherwise
        """
        return db.query(User).filter(User.id == user_id).first()
