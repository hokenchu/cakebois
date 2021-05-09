import os
import shutil

TMP_FOLDER = r"./tmp"


def get_token(key):
    """
    Returns token as string if it's a single value or json/dict format
    """
    import os
    if os.path.isfile(r'keys.json'):
        print("[Debug]", "Loading local discord bot token")
        with open(r'keys.json', 'r') as read_file:
            key_string = read_file.read()
    else:
        key_string = os.getenv('keys')

    if key_string is None:
        raise RuntimeError("NO KEYFILE FOUND")

    import json
    key_dict = json.loads(key_string)

    return key_dict[key]


def empty_folder(path=TMP_FOLDER):
    """
    Clears the local tmp folder and creates a new one
    """
    if os.path.isdir(path):
        shutil.rmtree(path)

    os.makedirs(path)


def get_tmp():
    """
    Returns the path to the local tmp folder
    """
    return TMP_FOLDER


async def save(attachment, filename_base, channel):
    """
    Saves a discord.attachment in the local tmp folder
    """
    ext = attachment.filename.split('.')[-1]
    filename = f"{filename_base}.{ext}"
    path = get_path(channel)
    if not os.path.isdir(path):
        os.makedirs(path)
    filepath = f"{path}/{filename}"
    print(f"Saving [{filepath}]")
    await attachment.save(filepath)
    return filepath


def get_path(channel=None, channel_id=None):
    """
    Returns the tmp folder sub path for the current channel.
    Necessary so simultaneous uploads from different channels dont collide!

    Must pass either channel or channel_id
    """
    if channel is None and channel_id is None:
        raise ValueError("Expected at least one parameter")
    return f"{TMP_FOLDER}/{channel.id or channel_id}"


# Initial cleanup of residual files in tmp folder
empty_folder()
