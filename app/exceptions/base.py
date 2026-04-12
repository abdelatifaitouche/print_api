"""
Exceptions for the overrall app
separated with :
    - business layer exceptions
    - Infrastructure layer
"""


class AppExceptions(Exception):
    def __init__(self, message: str, details: dict = None):
        self.message: str = message
        self.details: dict = details or {}
        super().__init__(self, message)


# Business Logic Exceptions


class NotFoundError(AppExceptions):
    """Resource not Found"""

    pass


class ValidationError(AppExceptions):
    """Business Validation Failed"""

    pass


# Authentication Exceptions


class InvalidCredentialsError(AppExceptions):
    pass


class UserAlreadyExistsError(AppExceptions):
    pass


class WeakPasswordError(AppExceptions):
    pass


# Infrastructure Error :


class AlreadyExistsError(AppExceptions):
    pass


class DatabaseError(AppExceptions):
    pass


class ExternalServiceError(AppExceptions):
    pass
