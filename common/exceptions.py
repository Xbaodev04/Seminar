from typing import Any, Dict, Optional

class BaseAppException(Exception):
    """Base exception class for the application"""
    def __init__(
        self,
        message: str,
        status_code: int = 400,
        error_details: Optional[str] = None
    ):
        self.message = message
        self.status_code = status_code
        self.error_details = error_details
        super().__init__(self.message)

class NotFoundError(BaseAppException):
    """Exception raised when a resource is not found"""
    def __init__(self, message: str = "Resource not found", error_details: Optional[str] = None):
        super().__init__(message=message, status_code=404, error_details=error_details)

class ValidationError(BaseAppException):
    """Exception raised when input validation fails"""
    def __init__(self, message: str = "Validation failed", error_details: Optional[str] = None):
        super().__init__(message=message, status_code=422, error_details=error_details)

class UnauthorizedError(BaseAppException):
    """Exception raised for authentication errors"""
    def __init__(self, message: str = "Unauthorized access", error_details: Optional[str] = None):
        super().__init__(message=message, status_code=401, error_details=error_details)

class ForbiddenError(BaseAppException):
    """Exception raised for authorization errors (no permission)"""
    def __init__(self, message: str = "Permission denied", error_details: Optional[str] = None):
        super().__init__(message=message, status_code=403, error_details=error_details)

class BusinessRuleError(BaseAppException):
    """Exception raised when a business rule is violated"""
    def __init__(self, message: str = "Business rule violation", error_details: Optional[str] = None):
        super().__init__(message=message, status_code=400, error_details=error_details)
