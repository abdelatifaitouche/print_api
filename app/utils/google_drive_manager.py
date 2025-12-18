
from google.oauth2 import service_account
from googleapiclient.discovery import build
from pathlib import Path
import uuid
from googleapiclient.http import MediaIoBaseUpload
from googleapiclient.errors import HttpError
class GoogleDriveManager : 
    def __init__(self):
        BASE_DIR = Path(__file__).resolve().parent.parent.parent
        self.__service_file = BASE_DIR /  "drive_api.json"
        self.SCOPES = ["https://www.googleapis.com/auth/drive"]
        self.__creds = self.__authenticate()
        self.__client =  self.__get_client()


    def __authenticate(self):
        return service_account.Credentials.from_service_account_file(self.__service_file , scopes=self.SCOPES,)
    
    def __get_client(self):
        return build("drive" , "v3" , credentials=self.__creds) 

    def upload_file(self, file_upload):
        try:
            # Metadata for Google Drive
            file_metadata = {"name": file_upload.filename}  # use actual filename

            # Ensure file pointer is at start
            file_upload.file.seek(0)

            # Stream file directly (no full RAM read)
            media = MediaIoBaseUpload(file_upload.file, mimetype=file_upload.content_type, resumable=True)

            # Upload to Google Drive
            file = self.__client.files().create(
                body=file_metadata,
                media_body=media,
                fields="id"
            ).execute()

            file_id = file.get("id")
            print(f'FILE ID: {file_id}')
            return file_id

        except HttpError as err:
            print(f"An error has occurred: {err}")
            return None

    def download_file(self):
        pass
    
    def create_folder(self, folder_name : str , parent_id : str | None = None)->str :
        metadata = {
            "name" :folder_name,
            "mimeType":"application/vnd.google-apps.folder"
        }

        if parent_id : 
            metadata["parents"]= parent_id

        folder = (self.__client.files().create(body=metadata , fields="id, name").execute())

        return folder['id']

    def list_files(self):
        folder_name = "DriveApiTest"

        response = (self.__client.files().list(
            pageSize=10, fields="nextPageToken, files(id, name)"
        ).execute())
        
        folders = response.get("files" , [])

        print(folders)


    def list_folders(self):
        """
        Lists all folders in the root directory of the service account's Drive.
        """
        query = "mimeType='application/vnd.google-apps.folder' and 'root' in parents"
        response = self.__client.files().list(
                q=query,
                pageSize=100,
                fields="nextPageToken, files(id, name)"
            ).execute()

        folders = response.get("files", [])
        for folder in folders:
            print(f"Folder Name: {folder['name']}, ID: {folder['id']}")
