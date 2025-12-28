



class BaseException(Exception): 
    def __init__(self , message : str , service : str | None = None ) : 
        self.message = message
        self.service = service or self.__class__.__name__
        super().__init__(self.message)


    def __str__(self):
        return f"<{self.service}> {self.message}"



class NoDataError(BaseException):
    pass
