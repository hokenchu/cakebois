from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

TMP_FOLDER = r"../tmp"
DRIVE_ROOT = "1UtB-Xzi8uFV9WP4HQ7laflXXT_bOESXs"


def get_drive():
    gauth = GoogleAuth()
    # gauth.LocalWebserverAuth()
    gauth.LoadCredentialsFile(r"../config/credentials.txt")
    if gauth.credentials is None:
        # Authenticate if they're not there
        gauth.LocalWebserverAuth()
    elif gauth.access_token_expired:
        # Refresh them if expired
        gauth.Refresh()
    else:
        # Initialize the saved creds
        gauth.Authorize()

    return GoogleDrive(gauth)


def left_over():
    drive = None
    # file1 = drive.CreateFile({'title': "FolderTODAY",
    #                              "parents": [{"id": id}],
    #                              "mimeType": "application/vnd.google-apps.folder"})

    # Create folder
    folder_metadata = {'title': 'MyFolder', 'mimeType': 'application/vnd.google-apps.folder'}
    folder = drive.CreateFile(folder_metadata)
    folder.Upload()

    # Get folder info and print to screen
    foldertitle = folder['title']
    folderid = folder['id']
    print('title: %s, id: %s' % (foldertitle, folderid))

    #
    # folder_id = "11Lu-L5-50lXkd9Ko9bjNkrj8flicvapR"
    # file = drive.CreateFile({"parents": [{"id": folder_id}]})
    # file.SetContentFile('../waifus/waifu.png')
    # file['title'] = "testFile"
    # file.Upload()
