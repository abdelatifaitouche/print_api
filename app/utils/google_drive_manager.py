import os
import pickle
from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload
import mimetypes

class GoogleDriveManager:
    SCOPES = ['https://www.googleapis.com/auth/drive']  # Full access - tu peux restreindre plus tard

    def __init__(
        self,
        token_path: str = "printshop_token.pickle",
        credentials_path: str = "printflow_dev.json",  # client secrets JSON (OAuth)
        parent_folder_id: str = "1Y0_n_Pqd1rj5cCJscsqzEwr_f3fZcg72"  # dossier racine du print shop
    ):
        BASE_DIR = Path(__file__).resolve().parent.parent.parent
        self.token_path = BASE_DIR / token_path
        self.credentials_path = BASE_DIR / credentials_path
        self.parent_folder_id = parent_folder_id

        self.creds = self._load_credentials()
        self.service = build("drive", "v3", credentials=self.creds)

    def _load_credentials(self):
        """Charge et rafraîchit les credentials OAuth2 depuis le pickle."""
        creds = None

        if os.path.exists(self.token_path):
            with open(self.token_path, 'rb') as token:
                creds = pickle.load(token)

        # Si pas de creds valides → refresh ou nouvelle auth
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                raise FileNotFoundError(
                    f"Token invalide et pas de refresh token. "
                    f"Supprime {self.token_path} et relance l'authentification manuelle."
                )

            # Sauvegarde le token rafraîchi
            with open(self.token_path, 'wb') as token:
                pickle.dump(creds, token)

        return creds

    def upload_file(self,file_name : str ,  file_path : str , folder_id: str):
        
        try:
            target_folder = folder_id

            file_metadata = {
                "name": file_name,
                "parents": [target_folder]
            }

            mime_type,_ = mimetypes.guess_type(file_path)

            media = MediaFileUpload(
                file_path,
                mimetype=mime_type or 'application/octet-stream',
                resumable=True
            )

            file = self.service.files().create(
                body=file_metadata,
                media_body=media,
                fields="id, webViewLink",
                supportsAllDrives=True
            ).execute()

            file_id = file.get('id')
            print(f"✅ Upload réussi → File ID: {file_id}")
            return file_id

        except HttpError as err:
            print(f"❌ Erreur upload Google Drive: {err}")
            return None

    def create_folder(self, folder_name: str, parent_id: str | None = None) -> str:
        
        metadata = {
            "name": folder_name,
            "mimeType": "application/vnd.google-apps.folder",
            "parents": [parent_id or self.parent_folder_id]
        }

        folder = self.service.files().create(
            body=metadata,
            fields="id",
            supportsAllDrives=True
        ).execute()

        print(f"folder created : {folder_name} (ID: {folder.get('id')})")
        return folder.get('id')

    def list_files(self, folder_id: str | None = None, include_folders: bool = False):
        
        target_folder = folder_id or self.parent_folder_id

        query_parts = [
            f"'{target_folder}' in parents",
            "trashed=false"
        ]

        if not include_folders:
            query_parts.append("mimeType != 'application/vnd.google-apps.folder'")

        query = " and ".join(query_parts)

        try:
            response = self.service.files().list(
                q=query,
                pageSize=100,
                fields="nextPageToken, files(id, name, mimeType, size, webViewLink, createdTime)",
                supportsAllDrives=True,
                includeItemsFromAllDrives=True
            ).execute()

            items = response.get('files', [])
            return items
        except Exception as e:
            print(f"Erreur list_files: {e}")
            return []

    def list_folders(self, parent_id: str | None = None):
        target_folder = parent_id or self.parent_folder_id
        query = (
            f"'{target_folder}' in parents "
            "and mimeType='application/vnd.google-apps.folder' "
            "and trashed=false"
        )

        response = self.service.files().list(
            q=query,
            pageSize=100,
            fields="nextPageToken, files(id, name, webViewLink, createdTime)",
            supportsAllDrives=True,
            includeItemsFromAllDrives=True
        ).execute()

        return response.get('files', [])

    def get_storage_data(self):
        
        try:
            about = self.service.about().get(fields="storageQuota").execute()
            return about.get('storageQuota', {})
        except Exception as e:
            print(f"Erreur quota: {e}")
            return {}
