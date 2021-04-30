import os

TMP_FOLDER = r"./tmp"


async def save(attachment, path=TMP_FOLDER):
    if not os.path.exists(path):
        os.makedirs(path)

    filepath = f"{path}/{attachment.filename}"
    print("[Log]", f"[{filepath}] Saving...")
    await attachment.save(filepath)
    print("[Log]", f"[{filepath}] Complete.")


async def save_all(message):
    from datetime import date
    album = f'{TMP_FOLDER}/{date.today().strftime("%y-%m-%d")}'

    for att in message.attachments:
        await save(att, album)
