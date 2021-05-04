import datetime
import os.path
import re

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

from cakeboi.util.common.user import GoogleUser

# If modifying these scopes, delete the file token.json.

DEFAULT_GET_FIELDS = "nextPageToken, files(id, name, mimeType, parents, createdTime)"


def login(cred_json=r"util/drive/client_secrets.json", token='util/drive/token.json',
          save_token='util/drive/token.json'):
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    _SCOPES = ["https://www.googleapis.com/auth/drive.file"]
    cred = None

    if os.path.exists(token):
        cred = Credentials.from_authorized_user_file(token, _SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not cred or not cred.valid:
        if cred and cred.expired and cred.refresh_token:
            cred.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                cred_json, _SCOPES)
            cred = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(save_token, 'w') as token:
            token.write(cred.to_json())

    service = build('drive', 'v3', credentials=cred)
    return service


class DriveUser:
    def __init__(self, name=None, channel_id=None, drive_id=None):
        GoogleUser.__init__(self, name=name, channel_id=channel_id, drive_id=drive_id)
        self.service = login()

    def upload(self, path_list=[], parent_id=None):
        """
        Uploads last X images from discord to Drive

        Returns list of dict of uploaded files.
        IDs are necessary for GoogleSheets =IMAGE()
        """
        items = []
        if parent_id is None:
            today_folder = self.create_folder()
            parent_id = today_folder['id']
        for path in path_list:
            filename = re.split(r'[ \\/]', path)[-1]
            new_file = self.create_file(file_name=filename, path=path, parent_id=parent_id)
            items.append(new_file)
        return items

    def create_file(self, path, file_name=None, parent_id=None):
        if type(parent_id) is dict:
            parent_id = parent_id['id']

        if type(parent_id) != list:
            parent_id = [parent_id]

        if file_name is None:
            file_name = re.split('[\\/]', path)[-1]

        metadata = {
            'name': file_name,
            'parents': parent_id,
        }

        media_body = MediaFileUpload(path, mimetype='image/jpeg')
        file = self.service.files().create(body=metadata, media_body=media_body, fields='*').execute()
        return file

    def create_folder(self, folder_name=None, parents=None):
        if folder_name is None:
            today = datetime.datetime.today() - datetime.timedelta(hours=21)
            folder_name = today.strftime("%a-%d-%b")

        if parents is None:
            parents = [self.drive_id]

        if type(parents) != list:
            parents = [parents]

        for sibling in self.get_children(parent_id=parents[0]):
            if sibling['name'] == folder_name:
                print("Folder already exists")
                return sibling

        file_metadata = {
            'name': folder_name,
            'mimeType': 'application/vnd.google-apps.folder',
            'parents': parents
        }

        file = self.service.files().create(body=file_metadata, fields='*').execute()
        return file

    def get_all(self, q='', spaces='drive', fields=DEFAULT_GET_FIELDS):
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
        return self.get_all(q=q, fields=fields)

    def get_children(self, parent_id=None):
        if parent_id is None:
            parent_id = self.drive_id
        return self.get_all(q=f"'{parent_id}' in parents")

    def tree(self, folder_id=None, indent=0):
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
        self.delete(file)

    def delete(self, drive_file):
        try:
            if type(drive_file) is dict:
                file_id = drive_file['id']
            elif type(drive_file) is str:
                file_id = drive_file
            else:
                raise ValueError
            self.service.files().delete(fileId=file_id).execute()
        except ValueError:  # FIXME specific Exception
            print("Received invalid parameter")

    def clear_folder(self, folder_id):
        content = self.get_children(parent_id=folder_id)
        trashed = []
        for f in content:
            trashed.append(f)
            self.delete(f)
        return trashed


def left_over():
    user = DriveUser(drive_id="1Hhz97eIh08IlNCDR2X35_PGYX8MH5kus")
    node = user.create_folder()
    files = [r"../tmp/1.jpg", r"../tmp/2.jpg", r"../tmp/3.jpg", r"../tmp/4.png"]
    # user.create_file(file_name="Test1", path=r"../tmp/1.jpg", parent_id=folder)

    trashed = user.clear_folder(node["id"])
    print("Removed:")
    for file in trashed:
        print(file)

    output = user.upload(path_list=files, parent_id=node)

    print("Uploaded:")
    for file in output:
        print(file)
