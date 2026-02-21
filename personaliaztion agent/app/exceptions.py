from fastapi import HTTPException, status


class PersonalizationException(Exception):
    """Base exception for personalization errors"""
    pass


class UserNotFoundException(PersonalizationException):
    """Raised when user profile is not found"""
    pass


class ModelNotAvailableException(PersonalizationException):
    """Raised when ML model is not available"""
    pass


class InvalidRequestException(PersonalizationException):
    """Raised when request validation fails"""
    pass


class DatabaseException(PersonalizationException):
    """Raised when database operation fails"""
    pass


def user_not_found_exception(user_id: str):
    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"User profile not found for user_id: {user_id}"
    )


def invalid_request_exception(message: str):
    return HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=message
    )


def internal_error_exception(message: str = "Internal server error"):
    return HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail=message
    )
