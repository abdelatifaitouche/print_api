from datetime import datetime, timedelta

"""
THIS IS A BULLSHIT CODE 
DONE FOR NO PURPOSE AT ALL
DA FUCK AM DOING
"""    

class JwtPayloadFactory : 
    
    __access_exp = 36000  #should be loaded from the .env
    __refresh_exp = 5000000

    @staticmethod
    def access_token_payload(id :str , name : str ,email : str ,  role : str , company_id : str)->dict:
        return {
            "id" :  id , 
            "name" : name , 
            "email" : email,
            "role" : role ,
            "company_id" : company_id , 
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


