

from cakeboi.bot import cakeboi
from cakeboi import validate_users
if __name__ == '__main__':
    validate_users.run()
    from cakeboi.util import gdrive

    u = gdrive.DriveUser(name="Realm")
    u.get_folders()

    cakeboi.run()
