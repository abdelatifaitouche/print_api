from app.schemas.user_schema import UserCreate, User, UserLogin, UserAdminUpdate
from app.repositories.auth_repo import AuthRepository
from sqlalchemy.orm import Session
from app.models.user import User as UserDB
from app.utils.password_utils import encrypt_password, check_password
from app.utils.jwt_utils import JwtManager
from app.services.base_service import BaseService
from app.auth.jwt.jwt_service import JwtService
from app.schemas.jwt_payload import JwtPayload
from app.execeptions.base import (
    InvalidCredentialsError,
    WeakPasswordError,
    UserAlreadyExistsError,
    NotFoundError,
)


class AuthService(BaseService[UserDB, UserCreate, User, UserAdminUpdate]):
    READ_SCHEMA = User
    CREATE_SCHEMA = UserCreate
    UPDATE_SCHEMA = UserAdminUpdate
    DB_MODEL = UserDB
    REPO_CLASS = AuthRepository

    def __init__(self, db: Session):
        super().__init__(db=db)
        self.__jwt_manager = JwtManager()

    def create(self, user_data: UserCreate) -> User:
        if self.repo.get_user_by_email(user_data.email) is not None:
            raise UserAlreadyExistsError(
                message="An account with this email Already exists",
                details={"email": user_data.email},
            )

        if len(user_data.password) < 6:
            raise WeakPasswordError(
                message="Password length must be at least 6 characters",
                details={"min_length": 6},
            )

        hashed_password = encrypt_password(user_data.password)

        user_model = UserDB(
            username=user_data.username,
            email=user_data.email,
            password=hashed_password,
            role=user_data.role,
            company_id=user_data.company_id,
        )

        user = self.repo.create(user_model)

        return User.from_orm(user)

    def login_user(self, login_data: UserLogin):
        user: UserDB = self.repo.get_user_by_email(login_data.email)

        if not user:
            raise InvalidCredentialsError(message="Invalid Credentials")
        if not check_password(login_data.password, user.password):
            raise InvalidCredentialsError(message="Invalid Credentials")

        payload: JwtPayload = JwtPayload(
            user_id=user.id,
            email=user.email,
            company_id=user.company_id,
            role=user.role,
            username=user.username,
        )

        access_token: str = JwtService.generate_access_token(payload)

        return access_token

    def get_user_by_email(self):
        return

    def get_user_by_id(self, user_id: str) -> User:
        user: User = self.repo.get_by_id(user_id)

        if not user:
            raise NotFoundError(
                message=f"{self.repo.MODEL.__name__} not found",
                details={"user_id": user_id},
            )

        return User.from_orm(user)
