# google spreadsheets
import gspread

# authentication packages, for "Login"
from oauth2client.service_account import ServiceAccountCredentials


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


def verify():
    scope = [
        'https://www.googleapis.com/auth/spreadsheets',
        "https://www.googleapis.com/auth/drive.file",
        "https://www.googleapis.com/auth/drive",
        "https://spreadsheets.google.com/feeds"]

    return ServiceAccountCredentials.from_json_keyfile_name("../config/credentials.json", scope)


# main routine
if __name__ == '__main__':

    user = gspread.authorize(verify())

    # Worksheet (Reference)
    worksheet = user.open("CakeboiSheet").sheet1  # Open the spreadsheet

    # get position of "today cell"
    (row, col) = get_position(worksheet)

    # TODO
    img_list = ["Image1", "Image2", "Image3", "Image4", "Image5", "Image6", ]  # ... bis 9 Links

    # insert guild name into left cell of 'date'
    # TODO
    worksheet.update_cell(row, col - 1, "Guild_Name_plcd")

    # inserts certain link
    # EXAMPLE
    img_link = "http://pullSomePicsOutaMyAss.com"  # Placeholder
    mein_string = f'=IMAGE("{img_link}")'
    worksheet.update_cell(row, col + 1, mein_string)

    x = 1
    for img in img_list:
        worksheet.update_cell(row, col + x, f"{img}")
        x = x + 1
