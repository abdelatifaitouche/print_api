import bcrypt


def encrypt_password(password : str) -> str:
    """
        encrypt the password using the bcrypt hashing function , 

        it takes the password string , convert it to bytes format

        returns the hashing in bytes
    """

    hashed_password = bcrypt.hashpw(password.encode("utf-8") , bcrypt.gensalt())


    return hashed_password.decode("utf-8")




def check_password(password : str , hashed_password : str) -> bool : 
    return bcrypt.checkpw(password.encode("utf-8") , hashed_password.encode("utf-8"))

