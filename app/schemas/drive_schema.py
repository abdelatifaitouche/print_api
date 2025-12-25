from pydantic import BaseModel




class DriveFolderRead(BaseModel):
    id : str
    name : str
    webViewLink : datetime
    createdTime : datetime



