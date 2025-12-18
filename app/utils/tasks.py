from celery import Celery
from app.utils.google_drive_manager import GoogleDriveManager
from app.repositories.company_repo import CompanyRepository
from app.config.database import SessionLocal
from sqlalchemy.orm import Session


celery_app = Celery(main="drive" , broker="pyamqp://guest:guest@localhost:5672//")


@celery_app.task
def process_folder_creation(company_id : str , folder_name : str):
    """
        Process the drive folder creation
    """
    gdm = GoogleDriveManager()
    folder_id = gdm.create_folder(folder_name=folder_name)
    
    db : Session = SessionLocal()

    cp = CompanyRepository()
    company_model = cp.get_by_id(company_id , db)

    if not folder_id : 
        data = {"folder_status":"FAILED"}
        cp.update(company_model , data , db)
        return
    
    data = {"drive_folder_id": folder_id , "folder_status":"CREATED"}

    cp.update(company_model , data , db)

    return "Message Processed"


