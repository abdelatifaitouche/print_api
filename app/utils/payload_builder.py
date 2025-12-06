from datetime import datetime, timedelta



class JwtPayloadFactory : 
    
    __access_exp = 36000  #should be loaded from the .env
    __refresh_exp = 5000000

    @staticmethod
    def access_token_payload(name : str ,email : str ,  role : str)->dict:
        return {
            "name" : name , 
            "email" : email,
            "role" : role , 
            "exp" :int((datetime.utcnow() + timedelta(seconds=JwtPayloadFactory.__access_exp)).timestamp())
        }

    @staticmethod
    def refresh_token_payload():    
        return {
            "name" : name , 
            "email" : email,
            "role" : role , 
            "exp" :int((datetime.utcnow() + timedelta(seconds=JwtPayloadFactory.__access_exp)).timestamp())
        }


