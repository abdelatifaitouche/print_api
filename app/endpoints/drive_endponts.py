from fastapi import APIRouter , UploadFile , File
from app.utils.google_drive_manager import GoogleDriveManager



drive_endpoints = APIRouter()
gdm = GoogleDriveManager()

@drive_endpoints.get("/")
def list_all_folders():
    gdm.list_folders()
    return "testing the listing"




@drive_endpoints.post('/upload')
def upload_file(file : UploadFile = File(...)):
    id = gdm.upload_file(file)
    return f"file id is : {id}"
