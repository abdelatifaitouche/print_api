from app.schemas.user_schema import UserCreate , User , UserLogin , UserAdminUpdate
from app.repositories.auth_repo import AuthRepository
from sqlalchemy.orm import Session
from app.models.user import User as UserDB
from app.utils.password_utils import encrypt_password , check_password
from app.utils.jwt_utils import JwtManager
from app.services.base_service import BaseService
from typing import List



class AuthService(BaseService[UserDB , UserCreate , User , UserAdminUpdate]) :

    READ_SCHEMA = User
    CREATE_SCHEMA = UserCreate
    UPDATE_SCHEMA = UserAdminUpdate
    DB_MODEL = UserDB
    
    def __init__(self):
        self.repo = AuthRepository()
        self.__jwt_manager = JwtManager()

    def create(self , user_data : UserCreate , db : Session) -> User:
        
        if not user_data.email or not user_data.password : 
            raise Exception("please provide a valid email or password")

        if self.repo.get_user_by_email(user_data.email , db) is not None : 
            raise Exception("Email already exists")
        
        
        hashed_password = encrypt_password(user_data.password)

        user_model = UserDB(username = user_data.username , 
                            email = user_data.email ,
                            password = hashed_password ,
                            role = user_data.role , 
                            company_id=user_data.company_id)

        user = self.repo.create(user_model , db)
        

        return User.from_orm(user)



    def login_user(self ,login_data : UserLogin , db : Session):
        """
            Takes the login data : email and password 
            checks if a user with the provided email exists 
                checks if the password matches(dont forget to hash it or use the utils validation)
                returns jwt auth tokens

        """
        
        user : UserDB = self.repo.get_user_by_email(login_data.email , db)

        if not user  : 
            raise Exception("email dosnt exists")

        if not check_password(login_data.password , user.password) :
            raise Exception("wrong password")

        """
            now , based on the right data encode it and return its jwt 
        """
        


        access_token : str = self.__jwt_manager.generate_token(user_data = {"id" : user.id ,
                                                                            "username":user.username , 
                                                                            "email" : user.email ,
                                                                            "role":user.role,
                                                                            "company_id" : user.company_id})
        
        return access_token
    
    """
    def get_all_users(self , db : Session) -> List[User]:
        
        users : List[User] = self.__auth_repo.list(db)
        
        return users 

    """
    def get_user_by_email(self):
        return

    

    def get_user_by_id(self , user_id :str , db:Session)-> User:
        
        user : User = self.repo.get_by_id(user_id , db) 

        if not user : 
            raise Exception("no user found")
        
        return User.from_orm(user)

