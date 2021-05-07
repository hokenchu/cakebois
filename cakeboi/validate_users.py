import json
import re

JSON = r'cakeboi/subscriber_list.json'


def validate_struct(path=JSON, verbose=True):
    try:
        with open(path) as f:
            users = json.load(f)

        # Check user list type (list)
        if type(users) is not list:
            raise TypeError("\nThe users are not saved as a list/array. Use: [ ... ]")

        # Check user type (dict)
        for u in users:
            if type(u) is not dict:
                print(u)
                raise TypeError("User is not saved as dictionary. Use { ... }")

        # Check attributes/keys
        for u in users:
            keys = []
            for key in u:
                keys.append(key)
            if sorted(keys) != sorted(['name', 'channel_id', 'sheet_id', 'drive_id']):
                raise TypeError("User is missing some attribute", u)
    except TypeError as err:
        print("[ERROR]", err)
        return False
    return True


def validate_raw(path=JSON, verbose=False):
    err_count = 0

    rules = {
        'start': r'^\[$',
        'head': r'^ *{$',
        '1': r'^ *"name": ".+",$',
        '2': r'^ *"channel_id": "\d{18}",$',
        '3': r'^ *"sheet_id": ".{44}",$',
        '4': r'^ *"drive_id": "\w{33}"$',
        'tail': r'^ *},$',
        'last_tail': r'^ *}$',
        'end': r'^ *]$',
    }

    with open(path) as f:
        lines = f.readlines()

    for (ln, text) in enumerate(lines, start=1):
        if ln == 1:
            regex = rules['start']
        elif ln == len(lines):
            regex = rules['end']
        else:
            i = (ln - 2) % 6
            if i == 0:
                regex = rules['head']
            elif i == 5 and ln == len(lines) - 1:
                regex = rules['last_tail']
            elif i == 5:
                regex = rules['tail']
            else:
                regex = rules[str(i)]

        if verbose or not re.match(re.compile(regex), text):
            print(f"\nChecking ln{ln} expecting /{regex}/")

        if not re.match(re.compile(regex), text):
            err_count += 1
            print(f"[ln {ln}] [WARNING!!!] {text.strip()}")
        else:
            if verbose:
                print(f"[ln {ln}] [Success] {text.strip()}")

    if err_count > 0:
        print("\n[Debug]", "[Validate sub list]", f"<{err_count}> lines are potentially wrong.\n")
        return False
    else:
        return True


def run():
    print('[Debug] [Validate sub list] - Start')
    struct = validate_struct()
    raw = validate_raw()
    if raw and struct:
        print('[Debug] [Validate sub list] - All seems good, buddy 👌')
    else:
        print("[Info]", "[Subscriber list]",
              "\n- Names can be any characters and whitespaces"
              "\n- Channel IDs consist of 18 digits"
              "\n- Sheet IDs consist of 44 characters"
              "\n- Drive IDs consist of 33 characters (mix of letters and numbers)")
        if raw and not struct:
            print("[Debug] [Validate sub list] - If that doesnt fix it, dunno whats wrong with your list man ☹️")
        else:
            print('[Debug] [Validate sub list] - You may want to check the user list for errors')
