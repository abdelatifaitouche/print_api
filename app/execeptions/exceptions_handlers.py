from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import SQLAlchemyError
import logging

from app.execeptions.base import (
    AppExceptions,
    NotFoundError,
    ValidationError,
    InvalidCredentialsError,
    UserAlreadyExistsError,
    WeakPasswordError,
    AlreadyExistsError,
    DatabaseError,
    ExternalServiceError,
)

logger = logging.getLogger(__name__)


def register_exception_handlers(app: FastAPI):
    @app.exception_handler(NotFoundError)
    async def not_found_handler(request: Request, exc: NotFoundError):
        """Handle resource not found errors - 404"""
        logger.warning(
            f"NotFoundError: {exc.message}",
            extra={
                "path": request.url.path,
                "method": request.method,
                "details": exc.details,
            },
        )
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={
                "error": "not_found",
                "message": exc.message,
                "details": exc.details,
            },
        )

    @app.exception_handler(ValidationError)
    async def validation_error_handler(request: Request, exc: ValidationError):
        """Handle business validation errors - 422"""
        logger.warning(
            f"ValidationError: {exc.message}",
            extra={
                "path": request.url.path,
                "method": request.method,
                "details": exc.details,
            },
        )
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "error": "validation_error",
                "message": exc.message,
                "details": exc.details,
            },
        )

    @app.exception_handler(InvalidCredentialsError)
    async def invalid_credentials_handler(
        request: Request, exc: InvalidCredentialsError
    ):
        logger.warning(
            f"InvalidCredentialsError: {exc.message}",
            extra={
                "path": request.url.path,
                "method": request.method,
            },
        )
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={
                "error": "invalid_credentials",
                "message": exc.message or "Invalid email or password",
            },
        )

    @app.exception_handler(UserAlreadyExistsError)
    async def user_already_exists_handler(
        request: Request, exc: UserAlreadyExistsError
    ):
        """Handle duplicate user registration - 409"""
        logger.warning(
            f"UserAlreadyExistsError: {exc.message}",
            extra={
                "path": request.url.path,
                "method": request.method,
                "details": exc.details,
            },
        )
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={
                "error": "user_already_exists",
                "message": exc.message or "An account with this email already exists",
                "details": exc.details,
            },
        )

    @app.exception_handler(WeakPasswordError)
    async def weak_password_handler(request: Request, exc: WeakPasswordError):
        logger.warning(
            f"WeakPasswordError: {exc.message}",
            extra={
                "path": request.url.path,
                "method": request.method,
                "details": exc.details,
            },
        )
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "error": "weak_password",
                "message": exc.message
                or "Password does not meet security requirements",
                "details": exc.details,
            },
        )

    @app.exception_handler(AlreadyExistsError)
    async def already_exists_handler(request: Request, exc: AlreadyExistsError):
        logger.warning(
            f"AlreadyExistsError: {exc.message}",
            extra={
                "path": request.url.path,
                "method": request.method,
                "details": exc.details,
            },
        )
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={
                "error": "already_exists",
                "message": exc.message,
                "details": exc.details,
            },
        )

    @app.exception_handler(DatabaseError)
    async def database_error_handler(request: Request, exc: DatabaseError):
        logger.error(
            f"DatabaseError: {exc.message}",
            extra={
                "path": request.url.path,
                "method": request.method,
                "details": exc.details,
            },
            exc_info=True,
        )

        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "error": "database_error",
                "message": "A database error occurred. Please try again later.",
                "details": exc.details,
            },
        )

    @app.exception_handler(ExternalServiceError)
    async def external_service_error_handler(
        request: Request, exc: ExternalServiceError
    ):
        """Handle external service failures - 503"""
        logger.error(
            f"ExternalServiceError: {exc.message}",
            extra={
                "path": request.url.path,
                "method": request.method,
                "details": exc.details,
            },
            exc_info=True,
        )
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={
                "error": "external_service_error",
                "message": exc.message or "External service temporarily unavailable",
                "details": exc.details,
            },
        )

    @app.exception_handler(RequestValidationError)
    async def request_validation_handler(request: Request, exc: RequestValidationError):
        logger.warning(
            f"Request validation failed: {exc.errors()}",
            extra={
                "path": request.url.path,
                "method": request.method,
                "errors": exc.errors(),
            },
        )
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "error": "request_validation_error",
                "message": "Request validation failed",
                "details": exc.errors(),
            },
        )

    @app.exception_handler(SQLAlchemyError)
    async def sqlalchemy_error_handler(request: Request, exc: SQLAlchemyError):
        logger.error(
            f"Unhandled SQLAlchemy error: {str(exc)}",
            extra={
                "path": request.url.path,
                "method": request.method,
            },
            exc_info=True,
        )
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "error": "database_error",
                "message": "An unexpected database error occurred",
                "details": {},
            },
        )

    @app.exception_handler(Exception)
    async def generic_exception_handler(request: Request, exc: Exception):
        """Catch all unhandled exceptions - 500"""
        logger.critical(
            f"Unhandled exception: {str(exc)}",
            extra={
                "path": request.url.path,
                "method": request.method,
                "exception_type": type(exc).__name__,
            },
            exc_info=True,
        )

        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "error": "internal_server_error",
                "message": "An unexpected error occurred. Please try again later.",
                "details": {
                    "error_type": type(exc).__name__,
                    "error": str(exc),
                },
            },
        )

    @app.exception_handler(AppExceptions)
    async def app_exception_handler(request: Request, exc: AppExceptions):
        """Handle any AppException subclass not caught by specific handlers - 500"""
        logger.error(
            f"Unhandled AppException: {exc.message}",
            extra={
                "path": request.url.path,
                "method": request.method,
                "details": exc.details,
                "exception_type": type(exc).__name__,
            },
            exc_info=True,
        )
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "error": "application_error",
                "message": exc.message,
                "details": exc.details,
            },
        )
