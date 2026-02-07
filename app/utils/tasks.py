from celery import Celery
from app.utils.google_drive_manager import GoogleDriveManager
from app.repositories.company_repo import CompanyRepository
from app.config.database import SessionLocal
from sqlalchemy.orm import Session
import os
from app.models import UploadedFile as UploadedFileDb

celery_app = Celery(main="drive", broker=os.getenv("CELERY_BROKER_URL"))

celery_app.conf.update(
    task_track_started=True,
    task_acks_late=True,
    worker_prefetch_multiplier=1,
    worker_max_tasks_per_child=10,
)


@celery_app.task(bind=True, max_retires=3)
def process_folder_creation(self, company_id: str, folder_name: str):
    """
    Process the drive folder creation
    """
    gdm = GoogleDriveManager()
    folder_id = gdm.create_folder(folder_name=folder_name)

    db: Session = SessionLocal()

    cp = CompanyRepository(db)
    company_model = cp.get_by_id(company_id)

    if not folder_id:
        data = {"folder_status": "FAILED"}
        cp.update(company_model, data)
        return

    data = {"drive_folder_id": folder_id, "folder_status": "CREATED"}

    cp.update(company_model, data)

    return "Message Processed"


import logging

logger = logging.getLogger(__name__)


@celery_app.task(bind=True, max_retries=3)
def process_file_upload(self, uploaded_file_id: str, file_name: str, file_path: str):
    logger.info(f"Task STARTED - ID: {self.request.id}")
    logger.info(
        f"Params: uploaded_file_id={uploaded_file_id}, file_name={file_name}, file_path={file_path}"
    )

    db = None
    try:
        # Ensure uploaded_file_id is a string
        uploaded_file_id = str(uploaded_file_id)

        logger.info("Opening DB session")
        db = SessionLocal()

        logger.info(f"Querying UploadedFile with id: {uploaded_file_id}")
        uploaded_file = (
            db.query(UploadedFileDb)
            .filter(UploadedFileDb.id == uploaded_file_id)
            .first()
        )

        if not uploaded_file:
            logger.error(f"UploadedFile NOT FOUND for id: {uploaded_file_id}")
            return {"error": f"UploadedFile {uploaded_file_id} not found"}

        logger.info(
            f"Found UploadedFile: id={uploaded_file.id}, name={uploaded_file.file_name}, status={uploaded_file.status}"
        )

        # Check if already uploaded to prevent duplicate uploads
        if uploaded_file.status == "uploaded":
            logger.warning(f"File {uploaded_file_id} already uploaded, skipping")
            return {
                "status": "already_uploaded",
                "google_file_id": uploaded_file.google_file_id,
                "uploaded_file_id": uploaded_file_id,
            }

        logger.info("Updating status to 'uploading'")
        uploaded_file.status = "uploading"
        db.commit()
        db.refresh(uploaded_file)
        logger.info("Status 'uploading' committed")

        # Verify file exists before upload
        if not os.path.exists(file_path):
            logger.error(f"File not found at path: {file_path}")
            raise FileNotFoundError(f"File not found: {file_path}")

        logger.info("Initializing GoogleDriveManager")
        gdm = GoogleDriveManager()

        logger.info(f"Calling upload_file for: {file_name}")
        google_drive_file_id = gdm.upload_file(
            file_name, file_path, folder_id=uploaded_file.parent_drive_folder
        )
        logger.info(f"Upload returned: {google_drive_file_id}")

        if not google_drive_file_id:
            logger.error("upload_file returned None/empty ID")
            raise RuntimeError("File upload failed - no Google file ID")

        logger.info("Updating DB with Google file ID and status 'uploaded'")
        uploaded_file.google_file_id = google_drive_file_id
        uploaded_file.status = "uploaded"
        db.commit()
        db.refresh(uploaded_file)
        logger.info("File successfully uploaded!")

        # Clean up temporary file
        if os.path.exists(file_path):
            os.remove(file_path)
            logger.info(f"Temporary file removed: {file_path}")

        return {
            "status": "success",
            "google_file_id": google_drive_file_id,
            "uploaded_file_id": uploaded_file_id,
        }

    except Exception as e:
        logger.exception(f"Task FAILED with error: {str(e)}")

        if db:
            try:
                # Re-query to avoid stale object
                uploaded_file = (
                    db.query(UploadedFileDb)
                    .filter(UploadedFileDb.id == uploaded_file_id)
                    .first()
                )

                if uploaded_file:
                    uploaded_file.status = "failed"
                    db.commit()
                    logger.info("Status set to 'failed'")
            except Exception as commit_error:
                logger.error(f"Failed to update error status: {commit_error}")
                db.rollback()

        # Retry with exponential backoff
        raise self.retry(exc=e, countdown=60 * (2**self.request.retries), max_retries=3)

    finally:
        if db:
            logger.info("Closing DB session")
            db.close()
