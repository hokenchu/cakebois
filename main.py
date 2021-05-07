

from cakeboi.bot import cakeboi
from cakeboi import validate_users
if __name__ == '__main__':
    validate_users.run()
    from cakeboi.util.drive.helper import DriveUser
    u = DriveUser(name="Realm")
    if validate_users: # placeholder
        cakeboi.run()
