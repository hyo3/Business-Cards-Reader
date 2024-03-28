import os.path
import io
from googleapiclient.http import MediaIoBaseDownload

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2 import service_account

from modules.decode_json import decode_json


def get_drive(sheet_id: str):
    """Shows basic usage of the Drive v3 API.
    Prints the names and ids of the first 10 files the user has access to.
    """

    SCOPES = ["https://www.googleapis.com/auth/drive.metadata.readonly"]
    encoded_str = os.getenv('GCP_JSON_STR')
    dict_data = decode_json(encoded_str=encoded_str)
    dict_data["scopes"] = SCOPES

    creds = None
    creds = service_account.Credentials.from_service_account_info(dict_data)

    try:
        service = build("drive", "v3", credentials=creds)

        request = service.files().get_media(fileId=sheet_id)
        fh = io.BytesIO()
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()
            print("Download %d%%." % int(status.progress() * 100))

        fh.seek(0)
        bibary_data = fh.getvalue()
        return bibary_data

    except HttpError as error:
        print(f"An error occurred: {error}")

if __name__ == "__main__":
    my_dict = get_drive("1cz0k0UDM6qZj9DkhAchWaJrl5AFoO0oA")
    print(my_dict)