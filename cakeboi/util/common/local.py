import os
import shutil

TMP_FOLDER = r"./tmp"


def empty_tmp():
    if os.path.isdir(TMP_FOLDER):
        shutil.rmtree(TMP_FOLDER)

    os.makedirs(TMP_FOLDER)


def get_tmp():
    return TMP_FOLDER


async def save(attachment, filename_base, channel):
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
    pass either channel or channel_id
    """
    if channel is None and channel_id is None:
        raise ValueError("Expected at least one parameter")
    return f"{TMP_FOLDER}/{channel.id or channel_id}"


empty_tmp()
