from fastapi import APIRouter, UploadFile, File, Depends
from app.utils.google_drive_manager import GoogleDriveManager
from typing import List
from pydantic import BaseModel

drive_endpoints = APIRouter()


class DriveFolderCreate(BaseModel):
    folder_name: str
    parent_id: str | None = None


def get_drive_service():
    return GoogleDriveManager()


@drive_endpoints.post("/")
def create_folder(
    folder_data: DriveFolderCreate,
    gdm: GoogleDriveManager = Depends(get_drive_service),
):
    folder = gdm.create_folder()
    return


@drive_endpoints.get("/")
def list_all_folders(gdm: GoogleDriveManager = Depends(get_drive_service)):
    folders = gdm.list_folders()
    return folders


@drive_endpoints.get("/{folder_id}")
def list_files_per_folder(
    folder_id: str, gdm: GoogleDriveManager = Depends(get_drive_service)
):
    files = gdm.list_files(folder_id)
    return files


@drive_endpoints.get("/storage")
def get_storage(gdm: GoogleDriveManager = Depends(get_drive_service)):
    storage = gdm.get_storage_data()
    return storage
