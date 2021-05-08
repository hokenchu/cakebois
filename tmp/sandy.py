from datetime import datetime, timedelta

def today_string():
    """ Returns the TODAY in the right format for worksheet.find() """
    today = datetime.today() - timedelta(hours=12)
    return today.strftime("%a-%d-%b")
print(datetime.today())