from cakeboi.util.common.user import GoogleUser

TMP_FOLDER = r"../tmp"
DRIVE_ROOT = "1UtB-Xzi8uFV9WP4HQ7laflXXT_bOESXs"


class SheetsUser(GoogleUser):
    def __init__(self, name=None, channel_id=None, drive_id=None):
        GoogleUser.__init__(self, name=name, channel_id=channel_id, drive_id=drive_id)

    def upload(self, list_of_links=[], start=1):
        """
        Uploads last X images from discord to Drive
        """


@DeprecationWarning
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
