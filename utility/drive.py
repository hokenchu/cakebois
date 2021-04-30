from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

TMP_FOLDER = r"../tmp"

if __name__ == '__main__':
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

    drive = GoogleDrive(gauth)
    file = drive.CreateFile()
    file.SetContentFile('../waifus/waifu.png')
    file['title'] = "testFile"
    file.Upload()
