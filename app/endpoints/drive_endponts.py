from fastapi import APIRouter , UploadFile , File
from app.utils.google_drive_manager import GoogleDriveManager
from typing import List
from pydantic import BaseModel

drive_endpoints = APIRouter()
gdm = GoogleDriveManager()


"""
CREATE FOLDERS 
DELETE FOLDERS
UPDATE A FOLDER
LIST FOLDERS
"""    

@drive_endpoints.post("/")
def create_folder():
    return




@drive_endpoints.get("/")
def list_all_folders():
    folders =  gdm.list_folders()
    return folders


@drive_endpoints.get("/{folder_id}")
def list_files_per_folder(folder_id : str):
    files = gdm.list_files(folder_id)
    return files


@drive_endpoints.get("/storage")
def get_storage():
    storage = gdm.get_storage_data()
    return storage



@drive_endpoints.post('/upload')
def upload_file():
    #id = gdm.upload_file(file , "1iqsvTbXlhytlxpPRyyPlqTCUemcW4njC")
    return f"uploaded check logs"
