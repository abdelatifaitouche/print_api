from pydantic import BaseModel , Field
from app.enums.file_enums import FileStatus
class UploadedFileBase(BaseModel):
    file_name : str = Field(... , min_length=1) 
    status : str = Field(default=FileStatus.PENDING.value) 


class UploadedFileRead(BaseModel):
    file_name : str
    google_file_id : str | None =None
    status : str

    model_config = {"from_attributes" : True}



