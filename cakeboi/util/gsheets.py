# google spreadsheets
from datetime import datetime, timedelta

import gspread
# authentication packages, for "Login"
from oauth2client.service_account import ServiceAccountCredentials
from cakeboi.util import local
from cakeboi.util.guser import GoogleUser


def login(sheets_token=None):
    """
    Logs the user in and returns a service resource object
    """
    scope = ['https://www.googleapis.com/auth/spreadsheets',
             "https://www.googleapis.com/auth/drive.file",
             "https://www.googleapis.com/auth/drive",
             "https://spreadsheets.google.com/feeds"]
    token = local.get_token('sheets_token')
    cred = ServiceAccountCredentials.from_json_keyfile_dict(token, scope)
    user = gspread.authorize(cred)

    return user


class SheetsUser(GoogleUser):
    def __init__(self, name=None, channel_id=None, sheet_id=None):
        GoogleUser.__init__(self, name=name, channel_id=channel_id, sheet_id=sheet_id)
        self.worksheet = login().open_by_key(self.sheet_id).sheet1
        # print("[LOG]", "Initiated Google Sheets User")

    def update_cell(self, row, col, text):
        """
        Updates a certain cell value with a text
        """
        self.worksheet.update_cell(row, col, text)

    def comment(self, your_text="<no comment>", date = None):
        """
        Adds comment in the same row as today's date
        """
        if date is None:
            date = today_string()
        target_cell = self.worksheet.find(date)
        self.update_cell(target_cell.row, target_cell.col + 13, your_text)

    def set_outcome(self, outcome='n/a', date=None):
        """
        Sets outcome for today's battle
        """
        if date is None:
            date = today_string()
        target_cell = self.worksheet.find(date)
        self.update_cell(target_cell.row, target_cell.col + 10, outcome)
        pass

    def upload(self, list_of_links=None, start=1, date=None):
        """
        Adds image links to the same row as today's date
        starting at "start=1"
        """
        if date is None:
            date = today_string()
        if list_of_links is None:
            print("[Debug]", "Empty list was passed to sheets.helper.update()")
            return
        target_cell = self.worksheet.find(date)
        for (step, link) in enumerate(list_of_links, start=start):
            self.update_cell(target_cell.row, target_cell.col + step, f'=IMAGE("{link}")')

    def set_guildname(self, guild_name, date=None):
        if date is None:
            date = today_string()
        target_cell = self.worksheet.find(date)
        self.update_cell(target_cell.row, target_cell.col - 1, guild_name)
        pass


def today_string():
    """ Returns the TODAY in the right format for worksheet.find() """
    today = datetime.today() - timedelta(hours=19)
    return today.strftime("%d-%b-%Y")
