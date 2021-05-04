import json
import re

JSON = r'subscriber_list.json'


def validate_objects(path=JSON, verbose=True):
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


def validate_layout(path=JSON, verbose=False):
    err_count = 0

    rules = {
        'start': r'^\[$',
        'head': r'^ *{$',
        '1': r'^ *"name": ".+",$',
        '2': r'^ *"channel_id": "\d+",$',
        '3': r'^ *"sheet_id": ".+",$',
        '4': r'^ *"drive_id": ".+"$',
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
            print(f"Checking ln{ln} expecting /{regex}/")

        if not re.match(re.compile(regex), text):
            err_count += 1
            print(f"[ln {ln}] [WARNING!!!] {text}")
        else:
            if verbose:
                print(f"[ln {ln}] [Success] {text}")

    if err_count > 0:
        print(f"\n-----------------\n<{err_count}> lines potentially wrong.")
        return False
    else:
        return True


if __name__ == '__main__':
    if validate_objects() and validate_layout():
        print('All seems good, buddy 👌')
    else:
        print('You may want to check the code for errors\n')
        out = ""
        print("Run script to check code line by line? (Y/n)")
        while out not in ["y", "Y", "yes", "Yes", "n", "N", "no", "No"]:
            out = input()
        if (out in ["y", "Y", "yes", "Yes"]) and validate_layout():
            print("Dunno whats wrong with your code man ☹️")
