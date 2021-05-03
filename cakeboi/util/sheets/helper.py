# google spreadsheets
import json
from datetime import datetime, timedelta

import gspread
# authentication packages, for "Login"
from oauth2client.service_account import ServiceAccountCredentials

from cakeboi.prototype import read_config

with open(r'C:\Data\Projects\Py\pythonProject\cakebois\cakeboi\subscriber_list.json') as f:
    subscriber_list = json.load(f)


class SheetsUser:
    def __init__(self, name=None, channel_id=None, sheet_id=None):
        if name:
            for subscriber in subscriber_list:
                if name == subscriber["name"]:
                    self.name = subscriber["name"]
                    self.channel_id = subscriber["channel_id"]
                    self.sheet_id = subscriber["sheet_id"]
                    break
        elif channel_id:
            channel_id = str(channel_id)
            for subscriber in subscriber_list:
                if channel_id == subscriber["channel_id"]:
                    self.name = subscriber["name"]
                    self.channel_id = subscriber["channel_id"]
                    self.sheet_id = subscriber["sheet_id"]
                    break
        elif sheet_id:
            for subscriber in subscriber_list:
                if sheet_id == subscriber["sheet_id"]:
                    self.name = subscriber["name"]
                    self.channel_id = subscriber["channel_id"]
                    self.sheet_id = subscriber["sheet_id"]
                    break
        else:
            raise ValueError("[CRITICAL] Expected either name, channel_id or sheet_id")
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
        self.update_cell(today_cell.row, today_cell.col - 1, your_text)

    def upload(self, list_of_links=[], start=1):
        """
        Adds image links to the same row as today's date
        starting at "start=1"
        """
        today_cell = self.worksheet.find(today_string())
        for (step, link) in enumerate(list_of_links, start=start):
            self.update_cell(today_cell.row, today_cell.col + step, f'=IMAGE("{link}")')


def login(json_path="util/sheets/discord_cakeboi.json"):
    scope = ['https://www.googleapis.com/auth/spreadsheets',
             "https://www.googleapis.com/auth/drive.file",
             "https://www.googleapis.com/auth/drive",
             "https://spreadsheets.google.com/feeds"]

    cred = ServiceAccountCredentials.from_json_keyfile_name(json_path, scope)
    user = gspread.authorize(cred)

    return user


def today_string():
    """ Returns the TODAY in the right format for worksheet.find() """
    today = datetime.today() - timedelta(hours=21)
    return today.strftime("%a-%d-%b")


@DeprecationWarning
def get_sheet(channel_id=None, sheet_id=None):
    if sheet_id is None:
        if channel_id is not None:
            for user in subscriber_list:
                print(user["channel_id"], "\n", channel_id)
                if user["channel_id"] == channel_id:
                    sheet_id = user["sheet_id"]
        else:
            # TODO exception
            print("[ERROR]", "no IDs passed")
            return

    if sheet_id is None:
        # TODO exception
        print("[ERROR]", "no matching channel_id")
        return

    bot_user = login()
    return bot_user.open_by_key(sheet_id).sheet1  # Open the spreadsheet


@DeprecationWarning
def comment(search_string, text, sheet_id=None, channel_id=None):
    worksheet = get_sheet(channel_id=channel_id, sheet_id=sheet_id)
    # Finds cell containing specified string
    cell = worksheet.find(search_string)
    # Updates the cell to the right of the previous one
    worksheet.update_cell(cell.row, cell.col + 1, text)


@DeprecationWarning
def get_position(worksheet):
    """
    Subroutine to find position of target cell.

    Target cell is the cell containing today's date.
    Returns row and col number.
    """
    from datetime import date

    # string format time
    # % :: start of placeholder
    # d :: day (numeric)

    # a :: weekday (abbr)
    # A :: weekday
    # b :: month

    cell_of_today = date.today().strftime("%a-%d-%b")
    return worksheet.find(cell_of_today).row, worksheet.find(cell_of_today).col


@DeprecationWarning
def get_service_credentials(path_to_credentials_json):
    """
    Subroutine to get Service Credentials for gspread.authorize()
    :param path_to_credentials_json:
    :return:
    """
    scope = [
        'https://www.googleapis.com/auth/spreadsheets',
        "https://www.googleapis.com/auth/drive.file",
        "https://www.googleapis.com/auth/drive",
        "https://spreadsheets.google.com/feeds"]

    return ServiceAccountCredentials.from_json_keyfile_name(path_to_credentials_json, scope)


@DeprecationWarning
def upload_link_batch(links):
    """
    Transfers images (http links only) from discord to google spreadsheet
    :param links: list of file/image links
    :return:
    """
    cred_file = read_config.get("credentials")
    svc_cred = get_service_credentials(cred_file)
    user = gspread.authorize(svc_cred)
    print("[Log]", "[local.py]", "Successfully authorized Google Spreadsheets")

    # Open the spreadsheet
    # First sheet of "CakeboiSheet"
    worksheet = user.open_by_key("1QPtUaV95DvA-25uokOo1qpf_58OPUkOTBRpwML_Yh48").sheet1

    (row, col) = get_position(worksheet)

    for (index, link) in enumerate(links, start=1):
        print("[Log]", "[local.py]", f"Updated cell at (Col{col + index}|Row{row}): {link}")
        worksheet.update_cell(row, col + index, f"=IMAGE(\"{link}\")")
