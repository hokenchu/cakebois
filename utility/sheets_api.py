# google spreadsheets
import gspread

# authentication packages, for "Login"
from oauth2client.service_account import ServiceAccountCredentials

from utility.read_config import get

# Subroutine to find position of target cell.
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


def upload_link_batch(links):
    """
    Transfers images (http links only) from discord to google spreadsheet
    :param links: list of file/image links
    :return:
    """
    cred_file = get("credentials")
    svc_cred = get_service_credentials(cred_file)
    user = gspread.authorize(svc_cred)
    print("[Log]", "[sheets_api.py]", "Successfully authorized Google Spreadsheets")

    # Open the spreadsheet
    # First sheet of "CakeboiSheet"
    worksheet = user.open_by_key("1QPtUaV95DvA-25uokOo1qpf_58OPUkOTBRpwML_Yh48").sheet1

    (row, col) = get_position(worksheet)
    for (index, link) in enumerate(links, start=1):
        print("[Log]", "[sheets_api.py]", f"Updated cell at (Col{col + index}|Row{row}): {link}")
        worksheet.update_cell(row, col + index, f"=IMAGE(\"{link}\")")
