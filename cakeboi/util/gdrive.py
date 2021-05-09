import datetime
import re

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

from cakeboi.util import local
from cakeboi.util.gsheets import today_string
from cakeboi.util.guser import GoogleUser

DEFAULT_GET_FIELDS = "nextPageToken, files(id, name, mimeType, parents, createdTime)"


def create_token():
    """
    Logs the user in and returns a service resource object
    """
    client_secret = local.get_token('oauth')  # dict/json format

    flow = InstalledAppFlow.from_client_config(
        client_secret, ["https://www.googleapis.com/auth/drive"])
    creds = flow.run_local_server(port=0)

    print(creds.to_json())
    with open('new_drive_token.json', 'w') as token:
        token.write(creds.to_json())

    service = build('drive', 'v3', credentials=creds)


def login(token=None, client_secret=None):
    """
    Logs the user in and returns a service resource object
    """
    token = local.get_token("drive_token")  # dict/json format
    client_secret = local.get_token('oauth')  # dict/json format
    creds = None

    _SCOPES = ["https://www.googleapis.com/auth/drive"]
    if token:
        creds = Credentials.from_authorized_user_info(token, _SCOPES)

    # If there are no (valid) credentials available, let the user log in.
    # Click http link
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            # cred_json = ""
            flow = InstalledAppFlow.from_client_config(
                client_secret, _SCOPES)
            creds = flow.run_local_server(port=0)
            print(creds.to_json())

    service = build('drive', 'v3', credentials=creds)
    return service


class DriveUser(GoogleUser):
    def __init__(self, name=None, channel_id=None, drive_id=None):
        GoogleUser.__init__(self, name=name, channel_id=channel_id, drive_id=drive_id)
        self.service = login()

    def upload(self, path_list=None, parent_id=None):
        """
        Uploads last X images from discord to Drive

        Returns list of references of uploaded files.
        IDs are necessary for GoogleSheets =IMAGE()
        """
        if path_list is None:
            print("[Debug]", "Empty list was passed to drive.helper.update()")
            return

        # Collects references to return later
        items = []
        # If no specific folder given, upload to 'today folder' (creates it if it doesnt exist)
        if parent_id is None:
            today_folder = self.create_folder()
            parent_id = today_folder['id']

        # Uploads each file from that list to the drive folder
        for path in path_list:
            filename = re.split(r'[ \\/]', path)[-1]
            new_file = self.create_file(file_name=filename, path=path, parent_id=parent_id)
            items.append(new_file)

        return items

    def create_file(self, path, file_name=None, parent_id=None):
        """
        Creates a drive file.
        Uploads the content of a local file given by path
        """
        # Some typecasting measures
        if type(parent_id) is dict:
            parent_id = parent_id['id']

        if type(parent_id) != list:
            parent_id = [parent_id]

        if file_name is None:
            file_name = re.split(r'[\\/]', path)[-1]

        # Metadata for the file
        metadata = {
            'name': file_name,  # file name
            'parents': parent_id,  # parent folder
        }

        # Uploads local file into program/drive space
        media_body = MediaFileUpload(path, mimetype='image/jpeg')

        # Officially create the file (makes it accessible/visible/etc)
        file = self.service.files().create(body=metadata, media_body=media_body, fields='*').execute()
        return file

    def create_folder(self, folder_name=None, parents=None):
        """
        Creates a sub folder for the day in the correct folder (per channel)
        Returns the folder reference
        """
        # If no folder name passed, make it current day
        if folder_name is None:
            folder_name = today_string()

        # Defaults to a drive folder specific to the channel/user
        if parents is None:
            parents = [self.drive_id]

        # fix data type
        if type(parents) != list:
            parents = [parents]

        # Check if folder already exists with that name.
        # Use that one instead then
        for sibling in self.get_children(parent_id=parents[0]):
            if sibling['name'] == folder_name:
                print("Folder already exists")
                return sibling

        # Prepare folder meta data
        file_metadata = {
            'name': folder_name,
            'mimeType': 'application/vnd.google-apps.folder',
            'parents': parents
        }

        # Creates it
        file = self.service.files().create(body=file_metadata, fields='*').execute()
        return file

    def get_all(self, q='', spaces='drive', fields=DEFAULT_GET_FIELDS):
        """
        Lists all Google Drive files and folders that are accessible to the bot (= were created by the bot)
        Returns list of file references (drive file objects)
        """
        page_token = None
        items = []
        while True:
            request = self.service.files().list(q=q + " and trashed = false",
                                                spaces=spaces,
                                                fields=fields,
                                                pageToken=page_token)
            response = request.execute()
            for item in response.get('files', []):
                items.append(item)
            page_token = response.get('nextPageToken', None)
            if page_token is None:
                break
        return items

    def get_folders(self, q=f"mimeType = 'application/vnd.google-apps.folder'", fields=DEFAULT_GET_FIELDS):
        """
        Get all Google Drive files that are accessible to the bot (= were created by the bot)
        Returns list of file references (drive file objects)
        """
        return self.get_all(q=q, fields=fields)

    def get_children(self, parent_id=None):
        """
        Find the children files/folders of a folder
        Returns list of file references (drive file objects)
        """
        if parent_id is None:
            parent_id = self.drive_id
        return self.get_all(q=f"'{parent_id}' in parents")

    def tree(self, folder_id=None, indent=0):
        """
        Find the children files/folders of a folder
        Recursive call and formats as a tree

        Returns nothing
        """
        # BASE CASE
        if folder_id is None:
            folder_id = self.drive_id
        children = self.get_children(folder_id)
        if indent == 0:
            print(f"ROOT [{len(children)}]")
        if len(children) == 0:
            return

        # RECURSION
        for c in children:
            c_children = self.get_children(c['id'])
            print((indent + 4) * ' ', f"{c['name']} [{len(c_children)}]")
            self.tree(c['id'], indent + 4)

    def remove(self, file):
        """
        Alias for delete()
        """
        self.delete(file)

    def delete(self, drive_file):
        """
        Deletes a google drive file
        """
        try:
            if type(drive_file) is dict:
                file_id = drive_file['id']
            elif type(drive_file) is str:
                file_id = drive_file
            else:
                raise ValueError
            self.service.files().delete(fileId=file_id).execute()
        except ValueError as err:
            print(err, "Received invalid parameter")

    def clear_folder(self, folder_id):
        """
        Clears a google drive folder of its content.
        Wont work for files that weren't created by bot.
        """
        content = self.get_children(parent_id=folder_id)
        trashed = []
        for f in content:
            trashed.append(f)
            self.delete(f)
        return trashed
