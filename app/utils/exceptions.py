from fastapi import HTTPException, status


class BaseAPIException(HTTPException):
    """Base class for API exceptions."""
    
    def __init__(self, detail: str, status_code: int = status.HTTP_400_BAD_REQUEST):
        super().__init__(status_code=status_code, detail=detail)


class NotFoundException(BaseAPIException):
    """Raised when a requested resource is not found."""
    
    def __init__(self, detail: str = "Resource not found"):
        super().__init__(detail=detail, status_code=status.HTTP_404_NOT_FOUND)


class UnauthorizedException(BaseAPIException):
    """Raised when authentication fails or token is invalid."""
    
    def __init__(self, detail: str = "Could not validate credentials"):
        super().__init__(
            detail=detail,
            status_code=status.HTTP_401_UNAUTHORIZED
        )


class ForbiddenException(BaseAPIException):
    """Raised when user doesn't have permission to access a resource."""
    
    def __init__(self, detail: str = "Not authorized to access this resource"):
        super().__init__(detail=detail, status_code=status.HTTP_403_FORBIDDEN)


class BadRequestException(BaseAPIException):
    """Raised when request data is invalid."""
    
    def __init__(self, detail: str = "Invalid request data"):
        super().__init__(detail=detail, status_code=status.HTTP_400_BAD_REQUEST)


class ConflictException(BaseAPIException):
    """Raised when there's a conflict with existing data."""
    
    def __init__(self, detail: str = "Resource already exists"):
        super().__init__(detail=detail, status_code=status.HTTP_409_CONFLICT)
