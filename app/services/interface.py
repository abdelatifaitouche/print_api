from abc import ABC , abstractmethod




class ServiceInterface(ABC):


    @abstractmethod
    def list(self , *args , **kwargs):
        raise NotImplementedError("List method should be implemented")



    @abstractmethod
    def create(self, *args , **kwargs):
        raise NotImplementedError("Create method not implemented")


    @abstractmethod
    def get_by_id(self , *args , **kwargs):
        raise NotImplementedError("Get by id should be implemented")


    @abstractmethod
    def delete(self , *args , **kwargs):
        raise NotImplementedError("Delete method should be implemented")

    
    @abstractmethod
    def update(self , *args , **kwargs):
        raise NotImplementedError("Update method should be implemented")
