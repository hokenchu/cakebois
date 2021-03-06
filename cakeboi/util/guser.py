import json

PATH_TO_SUB_LIST = r'cakeboi/subscriber_list.json'
with open(PATH_TO_SUB_LIST) as f:
    print("[Debug]", f"Loading user list from {PATH_TO_SUB_LIST}")
    subscriber_list = json.load(f)


def get_subscribers():
    return subscriber_list


class GoogleUser:
    """
    A user object that combines and keeps track of
    - Google Sheets spreadsheet ID
    - Google Drive folder ID
    - Discord Channel ID
    - and some arbitrary username

    Loads its information from subscriber_list file
    """

    def __init__(self, name=None, channel_id=None, sheet_id=None, drive_id=None):
        match = None
        if name:
            for sub in subscriber_list:
                if name == sub["name"]:
                    match = sub
                    break
        elif channel_id:
            channel_id = str(channel_id)
            for sub in subscriber_list:
                if channel_id == sub["channel_id"]:
                    match = sub
                    break
        elif sheet_id:
            for sub in subscriber_list:
                if sheet_id == sub["sheet_id"]:
                    match = sub
                    break
        elif drive_id:
            for sub in subscriber_list:
                if drive_id == sub["drive_id"]:
                    match = sub
                    break

        # Remove this if you dont care about errors
        if match is None:
            raise ValueError("[CRITICAL] Expected either name, channel_id, sheet_id or drive_id")

        self.name = match["name"]
        self.channel_id = match["channel_id"]
        self.sheet_id = match["sheet_id"]
        self.drive_id = match["drive_id"]
