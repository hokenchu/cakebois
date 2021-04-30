TMP_FOLDER = r"./tmp"


async def save(attachment, path=TMP_FOLDER):
    filepath = f"{path}/{attachment.filename}"
    print("[Log]", f"[{filepath}] Saving...")
    await attachment.save(filepath)
    print("[Log]", f"[{filepath}] Complete.")


async def save_all(message):
    import os
    from datetime import date

    album = f'{TMP_FOLDER}/{date.today().strftime("%y-%m-%d")}'
    if not os.path.exists(album):
        os.makedirs(album)

    for att in message.attachments:
        await save(att, album)
