# google spreadsheets
from datetime import datetime, timedelta

import gspread
# authentication packages, for "Login"
from oauth2client.service_account import ServiceAccountCredentials

from cakeboi.util.common.user import GoogleUser


def login(json_path="cakeboi/util/sheets/discord_cakeboi.json"):
    """
    Logs the user in and returns a service resource object
    """
    scope = ['https://www.googleapis.com/auth/spreadsheets',
             "https://www.googleapis.com/auth/drive.file",
             "https://www.googleapis.com/auth/drive",
             "https://spreadsheets.google.com/feeds"]

    cred = ServiceAccountCredentials.from_json_keyfile_name(json_path, scope)
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

    def comment(self, your_text="<no comment>"):
        """
        Adds comment in the same row as today's date
        """
        today_cell = self.worksheet.find(today_string())
        self.update_cell(today_cell.row, today_cell.col + 13, your_text)

    def set_outcome(self, outcome='n/a'):
        """
        Sets outcome for today's battle
        """
        today_cell = self.worksheet.find(today_string())
        self.update_cell(today_cell.row, today_cell.col + 10, outcome)
        pass

    def upload(self, list_of_links=None, start=1):
        """
        Adds image links to the same row as today's date
        starting at "start=1"
        """
        if list_of_links is None:
            print("[Debug]", "Empty list was passed to sheets.helper.update()")
            return
        today_cell = self.worksheet.find(today_string())
        for (step, link) in enumerate(list_of_links, start=start):
            self.update_cell(today_cell.row, today_cell.col + step, f'=IMAGE("{link}")')

    def set_guildname(self, guild_name):
        today_cell = self.worksheet.find(today_string())
        self.update_cell(today_cell.row, today_cell.col - 1, guild_name)
        pass


def today_string():
    """ Returns the TODAY in the right format for worksheet.find() """
    today = datetime.today() - timedelta(hours=19)
    return today.strftime("%a-%d-%b")
