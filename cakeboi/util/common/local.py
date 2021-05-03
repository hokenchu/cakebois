import os

TMP_FOLDER = r"../tmp"


async def save(attachment, path=TMP_FOLDER):
    if not os.path.exists(path):
        os.makedirs(path)

    filepath = f"{path}/{attachment.filename}"
    if os.path.isfile(filepath):
        name = attachment.filename.split('.')[0]
        ext = attachment.filename.split('.')[1]

        n = 1
        filepath_n = f"{path}/{name}({n}).{ext}"
        while os.path.isfile(filepath_n):
            n = n + 1
            filepath_n = f"{path}/{name}({n}).{ext}"

        filepath = filepath_n
    print("[Log]", f"[{filepath}] Saving...")
    await attachment.save(filepath)
    print("[Log]", f"[{filepath}] Complete.")


async def save_all(message):
    from datetime import datetime
    today = datetime.today()
    album = f'{TMP_FOLDER}/{message.channel.id}/{today.strftime("%Y-%m-%d")}'

    for att in message.attachments:
        await save(att, album)
