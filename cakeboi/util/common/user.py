import json

# This needs to run when
# from cakeboi.util.common.user import GoogleUser
# is run
with open(r'subscriber_list.json') as f:
    subscriber_list = json.load(f)
    print("Loaded user list")

class GoogleUser:
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
